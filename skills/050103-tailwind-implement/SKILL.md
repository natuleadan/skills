---
name: 050103-tailwind-implement
description: "Tailwind CSS v4 CSS-first configuration and shadcn/ui component composition — CVA factories, styling rules, forms, icons, Base vs Radix API."
license: MIT
---

# Tailwind CSS v4 & shadcn/ui Composition

Implementation layer of frontend design — translating design tokens into `@theme` blocks and composing shadcn/components following the component system rules.

## References

| Topic | File |
|---|---|
| Tailwind v4: `@theme`, `@custom-variant`, `@utility`, `@starting-style`, container queries, CVA patterns, v3→v4 migration | [references/tailwind-v4.md](references/tailwind-v4.md) |
| shadcn styling: semantic colors, gap-*, size-*, truncate, cn(), no dark: overrides, no z-index on overlays | [references/shadcn-styling.md](references/shadcn-styling.md) |
| shadcn forms: FieldGroup/Field, InputGroup, ToggleGroup, FieldSet, validation states | [references/shadcn-forms.md](references/shadcn-forms.md) |
| shadcn composition: Card, Empty, Alert, sonner toast, Dialog/Sheet/Drawer Title, Button loading, Tabs, Avatar, Separator, Skeleton, Badge | [references/shadcn-composition.md](references/shadcn-composition.md) |
| shadcn icons: data-icon, no sizing, pass as objects, stroke consistency, no emoji | [references/shadcn-icons.md](references/shadcn-icons.md) |
| Base vs Radix API: asChild vs render, Select, Accordion, Slider, ToggleGroup differences | [references/shadcn-base-radix.md](references/shadcn-base-radix.md) |
| Data Table with TanStack: column defs, sorting, filtering, pagination, row selection, visibility | [references/shadcn-data-table.md](references/shadcn-data-table.md) |
| Charts with Recharts: ChartContainer, bar/line/area/pie/radial, tooltip, legend | [references/shadcn-charts.md](references/shadcn-charts.md) |

## When to Use

| Trigger | Use |
|---|---|
| Setting up Tailwind v4 theme | [references/tailwind-v4.md](references/tailwind-v4.md) |
| Building form UI | [references/shadcn-forms.md](references/shadcn-forms.md) |
| Composing Card/Dialog/Sheet | [references/shadcn-composition.md](references/shadcn-composition.md) |
| Placing icons in buttons | [references/shadcn-icons.md](references/shadcn-icons.md) |
| Deciding asChild vs render | [references/shadcn-base-radix.md](references/shadcn-base-radix.md) |
| Using semantic colors correctly | [references/shadcn-styling.md](references/shadcn-styling.md) |
| Building a data table with TanStack | [references/shadcn-data-table.md](references/shadcn-data-table.md) |
| Building charts with Recharts | [references/shadcn-charts.md](references/shadcn-charts.md) |
