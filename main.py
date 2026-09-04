import argparse
import sys

from src import canon, compositor, config, generator, illustrator, publisher

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
    print("Status: pending_review. Run 'python main.py publish' once you've reviewed it.")
    return 0


def cmd_publish(args: argparse.Namespace) -> int:
    entries = canon.load_entries()
    try:
        entry = canon.find_pending(entries, args.canon_ref or None)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    image_url = f"https://raw.githubusercontent.com/{config.GITHUB_REPOSITORY}/main/{entry['image_path']}"

    try:
        result = publisher.publish_entry(image_url, entry["caption"], dry_run=args.dry_run)
    except publisher.PublishError as exc:
        canon.mark_publish_failed(entry, error=str(exc), container_id=exc.container_id)
        canon.save_entries(entries)
        print(f"Publish failed for {entry['id']}: {exc}", file=sys.stderr)
        return 1

    if args.dry_run:
        canon.save_entries(entries)
        print(f"Dry run OK for {entry['id']}: container {result['container_id']} created and polled successfully.")
        print("No post was published (--dry-run). Re-run without --dry-run to actually publish.")
        return 0

    canon.mark_published(entry, ig_media_id=result["ig_media_id"])
    canon.save_entries(entries)
    print(f"Published {entry['id']} as Instagram media {result['ig_media_id']}.")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    entries = canon.load_entries()
    pending = canon.list_pending(entries)
    if not pending:
        print("No pending entries.")
        return 0
    for entry in pending:
        print(f"{entry['id']} [{entry['status']}] {entry['image_path']}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="nim. daily post pipeline")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_generate = subparsers.add_parser("generate", help="Generate, illustrate, and render the next card.")
    p_generate.add_argument("--mock", action="store_true", help="Use canned content, skip Gemini and canon.json.")
    p_generate.set_defaults(func=cmd_generate)

    p_publish = subparsers.add_parser("publish", help="Publish a pending card to Instagram.")
    p_publish.add_argument("--canon-ref", default=None, help="e.g. 1.14. Defaults to the latest pending entry.")
    p_publish.add_argument("--dry-run", action="store_true", help="Create and poll the container but don't publish.")
    p_publish.set_defaults(func=cmd_publish)

    p_status = subparsers.add_parser("status", help="List all pending (unpublished) entries.")
    p_status.set_defaults(func=cmd_status)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
