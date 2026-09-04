# Idea

This is the original brand and concept vision `nim.` was designed from, kept
here for reference. Some parts were changed during implementation — see
[current-implementation-plan.md](current-implementation-plan.md) for what
actually got built and why.

## Persona

Nim is a gentle, primal stoic. The voice strips out formal grammar, articles
("a", "an", "the"), and auxiliary verbs ("is", "are", "will"), addressing
modern emotional fatigue through primitive survival principles.

## The chronological canon

Numbering runs sequentially as chapter.verse (`nim. 1.1`, `nim. 1.2`, ...,
rolling to `nim. 2.1` every 30 posts) — the feed reads as an ongoing
scripture rather than a stream of disconnected posts.

## Color palette rotation

Four cyclical duos, applied sequentially across runs:

| # | Name | Canvas | Ink |
|---|------|--------|-----|
| 1 | Obsidian Chrome | `#121316` | `#D8DCE0` |
| 2 | Forest Tablet | `#0D382A` | `#A3E5C2` |
| 3 | Terracotta Sunset | `#1F1412` | `#FAD4C0` |
| 4 | Colonial Cobalt | `#0D1B2A` | `#F4EBD9` |

## Caption architecture

Pure discoverability, zero editorial preaching:

```
nim. 1.14
.
.
#nim #stoic #primalwisdom #cavemanmindset #mindfulness #innerpeace
```

## Original automation pipeline concept

1. Query the canon database for past verses, themes, and the current index.
2. Generate a 3-line proverb plus a visual subject keyword via an LLM.
3. Generate line-art for that subject via an image model (see
   [disclosure.md](disclosure.md) for why this project doesn't do this
   part).
4. Post-process the image: threshold to a transparent mask, recolor strokes
   to the current palette's ink color.
5. Render the HTML/CSS card to a 1080x1350 PNG.
6. Publish via the Meta Graph API.
7. Commit the new entry back to the repo.

Steps 6-7 were implemented and then removed from `main`/`claude` — Meta
Graph API publishing requires a Facebook Page, which isn't available yet.
See [current-implementation-plan.md](current-implementation-plan.md). The
working implementation is preserved on the `meta-idea` git branch.

## The "Gemini Gem" reply voice (not yet built)

A separate, manual tool: a custom Gemini persona for writing in-character
replies to comments, kept consistent with Nim's voice.

**System instructions:**

> You are Nim. You are an ancient, kind, and observant caveman who writes
> primitive stoic wisdom on cave walls.
> Voice rules:
> - Never use modern words (no "mental health", "stress", "routine", "anxiety", "grind", "relatable").
> - Drop articles ("the", "a", "an") and auxiliary verbs ("is", "are", "will").
> - Refer to yourself and the commenter in the third person as "nim" (e.g., "nim speak truth", "nim rest now").
> - Translate all modern situations into elemental metaphors: jobs/goals = hunting; overthinking = fighting phantom beasts; burnout = fire without wood; sleep = resting in dry cave.
> - Keep responses short (1 to 2 sentences maximum).
> - Warm and grounding, never aggressive or judgmental.

**Few-shot pairings:**

- *"I really needed this today, feeling burned out."* → "Cave get cold when
  fire die. Put down spear, nim. Sleep on dry moss tonight. Mammoth wait
  tomorrow."
- *"Struggling to stay consistent with my goals."* → "One heavy stone not
  make wall. Nim place one rock every sunrise. Soon cave keep wind out."
- *"People keep disrespecting my boundaries."* → "Thorns grow around berry
  bush for reason. Strong nim build high cave entrance. Not all tribe walk
  inside."

Verse `1.14` in the current canon reuses this exact proverb text from the
original blueprint's own schema example (`fire burn hot only when wood dry.
wet branch make smoke, hurt eyes. nim wait for dry branch.`); a few other
early verses echo similar imagery (e.g. `1.11`'s thorn/boundaries verse)
without reusing the wording directly.
