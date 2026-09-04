import json
import os
import random
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
        "palette_index": random.randrange(len(config.PALETTES)),
    }


def append_entry(entries: list[dict], *, pos: dict, lines: list[str], icon: str,
                  theme: str, font: str, image_path: str) -> dict:
    palette = config.PALETTES[pos["palette_index"]]
    entry = {
        "index": pos["index"],
        "chapter": pos["chapter"],
        "verse": pos["verse"],
        "id": f"{pos['chapter']}.{pos['verse']}",
        "created_at": _now_iso(),
        "palette_index": pos["palette_index"],
        "palette_name": palette["name"],
        "font": font,
        "icon": icon,
        "theme": theme,
        "lines": lines,
        "caption": config.CAPTION_TEMPLATE.format(chapter=pos["chapter"], verse=pos["verse"]),
        "image_path": image_path,
    }
    entries.append(entry)
    return entry
