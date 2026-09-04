# Architecture

## Pipeline overview

```mermaid
flowchart TD
    A["python main.py generate --count N<br/>manual, local"] --> B["generator.py<br/>Gemini: verse + icon"]
    B --> C["illustrator.py<br/>resolve icon SVG"]
    C --> D["compositor.py<br/>Playwright render"]
    D --> E[("canon.json entry<br/>appended")]
    E --> F["python main.py list / gallery<br/>review offline"]
    F --> G["you post it to Instagram yourself"]
```

No GitHub Actions, no cron, no server. Everything runs as a local CLI
command against local files. There is also currently no automated
publishing step — see [current-implementation-plan.md](current-implementation-plan.md)
for why an earlier Meta Graph API integration was removed from this branch.

## Modules (`src/`)

- **`config.py`** — every constant in one place: the 4 palettes, chapter
  length (30), card dimensions (1080x1350), file paths, the caption
  template, and the Gemini model name. Loads secrets from the environment
  (via `python-dotenv` locally).
- **`canon.py`** — all reads/writes of `database/canon.json`: atomic save
  (write to a temp file, then `os.replace`), the chapter/verse/palette-index
  math (`next_position`), and appending a new entry.
- **`generator.py`** — one Gemini call per post. Builds a prompt from the
  brand-voice rules plus the current icon manifest (so the model can only
  choose an icon slug that actually exists), asks for JSON, validates the
  shape (exactly 3 non-empty lines, a known icon slug), and retries on
  transient failures.
- **`illustrator.py`** — loads `assets/doodles/manifest.json`, resolves a
  slug to its SVG file, and normalizes every SVG (strips fixed width/height
  so CSS controls sizing, forces `stroke="currentColor"`) so the palette's
  ink color can drive the icon's color purely via CSS. This is the entire
  "recoloring" mechanism — no raster image processing anywhere.
- **`compositor.py`** — fills `templates/card_template.html`'s placeholder
  tokens, opens it in headless Chromium via Playwright at an exact
  1080x1350 viewport, waits for `document.fonts.ready`, and screenshots.
- **`gallery.py`** — builds a static, offline HTML page (`gallery.html`)
  from every `canon.json` entry: a grid of the rendered PNG plus its id,
  icon, theme, and text, newest first. No server, no build step — open the
  file directly in a browser.

## `main.py`

A plain CLI, no framework — three subcommands, none of which shell out to
git:

- `generate [--mock] [--count N]` — `--mock` skips Gemini and `canon.json`
  entirely for free, instant template iteration. `--count` (default 1)
  loops the real generate-render-append cycle N times in one run — e.g. a
  weekly batch of 7, each post getting its own Gemini call so icon/theme
  variety holds up.
- `list` — prints every post generated so far (id, icon, theme, first line).
- `gallery` — writes `gallery.html` via `src/gallery.py`.

Instagram publishing (`publish` subcommand, `src/publisher.py`,
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
text sits next to a rendered PNG in the gallery is exactly what should go in
the Instagram post if you copy it over by hand.

## Numbering and palette rotation

For the *n*th post (0-indexed):

```
chapter       = n // 30 + 1
verse         = n % 30 + 1
palette_index = n % 4
```

Verified against the brand spec's own example: post 14 (n=13) → chapter 1,
verse 14, palette_index 1 (Forest Tablet) — exactly `nim. 1.14`.
