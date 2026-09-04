import json
import re

from . import config

_STROKE_COLOR_RE = re.compile(r'stroke="(?!currentColor)[^"]*"')
_FILL_COLOR_RE = re.compile(r'fill="(black|#000000|#000)"', re.IGNORECASE)
_SVG_OPEN_TAG_RE = re.compile(r'^<svg\b[^>]*>')
_DIMENSION_ATTR_RE = re.compile(r'\s(width|height)="[^"]*"')


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
    """Strip fixed width/height from the root <svg> tag only -- NOT globally,
    since some source icons carry a <clipPath><rect width=.. height=..>...
    internally, and stripping those collapses the clip region to zero and
    hides the whole icon. CSS then controls the rendered size (each icon
    keeps its own viewBox, so non-square source art still scales to fit
    without distortion). Also forces any hardcoded black stroke/fill to
    currentColor so the palette's ink color (set via CSS on the wrapping
    element) drives the icon color with no raster tinting step."""
    svg = _SVG_OPEN_TAG_RE.sub(lambda m: _DIMENSION_ATTR_RE.sub("", m.group(0)), raw_svg, count=1)
    svg = _STROKE_COLOR_RE.sub('stroke="currentColor"', svg)
    svg = _FILL_COLOR_RE.sub('fill="currentColor"', svg)
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
