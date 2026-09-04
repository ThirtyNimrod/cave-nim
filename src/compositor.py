import html
from pathlib import Path

from playwright.sync_api import sync_playwright

from . import config


def _read_template() -> str:
    with open(config.TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()


def _font_size_for(lines: list[str]) -> int:
    """Longest line drives font size for the whole verse, so a wordy line doesn't
    wrap and crowd out its shorter neighbors within the same card."""
    longest = max(len(line) for line in lines)
    if longest <= 25:
        return 54
    if longest <= 35:
        return 46
    if longest <= 45:
        return 38
    return 32


def _gradient_css(palette: dict) -> str:
    stops = palette["stops"]
    return (
        f"linear-gradient({config.GRADIENT_ANGLE}deg, "
        f"{stops[0]} 0%, {stops[1]} 50%, {stops[2]} 100%)"
    )


def render_card(*, lines: list[str], icon_svg: str, sun_icon_svg: str, chapter: int,
                 verse: int, palette: dict, font: dict, output_path: Path) -> None:
    font_link = (
        '<link rel="stylesheet" '
        f'href="https://fonts.googleapis.com/css2?family={font["google_param"]}&display=swap">'
    )
    replacements = {
        "__CANVAS__": _gradient_css(palette),
        "__INK_COLOR__": palette["ink"],
        "__FONT_LINK__": font_link,
        "__FONT_FAMILY__": font["family"],
        "__FONT_SIZE__": str(_font_size_for(lines)),
        "__SUN_ICON_SVG__": sun_icon_svg,
        "__DOODLE_SVG__": icon_svg,
        "__LINE_1__": html.escape(lines[0]),
        "__LINE_2__": html.escape(lines[1]),
        "__LINE_3__": html.escape(lines[2]),
        "__CHAPTER__": str(chapter),
        "__VERSE__": str(verse),
    }
    page_html = _read_template()
    for token, value in replacements.items():
        page_html = page_html.replace(token, value)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page(
                viewport={"width": config.CARD_WIDTH, "height": config.CARD_HEIGHT},
                device_scale_factor=1,
            )
            # networkidle so the Google Fonts stylesheet + font file (external
            # requests) finish before document.fonts.ready is checked below.
            page.set_content(page_html, wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            page.screenshot(path=str(output_path))
        finally:
            browser.close()
