# Current implementation plan

This describes what actually exists in this repo today, and where it
deliberately differs from the original [idea](idea.md). For the "how it's
built" view, see [architecture.md](architecture.md).

## What's built

- Full generation pipeline: `src/config.py`, `canon.py`, `generator.py`,
  `illustrator.py`, `compositor.py`, `gallery.py`, and `main.py`
  (`generate` / `list` / `gallery`).
- `templates/card_template.html` — the 1080x1350 card layout.
- 19 doodle icons in `assets/doodles/` (fire, water, moon, mountain, storm,
  spear, footprint, star, tree, stone, wind, bone, shield, pawprint, thorn,
  cave, seed, snow, earth), mixing hand-authored originals with a purchased
  icon pack and one MIT-licensed icon — see [disclosure.md](disclosure.md)
  for the full sourcing breakdown. `assets/brand/sun.svg` (top-bar icon) is
  also from the purchased pack.
- 6 three-stop gradient palettes and a font pool (Nunito/Poppins, loaded
  live via Google Fonts), both picked at random per post rather than
  rotated — see [idea.md](idea.md) for the original gradient/font plan this
  replaced the flat 4-palette rotation with.
- `main.py generate --count N` — batch generation for a manual, local,
  weekly-ish cadence rather than a daily automated one.
- `main.py list` and `main.py gallery` — two offline ways to browse
  everything generated so far, plus reading `database/canon.json` directly.
- Chapter 1 complete: `nim. 1.1` through `nim. 1.30`, written and rendered in
  `database/canon.json` and `assets/rendered/`. Verse `1.14` intentionally
  reuses the exact text and palette from the original brand blueprint's own
  schema example.
- `README.md`, `.env.example`, and `.gitignore` set up for this project.

## What's deliberately different from the original idea

1. **No AI image generation.** The original concept called for an image
   model (Imagen 3 / DALL-E 3) to generate a bespoke doodle per post. This
   project uses a fixed icon library instead (hand-authored plus two
   properly-licensed sources) — see [disclosure.md](disclosure.md) for why,
   and [architecture.md](architecture.md) for how icon selection and
   recoloring work without one.
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
4. **No GitHub Actions at all.** The original concept ran generation on a
   daily cron in CI. This project now runs entirely offline and locally:
   `python main.py generate --count 7` run by hand, roughly weekly, gives
   better batch variety than a rigid daily schedule and needs no CI secrets,
   no server, nothing but a local `.env`.

## What's pending (not code — things only you can do)

- **`GEMINI_API_KEY`** — needed for any post after `1.30`. See
  [gemini-api-key-setup.md](gemini-api-key-setup.md).
- **Nothing has been pushed to GitHub yet.** `main`, `claude`, and
  `meta-idea` all exist locally; none are on the remote yet.
- **A better Instagram username and bio.** `nim.grug` is a placeholder —
  `nim`, `nim.say`, and `nim_says` were all already taken.

## Not built

- The "Gemini Gem" in-character reply engine from the original idea (a
  manual tool for replying to comments, not part of the automated
  pipeline). See [future-enhancements.md](future-enhancements.md).
- Automated Instagram publishing on `main`/`claude` (it exists on
  `meta-idea`, just not merged in — see above).
