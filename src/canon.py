import json
import os
from datetime import datetime, timezone

from . import config


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def load_entries() -> list[dict]:
    if not config.CANON_PATH.exists():
        return []
    with open(config.CANON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_entries(entries: list[dict]) -> None:
    tmp_path = config.CANON_PATH.with_suffix(".json.tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp_path, config.CANON_PATH)


def next_position(entries: list[dict]) -> dict:
    n = len(entries)
    return {
        "index": n,
        "chapter": n // config.POSTS_PER_CHAPTER + 1,
        "verse": n % config.POSTS_PER_CHAPTER + 1,
        "palette_index": n % len(config.PALETTES),
    }


def append_entry(entries: list[dict], *, pos: dict, lines: list[str], icon: str,
                  theme: str, image_path: str) -> dict:
    palette = config.PALETTES[pos["palette_index"]]
    entry = {
        "index": pos["index"],
        "chapter": pos["chapter"],
        "verse": pos["verse"],
        "id": f"{pos['chapter']}.{pos['verse']}",
        "created_at": _now_iso(),
        "palette_index": pos["palette_index"],
        "palette_name": palette["name"],
        "icon": icon,
        "theme": theme,
        "lines": lines,
        "caption": config.CAPTION_TEMPLATE.format(chapter=pos["chapter"], verse=pos["verse"]),
        "image_path": image_path,
        "status": "pending_review",
        "published": False,
        "published_at": None,
        "ig_container_id": None,
        "ig_media_id": None,
        "publish_error": None,
    }
    entries.append(entry)
    return entry


def list_pending(entries: list[dict]) -> list[dict]:
    return [e for e in entries if not e["published"]]


def find_pending(entries: list[dict], canon_ref: str | None) -> dict:
    if canon_ref:
        for entry in entries:
            if entry["id"] == canon_ref:
                if entry["published"]:
                    raise ValueError(
                        f"{canon_ref} was already published at {entry['published_at']} "
                        f"(ig_media_id={entry['ig_media_id']})."
                    )
                return entry
        raise ValueError(f"No canon entry found with id {canon_ref!r}.")

    pending = list_pending(entries)
    if not pending:
        raise ValueError("No pending entries to publish.")
    return max(pending, key=lambda e: e["index"])


def mark_published(entry: dict, *, ig_media_id: str) -> None:
    entry["published"] = True
    entry["status"] = "published"
    entry["published_at"] = _now_iso()
    entry["ig_media_id"] = ig_media_id
    entry["publish_error"] = None


def mark_publish_failed(entry: dict, *, error: str, container_id: str | None = None) -> None:
    entry["status"] = "publish_failed"
    entry["publish_error"] = error
    if container_id:
        entry["ig_container_id"] = container_id
