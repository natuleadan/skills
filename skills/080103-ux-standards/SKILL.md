---
name: 080103-ux-standards
description: "UX standards: WCAG accessibility, touch interaction, form UX, navigation, UX writing, cognitive load. Heuristic evaluation and critique methodology."
---

# UX Standards

Production-grade UX standards for web and mobile: accessibility, interaction, form design, navigation architecture, copy, and cognitive load.

## References

| Topic | File |
|---|---|
| WCAG accessibility: contrast 4.5:1, focus, keyboard, screen reader, ARIA, reduced motion | [references/accessibility.md](references/accessibility.md) |
| Touch interaction: targets 44×44pt, gestures, haptics, safe areas, platform standards | [references/touch-interaction.md](references/touch-interaction.md) |
| Form UX: labels, validation, error recovery, progressive disclosure, keyboard, autofill | [references/form-ux.md](references/form-ux.md) |
| Navigation: bottom nav, sidebar, breadcrumbs, back stack, deep linking, adaptive patterns | [references/navigation-patterns.md](references/navigation-patterns.md) |
| UX writing: error messages, empty states, CTAs, confirmation, tone | [references/ux-writing.md](references/ux-writing.md) |
| Cognitive load: information density, chunking, progressive disclosure, decision fatigue | [references/cognitive-load.md](references/cognitive-load.md) |

## Core Rules

- **Accessibility is critical**: Color contrast ≥4.5:1, visible focus rings, keyboard nav, aria-labels, skip links, heading hierarchy never skips levels. Color is never the only indicator.
- **Touch targets**: Minimum 44×44pt (Apple) / 48×48dp (Material). 8px minimum gap between targets. Don't rely on hover alone.
- **Forms**: Visible labels (not placeholder-only), errors below the field, progressive disclosure, validate on blur, input types trigger correct keyboard.
- **Navigation**: Bottom nav ≤5 items, labels + icons. Back must preserve scroll/state. All screens reachable via deep link.
- **UX writing**: Every word earns its place. Errors state cause + how to fix. Empty states teach the interface.

## When to Use

| Trigger | Use |
|---|---|
| Designing forms or inputs | [references/form-ux.md](references/form-ux.md) |
| Building navigation structure | [references/navigation-patterns.md](references/navigation-patterns.md) |
| Reviewing accessibility | [references/accessibility.md](references/accessibility.md) |
| Writing UI copy | [references/ux-writing.md](references/ux-writing.md) |
| Evaluating information density | [references/cognitive-load.md](references/cognitive-load.md) |
| Mobile/touch design review | [references/touch-interaction.md](references/touch-interaction.md) |
