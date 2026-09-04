# AI use disclosure

This project uses generative AI for **text only**.

`src/generator.py` calls Google's Gemini API to write each post's 3-line
proverb and to choose which existing icon best matches it. That is the only
place in this pipeline where a generative model produces content that ends
up in a published post.

**This project does not use AI-generated imagery**, by design. The visual
side of every card is produced by:

1. A library of line-art icons (`assets/doodles/*.svg`) drawn from three
   sources, none of them a generative model:
   - Hand-authored originals for themes with no good match elsewhere
     (mountain, spear, footprint, stone, bone, thorn, cave, seed).
   - A commercially-licensed doodle icon pack purchased from
     [khushmeen.com](https://khushmeen.com/icons.html) (fire, water, moon,
     earth, star, shield, snow, wind, storm, plus the top-bar sun icon).
     Source files are kept locally under `ref/` (gitignored, not
     redistributed) under the project owner's purchased license.
   - One icon (pawprint) from [Reicon](https://reicon.dev), MIT licensed
     (github.com/dqev/reicon).
2. Deterministic code — Playwright rendering plain HTML/CSS
   (`templates/card_template.html`) — to lay out text, color, and the
   chosen icon into the final image. See [architecture.md](architecture.md)
   for how this works.

No pixel in a published card comes from an image-generation model. When the
icon library needs to grow, new icons should be added the same way: hand-
authored, or sourced from a properly licensed set — never generated.
