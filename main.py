import argparse
import sys

from src import canon, compositor, config, generator, illustrator

_MOCK_ICON_SVG = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="8"/></svg>'
)
_MOCK_LINES = [
    "fire burn hot only when wood dry",
    "wet branch make smoke, hurt eyes",
    "nim wait for dry branch",
]


def _sun_icon_svg() -> str:
    if config.SUN_ICON_PATH.exists():
        return illustrator.get_fixed_icon(config.SUN_ICON_PATH)
    return _MOCK_ICON_SVG


def cmd_generate(args: argparse.Namespace) -> int:
    if args.mock:
        output_path = config.RENDERED_DIR / "_preview.png"
        compositor.render_card(
            lines=_MOCK_LINES,
            icon_svg=_MOCK_ICON_SVG,
            sun_icon_svg=_sun_icon_svg(),
            chapter=1,
            verse=1,
            palette=config.PALETTES[0],
            output_path=output_path,
        )
        print(f"Mock card rendered to {output_path} (canon.json untouched).")
        return 0

    entries = canon.load_entries()
    recent_icons = [e["icon"] for e in entries[-15:]]
    try:
        result = generator.generate_verse(recent_icons=recent_icons)
    except generator.GenerationError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    pos = canon.next_position(entries)
    palette = config.PALETTES[pos["palette_index"]]
    image_path = config.RENDERED_DIR / f"{pos['chapter']}.{pos['verse']:02d}.png"

    compositor.render_card(
        lines=result["lines"],
        icon_svg=illustrator.get_icon_svg(result["icon"]),
        sun_icon_svg=_sun_icon_svg(),
        chapter=pos["chapter"],
        verse=pos["verse"],
        palette=palette,
        output_path=image_path,
    )

    entry = canon.append_entry(
        entries,
        pos=pos,
        lines=result["lines"],
        icon=result["icon"],
        theme=result["theme"],
        image_path=str(image_path.relative_to(config.BASE_DIR)).replace("\\", "/"),
    )
    canon.save_entries(entries)
    print(f"Generated {entry['id']}: {' / '.join(entry['lines'])}")
    print(f"Image: {entry['image_path']}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="nim. daily post pipeline")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_generate = subparsers.add_parser("generate", help="Generate, illustrate, and render the next card.")
    p_generate.add_argument("--mock", action="store_true", help="Use canned content, skip Gemini and canon.json.")
    p_generate.set_defaults(func=cmd_generate)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
