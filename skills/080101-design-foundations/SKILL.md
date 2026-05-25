---
name: 080101-design-foundations
description: "Design foundations: color theory, token hierarchy, brand vs product registers, theming decisions. OKLCH color space, color strategies, absolute bans, slop test."
---

# Design Foundations

Foundational design decisions: color, tokens, and the register (brand vs product) that determines how design rules apply. Use this before making any color or theming choice.

## References

| Topic | File |
|---|---|
| Color strategies: Restrained, Committed, Full palette, Drenched | [references/color-strategies.md](references/color-strategies.md) |
| Design token hierarchy: Brand → Semantic → Component | [references/token-hierarchy.md](references/token-hierarchy.md) |
| Brand vs Product register differences, slop tests, shared laws | [references/brand-product-register.md](references/brand-product-register.md) |

## Core Rules

- **Scene Sentence**: Write one sentence of physical context (who, where, ambient light, mood) to decide dark vs light. If the sentence doesn't force the answer, it's not concrete enough.
- **Color strategy**: Pick from Restrained (≤10% accent), Committed (30-60% saturated), Full palette (3-4 roles), Drenched (surface IS the color).
- **OKLCH**: Use OKLCH, reduce chroma at lightness extremes, never `#000` or `#fff`, tint neutrals toward brand hue (chroma 0.005-0.01).
- **Absolute bans**: No gradient text, side-stripe borders, glassmorphism as default, hero-metric template, identical card grids, modal as first thought, nested cards.
- **Slop test (two altitudes)**: First-order — would someone guess theme from category alone? Second-order — would someone guess aesthetic from category-plus-anti-references? If yes, rework.

## When to Use

- Choosing color scheme for a new project
- Defining design tokens and CSS variables
- Deciding dark vs light mode
- Designing marketing/brand surfaces vs product UI
- Reviewing UI for "AI-generated" look
