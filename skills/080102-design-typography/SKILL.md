---
name: 080102-design-typography
description: "Typography and layout design: font selection methodology, modular type scales, 4/8pt spacing systems, grid theory, visual hierarchy for brand and product UI."
license: MIT
---

# Typography, Spacing & Layout

Typography, spacing, and layout decisions for brand and product interfaces. Covers font selection, type scale engineering, spacing systems, grid theory, and visual hierarchy.

## References

| Topic | File |
|---|---|
| Font selection procedure, reflex-reject list (22 fonts), pairing strategies, aesthetic lane rejection | [references/font-selection.md](references/font-selection.md) |
| Modular type scale, fluid `clamp()` formulas, fixed rem scale, weight hierarchy, line-height | [references/type-scale.md](references/type-scale.md) |
| 4/8pt spacing system, semantic tokens, density guidelines, rhythm through contrast | [references/spacing-systems.md](references/spacing-systems.md) |
| Grid theory, responsive breakpoints, squint test, card heuristics, container strategies | [references/grid-layout.md](references/grid-layout.md) |

## Core Rules

- **Font selection procedure**: (1) Write 3 concrete brand-voice words, (2) List 3 reflex fonts — reject them, (3) Browse real catalog with the 3 words, (4) Cross-check final vs reflex.
- **Reflex-reject fonts**: Fraunces, Newsreader, Lora, Crimson, Playfair Display, Cormorant, Syne, IBM Plex*, Space*, Inter, DM Sans, Outfit, Plus Jakarta Sans, Instrument*. Training-data defaults — look further.
- **Type scale**: ≥1.25 ratio between steps. Brand uses fluid `clamp()`. Product uses fixed rem (1.125-1.2 ratio).
- **Line length**: 35-60ch mobile, 60-75ch desktop.
- **Font pairing**: One committed family > timid two-family pair.
- **Spacing**: 4/8pt system. Vary spacing for rhythm — same padding everywhere is monotony.
- **Layout**: Cards are the lazy answer. Nested cards are always wrong. Don't wrap everything in a container.

## When to Use

- Selecting fonts for a new project
- Building a type scale
- Defining spacing tokens
- Designing responsive layouts
- Reviewing hierarchy and rhythm
