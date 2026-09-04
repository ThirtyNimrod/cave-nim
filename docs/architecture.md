# Architecture

## Pipeline overview

```mermaid
flowchart TD
    A["generate_daily.yml<br/>cron 14:00 UTC + manual"] --> B["generator.py<br/>Gemini: verse + icon"]
    B --> C["illustrator.py<br/>resolve icon SVG"]
    C --> D["compositor.py<br/>Playwright render"]
    D --> E[("canon.json entry<br/>appended")]
    E --> F["you review the PNG<br/>in assets/rendered/<br/>and post it yourself"]
```

There is currently no automated publishing step — see
[current-implementation-plan.md](current-implementation-plan.md) for why an
earlier Meta Graph API integration was removed from this branch.

## Modules (`src/`)

- **`config.py`** — every constant in one place: the 4 palettes, chapter
  length (30), card dimensions (1080x1350), file paths, the caption
  template, and the Gemini model name. Loads secrets from the environment
  (via `python-dotenv` locally).
- **`canon.py`** — all reads/writes of `database/canon.json`: atomic save
  (write to a temp file, then `os.replace`), the chapter/verse/palette-index
  math (`next_position`), and appending a new entry.
- **`generator.py`** — the one Gemini call per post. Builds a prompt from
  the brand-voice rules plus the current icon manifest (so the model can
  only choose an icon slug that actually exists), asks for JSON, validates
  the shape (exactly 3 non-empty lines, a known icon slug), and retries on
  transient failures.
- **`illustrator.py`** — loads `assets/doodles/manifest.json`, resolves a
  slug to its SVG file, and normalizes every SVG (strips fixed width/height
  so CSS controls sizing, forces `stroke="currentColor"`) so the palette's
  ink color can drive the icon's color purely via CSS. This is the entire
  "recoloring" mechanism — there is no raster image processing anywhere in
  this pipeline.
- **`compositor.py`** — fills `templates/card_template.html`'s placeholder
  tokens, opens it in headless Chromium via Playwright at an exact
  1080x1350 viewport, waits for `document.fonts.ready`, and screenshots.

## `main.py`

A plain CLI, no framework — one subcommand, which never shells out to git
(git commit/push only happens in the GitHub Actions YAML, never in Python):

- `generate [--mock]` — `--mock` skips Gemini and `canon.json` entirely, for
  free, instant template iteration.

Instagram publishing (`publish`/`status` subcommands, `src/publisher.py`,
`.github/workflows/publish.yml`) was removed from this branch — see
[current-implementation-plan.md](current-implementation-plan.md). That code
still exists as-is on the `meta-idea` git branch.

## `database/canon.json`

One JSON array, one object per post, appended to by `generate`:

```json
{
  "id": "1.14", "chapter": 1, "verse": 14,
  "palette_index": 1, "palette_name": "Forest Tablet",
  "icon": "fire", "theme": "patience before action",
  "lines": ["...", "...", "..."],
  "caption": "nim. 1.14\n.\n.\n#nim ...",
  "image_path": "assets/rendered/1.14.png"
}
```

`caption` is computed once at generate time and stored verbatim, so whatever
text sits next to a rendered PNG is exactly what should go in the Instagram
post if you copy it over by hand.

## Numbering and palette rotation

For the *n*th post (0-indexed):

```
chapter       = n // 30 + 1
verse         = n % 30 + 1
palette_index = n % 4
```

Verified against the brand spec's own example: post 14 (n=13) → chapter 1,
verse 14, palette_index 1 (Forest Tablet) — exactly `nim. 1.14`.
