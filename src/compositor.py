import html
from pathlib import Path

from playwright.sync_api import sync_playwright

from . import config


def _read_template() -> str:
    with open(config.TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()


def render_card(*, lines: list[str], icon_svg: str, sun_icon_svg: str, chapter: int,
                 verse: int, palette: dict, output_path: Path) -> None:
    replacements = {
        "__CANVAS_COLOR__": palette["canvas"],
        "__INK_COLOR__": palette["ink"],
        "__FONT_URL__": config.FONT_PATH.resolve().as_uri(),
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
            page.set_content(page_html)
            # Headless Chromium can otherwise screenshot before the @font-face
            # finishes loading and silently fall back to a system font.
            page.evaluate("document.fonts.ready")
            page.screenshot(path=str(output_path))
        finally:
            browser.close()
