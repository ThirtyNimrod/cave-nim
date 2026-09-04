# Setting up on a new system

Steps to get `nim.` running from scratch on a machine that has never seen
this repo — a new laptop, a fresh VM, a teammate's machine.

## 1. Clone

```bash
git clone <repo-url>
cd cave-nim
git checkout main   # or meta-idea for the version with Instagram publishing
```

## 2. Python

Needs Python 3.10+ (built and tested on 3.14). Check what you have:

```bash
python --version
```

## 3. Virtual env and dependencies

```bash
python -m venv .venv
.venv/Scripts/activate      # Windows
source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
playwright install chromium
```

## 4. Secrets

```bash
cp .env.example .env
```

Fill in `GEMINI_API_KEY` — see
[gemini-api-key-setup.md](gemini-api-key-setup.md). Nothing else is
required; there's no Meta credential on `main`/`claude` anymore (see
[current-implementation-plan.md](current-implementation-plan.md)).

## 5. Font (optional, cosmetic only)

`assets/fonts/Gaegu-Regular.ttf` isn't committed yet. Without it, cards
render with a system fallback font — everything still works. Drop the real
Gaegu font (Google Fonts, open license) into that exact path for the
intended handwritten look.

## 6. Verify the pipeline works, no API key needed

```bash
python main.py generate --mock   # renders assets/rendered/_preview.png
python main.py list              # see the 30 seeded chapter-1 posts
python main.py gallery           # writes gallery.html
```

Open `gallery.html` directly in a browser (double-click it, or `start
gallery.html` / `open gallery.html` / `xdg-open gallery.html`). It only
reads local files — `database/canon.json` and `assets/rendered/` — no
server needed.

## 7. Generate for real

```bash
python main.py generate --count 7   # a weekly batch, needs GEMINI_API_KEY
```

There is no cron job or CI on this branch — generation is a manual, local
command you run whenever you want new posts, then review with `list` or
`gallery`, then post to Instagram yourself.
