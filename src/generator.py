import json
import time

from google import genai

from . import config, illustrator


class GenerationError(Exception):
    pass


_PROMPT_TEMPLATE = """You are the voice of "nim.", an ancient, calm caveman who carves \
short stoic proverbs about primal survival wisdom.

Voice rules:
- Never use modern words (no "mental health", "stress", "routine", "anxiety", "grind").
- Drop articles ("the", "a", "an") and auxiliary verbs ("is", "are", "will") where natural.
- Speak in short, plain, elemental language. Warm and grounding, never preachy or aggressive.
- Translate modern struggles into elemental metaphors (fire, stone, cave, hunt, storm, river).

Write exactly 3 short lines (a single proverb split across 3 lines) about {theme_hint}.
Also choose the ONE icon slug from this list that best matches the proverb's subject:
{icon_menu}

Avoid repeating these recently used icons if you reasonably can: {recent_icons}

Respond with ONLY a JSON object, no markdown fences, in this exact shape:
{{"lines": ["line one", "line two", "line three"], "icon": "chosen-slug", "theme": "short theme label"}}
"""

_DEFAULT_THEME_HINT = "everyday resilience, patience, or quiet strength"


def _build_prompt(icon_slugs: list[str], tags_by_slug: dict, recent_icons: list[str]) -> str:
    icon_menu = "\n".join(
        f"- {slug} ({', '.join(tags_by_slug.get(slug, []))})" for slug in icon_slugs
    )
    return _PROMPT_TEMPLATE.format(
        theme_hint=_DEFAULT_THEME_HINT,
        icon_menu=icon_menu,
        recent_icons=", ".join(recent_icons) if recent_icons else "none",
    )


def _validate(data: dict, icon_slugs: list[str]) -> dict:
    lines = data.get("lines")
    icon = data.get("icon")
    if not isinstance(lines, list) or len(lines) != 3 or not all(
        isinstance(line, str) and line.strip() for line in lines
    ):
        raise GenerationError(f"Model returned malformed lines: {lines!r}")
    if icon not in icon_slugs:
        raise GenerationError(f"Model returned unknown icon {icon!r}, expected one of {icon_slugs}")
    return {
        "lines": [line.strip() for line in lines],
        "icon": icon,
        "theme": str(data.get("theme", "")).strip(),
    }


def generate_verse(recent_icons: list[str] | None = None, retries: int = 2) -> dict:
    icon_slugs = illustrator.available_slugs()
    if not icon_slugs:
        raise GenerationError(
            "No icons available in assets/doodles/manifest.json. "
            "Vendor the icon library before running generate without --mock."
        )
    if not config.GEMINI_API_KEY:
        raise GenerationError("GEMINI_API_KEY is not set. Copy .env.example to .env and fill it in.")

    prompt = _build_prompt(icon_slugs, illustrator.icon_tags(), recent_icons or [])
    client = genai.Client(api_key=config.GEMINI_API_KEY)

    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            response = client.models.generate_content(
                model=config.GEMINI_MODEL,
                contents=prompt,
                config={"response_mime_type": "application/json"},
            )
            data = json.loads(response.text)
            return _validate(data, icon_slugs)
        except Exception as exc:  # noqa: BLE001 - retrying any transient API/parse failure
            last_error = exc
            if attempt < retries:
                time.sleep(2 ** attempt)

    raise GenerationError(f"Gemini generation failed after {retries + 1} attempts: {last_error}")
