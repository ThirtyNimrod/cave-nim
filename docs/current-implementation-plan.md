# Current implementation plan

This describes what actually exists in this repo today, and where it
deliberately differs from the original [idea](idea.md). For the "how it's
built" view, see [architecture.md](architecture.md).

## What's built

- Full pipeline code: `src/config.py`, `canon.py`, `generator.py`,
  `illustrator.py`, `compositor.py`, `publisher.py`, `main.py`
  (`generate` / `publish` / `status`).
- `templates/card_template.html` — the 1080x1350 card layout.
- 18 original, hand-authored doodle icons in `assets/doodles/` (fire, water,
  moon, mountain, storm, spear, footprint, star, tree, stone, wind, bone,
  shield, pawprint, thorn, cave, seed, snow) plus `assets/brand/sun.svg` for
  the fixed top-bar icon.
- Two GitHub Actions workflows: `generate_daily.yml` (cron 14:00 UTC +
  manual) and `publish.yml` (manual `workflow_dispatch` only).
- Chapter 1 complete: `nim. 1.1` through `nim. 1.30`, written and rendered,
  all `pending_review` in `database/canon.json`. Verse `1.14` intentionally
  reuses the exact text and palette from the original brand blueprint's own
  schema example.
- `README.md`, `.env.example`, and `.gitignore` set up for this project.

## What's deliberately different from the original idea

1. **No AI image generation.** The original concept called for an image
   model (Imagen 3 / DALL-E 3) to generate a bespoke doodle per post. This
   project uses a fixed set of hand-authored icons instead — see
   [disclosure.md](disclosure.md) for why, and
   [architecture.md](architecture.md) for how icon selection and recoloring
   work without one.
2. **No raster image post-processing.** Because icons are vector SVG from
   the start, palette recoloring happens via a CSS variable at render time.
   Pillow was dropped from the dependencies entirely.
3. **Publishing requires manual approval.** The original concept auto-posted
   to Instagram straight from the daily cron with no review step. This
   project splits generation and publishing into two separate workflows —
   `publish.yml` only ever runs when manually triggered from the Actions
   tab.

## What's pending (not code — things only you can do)

- **Gaegu font** — `assets/fonts/Gaegu-Regular.ttf` isn't in the repo yet;
  cards currently render with a system fallback font. In progress.
- **`GEMINI_API_KEY`** — needed for any post after `1.30`. See
  [gemini-api-key-setup.md](gemini-api-key-setup.md).
- **`META_ACCESS_TOKEN` / `IG_USER_ID`** — needed before anything can
  actually publish. See
  [meta-access-token-setup.md](meta-access-token-setup.md).
- **GitHub repo secrets** — none are set yet.
- **Nothing has been committed or pushed yet.** Everything above exists
  only in the local working tree.
- **Neither workflow has run in CI yet** — recommend a manual
  `workflow_dispatch` test of `generate_daily.yml` before trusting the cron
  schedule, and a `publish.yml --dry-run` before a real first post.

## Not built

- The "Gemini Gem" in-character reply engine from the original idea (a
  manual tool for replying to comments, not part of the automated
  pipeline). See [future-enhancements.md](future-enhancements.md).
