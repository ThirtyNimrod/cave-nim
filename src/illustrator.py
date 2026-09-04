import json
import re

from . import config

_STROKE_COLOR_RE = re.compile(r'stroke="(?!currentColor)[^"]*"')
_DIMENSION_RE = re.compile(r'\s(width|height)="[^"]*"')


def load_manifest() -> dict:
    if not config.MANIFEST_PATH.exists():
        return {}
    with open(config.MANIFEST_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def available_slugs() -> list[str]:
    return sorted(load_manifest().keys())


def icon_tags() -> dict[str, list[str]]:
    return {slug: data.get("tags", []) for slug, data in load_manifest().items()}


def _normalize_svg(raw_svg: str) -> str:
    """Strip fixed width/height so CSS controls sizing, and force stroke=currentColor
    so the palette's ink color (set via CSS on the wrapping element) drives the icon
    color with no raster tinting step."""
    svg = _DIMENSION_RE.sub("", raw_svg)
    svg = _STROKE_COLOR_RE.sub('stroke="currentColor"', svg)
    return svg


def get_icon_svg(slug: str) -> str:
    manifest = load_manifest()
    if slug not in manifest:
        raise ValueError(f"Unknown icon slug {slug!r}. Available: {sorted(manifest.keys())}")
    path = config.DOODLES_DIR / manifest[slug]["file"]
    with open(path, "r", encoding="utf-8") as f:
        return _normalize_svg(f.read())


def get_fixed_icon(path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return _normalize_svg(f.read())
