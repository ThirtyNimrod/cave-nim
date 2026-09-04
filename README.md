# nim.

Daily caveman-stoic proverb cards for Instagram — an automated content pipeline
that writes a short verse, matches it to a hand-drawn line-art icon, and
renders a 1080x1350 card.

## How it works

1. **Generate** (`python main.py generate --count 7`): asks Gemini for a
   3-line proverb plus a matching icon per post, renders each card with
   Playwright, and appends each one to `database/canon.json`. Fully manual
   and local — no GitHub Actions, no cron. A weekly batch of ~7 works well.
2. **Browse**: `python main.py list` for a quick text index, or
   `python main.py gallery` to write `gallery.html` — open it in a browser,
   fully offline, reads only `database/canon.json` and `assets/rendered/`.
3. **Post**: pick a card and post it to Instagram yourself.

There's no automated Instagram publishing right now — see
[docs/current-implementation-plan.md](docs/current-implementation-plan.md)
for why, and [docs/future-enhancements.md](docs/future-enhancements.md) for
what would need to happen to bring it back.

## Current status

Chapter 1 (`nim. 1.1` through `nim. 1.30`) is already written and rendered —
see `database/canon.json` and `assets/rendered/`. Post `nim. 1.31` onward is
generated on demand with `python main.py generate --count N` once you add a
`GEMINI_API_KEY` (see below).

Cards currently render with a fallback system font — `assets/fonts/Gaegu-Regular.ttf`
hasn't been fetched yet. The 18 doodle icons in `assets/doodles/` are
original, hand-authored SVGs, not a vendored library.

Instagram posting is manual for now (account: `nim.grug`) — there's no Meta
Graph API integration on `main`, since that requires a Facebook Page which
isn't available yet. The version with automated publishing is preserved on
the `meta-idea` branch.

## Numbering & palettes

Posts are numbered `chapter.verse` (e.g. `nim. 1.14`), rolling to a new chapter
every 30 posts. Each post cycles through 4 fixed palettes in order (Obsidian
Chrome, Forest Tablet, Terracotta Sunset, Colonial Cobalt) — see
[`src/config.py`](src/config.py).

## Local setup

```bash
python -m venv .venv
.venv/Scripts/activate   # or source .venv/bin/activate on macOS/Linux
pip install -r requirements.txt
playwright install chromium
cp .env.example .env     # fill in your own key, see below
```

Setting up on a machine that's never seen this repo? See
[docs/new-system-setup.md](docs/new-system-setup.md) for the full
clone-to-first-gallery walkthrough.

### Try it with no API keys at all

```bash
python main.py generate --mock
```

Renders a placeholder card to `assets/rendered/_preview.png` using canned text
and a trivial icon — doesn't call Gemini, doesn't touch `canon.json`. Use this
to iterate on `templates/card_template.html` layout/fonts.

### Real generation (post 1.31 onward)

```bash
python main.py generate --count 7   # weekly batch, or any N you like
python main.py list                 # text index of every post so far
python main.py gallery              # writes gallery.html, open in a browser
```

## Required secrets

| Variable | Where it's used | How to get it |
|---|---|---|
| `GEMINI_API_KEY` | `generate` | [Google AI Studio](https://aistudio.google.com/apikey) |

Set this locally in `.env` (gitignored). There's no CI on this branch, so
there's nothing to add as a GitHub Actions secret.

## Icon library

`assets/doodles/manifest.json` maps icon slugs to SVG files and search tags;
Gemini picks one slug per post from this list. All 18 are original single-
stroke SVGs authored for this project (fire, water, moon, mountain, storm,
spear, footprint, star, tree, stone, wind, bone, shield, pawprint, thorn,
cave, seed, snow) — add more the same way as the verse vocabulary grows.

## Documentation

Deeper reference docs live in [`docs/`](docs/README.md): credential setup
for Gemini, new-system setup, the full architecture, current implementation
status, the original brand idea, planned future enhancements, and an
AI-use disclosure.

## Known limitations

- Committing a PNG per day grows repo history over time (~100-300MB/year) —
  fine at low volume, worth revisiting later (Git LFS or archival) if needed.
