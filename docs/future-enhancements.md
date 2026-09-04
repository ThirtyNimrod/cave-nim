# Future enhancements

Deliberately not built yet — none of these block the current pipeline.

## Content and icons

- Expand `assets/doodles/` as verse vocabulary grows beyond what the current
  18 icons cover well.
- Build the "Gemini Gem" reply engine from [idea.md](idea.md) as a separate,
  manual tool for in-character comment replies.

## Operations

- **Repo size**: committing a PNG per day adds roughly 100-300MB/year to git
  history. Fine at one post/day; revisit with Git LFS or periodic archival
  if it becomes a problem.
- **Token expiry alerts**: `META_ACCESS_TOKEN` expires every ~60 days with
  no warning — a scheduled workflow that calls the Graph API's
  `debug_token` endpoint and opens an issue when the token is close to
  expiring would remove the surprise-failure risk.
- **Generate failure alerts**: if `generate_daily.yml` fails (Gemini error,
  Playwright crash), nothing currently notifies you beyond the Actions tab
  going red. A failure notification (email, Slack, etc.) would close that
  gap.
- **Backlog visibility**: `python main.py status` covers this locally —
  worth wiring into a workflow that comments on a tracking issue, or
  similar, if the pending queue tends to grow unreviewed.

## Font

- `assets/fonts/Gaegu-Regular.ttf` likely ships full Hangul coverage though
  only Latin glyphs are used here — subsetting with `fonttools`/`pyftsubset`
  would shrink it if the full file size ever matters.

## Review workflow

- Browsing raw PNGs in `assets/rendered/` works but isn't a great review
  experience. A tiny static gallery page (or a GitHub Pages view over
  `canon.json` plus images) would make reviewing pending posts faster.

## Reach

- Reuse the same rendered cards on other platforms (Threads, X) once the
  Instagram pipeline is proven out.
- Pull Instagram Insights (engagement per post) back into `canon.json` to
  see which verses and icons resonate, informing future verse themes.
