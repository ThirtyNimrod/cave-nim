# Future enhancements

Deliberately not built yet — none of these block the current pipeline.

## Instagram publishing

- Revive the Meta Graph API integration once a Facebook Page is available
  to link to an Instagram Business/Creator account — the working
  implementation (`src/publisher.py`, `publish.yml`, the manual-approval
  gate) is preserved on the `meta-idea` branch, not deleted.
- Once revived: a scheduled check against the Graph API's `debug_token`
  endpoint that opens an issue when `META_ACCESS_TOKEN` is close to its
  ~60-day expiry, so it doesn't fail silently.
- A settled username and bio for the `nim.grug` account.

## Content and icons

- Expand `assets/doodles/` as verse vocabulary grows beyond what the current
  18 icons cover well.
- Build the "Gemini Gem" reply engine from [idea.md](idea.md) as a separate,
  manual tool for in-character comment replies.

## Automation

- This branch is intentionally offline/manual right now (see
  [current-implementation-plan.md](current-implementation-plan.md)).
  GitHub Actions cron generation could be revived later if a hands-off
  cadence becomes preferable to manual weekly batches — the earlier
  `generate_daily.yml` design is documented in `idea.md`'s pipeline concept.

## Operations

- **Repo size**: committing a PNG per batch adds up over time. Fine at low
  volume; revisit with Git LFS or periodic archival if it becomes a
  problem.

## Font

- `assets/fonts/Gaegu-Regular.ttf` likely ships full Hangul coverage though
  only Latin glyphs are used here — subsetting with `fonttools`/`pyftsubset`
  would shrink it if the full file size ever matters.

## Review workflow

- `main.py gallery` covers basic offline browsing. Could grow filters (by
  icon, by chapter) or a "copy caption" button if the post count gets large.

## Reach

- Reuse the same rendered cards on other platforms (Threads, X) once a
  posting workflow (manual or automated) is proven out.
- Pull Instagram Insights (engagement per post) back into `canon.json` to
  see which verses and icons resonate, informing future verse themes.
