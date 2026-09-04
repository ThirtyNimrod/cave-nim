# Gemini API key setup

`GEMINI_API_KEY` powers `src/generator.py` — the one Gemini call per post that
writes the 3-line proverb and picks a matching icon slug from
`assets/doodles/manifest.json`. Nothing else in the pipeline calls Gemini.

## Generate a key

1. Go to [Google AI Studio](https://aistudio.google.com/apikey).
2. Sign in with a Google account.
3. Click **Create API key**, and choose or create a Google Cloud project when prompted.
4. Copy the generated key — Google only shows it in full once.

This is a personal API key billed to whatever project you attach it to.
Google's free tier covers light, single-account usage like one generation
call a day, but check the current quota and pricing on the AI Studio
dashboard before relying on it — limits and free-tier terms change over time.

## Where it goes

**Local development** — copy the template and fill it in:

```bash
cp .env.example .env
```

Then edit `.env`:

```
GEMINI_API_KEY=your-key-here
```

`src/config.py` loads this automatically via `python-dotenv`. `.env` is
already in `.gitignore` — it will never be committed.

**GitHub Actions** — the `generate_daily.yml` workflow reads it from a repo
secret, not from `.env` (there is no `.env` file in CI):

1. On GitHub, go to the repo's **Settings → Secrets and variables → Actions**.
2. Click **New repository secret**.
3. Name: `GEMINI_API_KEY`. Value: the key you copied above.

## Test it

**Without a key at all** — confirms the rendering pipeline works, independent of Gemini:

```bash
python main.py generate --mock
```

**With a real key** — isolate credential problems from the rest of the pipeline:

```bash
.venv/Scripts/python.exe -c "from src import config; from google import genai; c = genai.Client(api_key=config.GEMINI_API_KEY); print(c.models.generate_content(model=config.GEMINI_MODEL, contents='Say hello in one word').text)"
```

This reads the key from `.env` via `config.py`, so it never appears in your
shell history. If this prints a one-word response, both the key and the
configured model name are valid.

**Full pipeline test**:

```bash
python main.py generate
```

On success this prints the new `chapter.verse`, the generated lines, and
appends a `pending_review` entry to `database/canon.json`. On failure, the
error message from `generator.GenerationError` says exactly what went wrong
(missing key, malformed response, or the underlying Gemini error after
retries are exhausted).
