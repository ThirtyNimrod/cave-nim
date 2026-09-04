# Current implementation plan

This describes what actually exists in this repo today, and where it
deliberately differs from the original [idea](idea.md). For the "how it's
built" view, see [architecture.md](architecture.md).

## What's built

- Full generation pipeline: `src/config.py`, `canon.py`, `generator.py`,
  `illustrator.py`, `compositor.py`, and `main.py generate`.
- `templates/card_template.html` — the 1080x1350 card layout.
- 18 original, hand-authored doodle icons in `assets/doodles/` (fire, water,
  moon, mountain, storm, spear, footprint, star, tree, stone, wind, bone,
  shield, pawprint, thorn, cave, seed, snow) plus `assets/brand/sun.svg` for
  the fixed top-bar icon.
- `generate_daily.yml` — a GitHub Actions workflow that generates, renders,
  and commits one card per day (cron 14:00 UTC, plus manual dispatch).
- Chapter 1 complete: `nim. 1.1` through `nim. 1.30`, written and rendered in
  `database/canon.json` and `assets/rendered/`. Verse `1.14` intentionally
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
3. **No automated Instagram publishing.** An earlier version of this
   pipeline (`src/publisher.py`, `.github/workflows/publish.yml`, the
   `publish`/`status` CLI subcommands) called the Meta Graph API to post
   directly to Instagram behind a manual-approval gate. That required a
   Facebook Page linked to an Instagram Business/Creator account, which
   isn't available yet — so the entire Meta posting path was removed from
   `main` and `claude`. It's preserved as-is on the `meta-idea` branch for
   whenever a Page becomes available. Posting is manual in the meantime,
   via the `nim.grug` Instagram account.

## What's pending (not code — things only you can do)

- **Gaegu font** — `assets/fonts/Gaegu-Regular.ttf` isn't in the repo yet;
  cards currently render with a system fallback font. In progress.
- **`GEMINI_API_KEY`** — needed for any post after `1.30`. See
  [gemini-api-key-setup.md](gemini-api-key-setup.md).
- **GitHub repo secrets** — `GEMINI_API_KEY` isn't set as a repo secret yet.
- **Nothing has been pushed to GitHub yet.** `main`, `claude`, and
  `meta-idea` all exist locally; none are on the remote yet.
- **`generate_daily.yml` hasn't run in CI yet** — recommend a manual
  `workflow_dispatch` test before trusting the cron schedule.
- **A better Instagram username and bio.** `nim.grug` is a placeholder —
  `nim`, `nim.say`, and `nim_says` were all already taken.

## Not built

- The "Gemini Gem" in-character reply engine from the original idea (a
  manual tool for replying to comments, not part of the automated
  pipeline). See [future-enhancements.md](future-enhancements.md).
- Automated Instagram publishing on `main`/`claude` (it exists on
  `meta-idea`, just not merged in — see above).
