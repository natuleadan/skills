# Variant Card Pattern

Building component demo/showcase pages with consistent layout and organization.

## Page Structure

- Outer container: `<div className="flex flex-col gap-6">`
- Page header: `<h2 className="mb-2 font-heading text-lg font-semibold">` + `<p className="text-sm text-muted-foreground">`
- All demo sections start with `"use client"`

## Mother Card Pattern

Each component variant group uses a **mother card**:

```tsx
<Card>
  <CardHeader>
    <CardTitle>Component Name</CardTitle>
    <CardDescription>Brief variant description.</CardDescription>
  </CardHeader>
  <CardContent>
    {/* Variant examples */}
  </CardContent>
</Card>
```

## Organizing Variants

- Simple variants (buttons, badges): use `flex flex-wrap gap-2` inside CardContent
- Complex variants with state: wrap each in a sub-`Card size="sm"` inside the mother card
- Grid layouts: use `grid gap-6 md:grid-cols-N`
- Cards must always include `CardDescription` for context

## Description Text

- `CardDescription` uses `text-xs/relaxed text-muted-foreground` by default
- Inline item labels: `text-xs text-muted-foreground`
- Avoid `text-sm` for secondary text

## Button Triggers

- Standard action trigger: `variant="outline" size="sm"`
- Destructive actions: `variant="destructive"`
- Hover/popover triggers: `variant="link"` or `variant="ghost" size="icon"`

## Anti-Patterns

- Never use native `<button>` — always use the `Button` component
- Never leave `CardDescription` empty — every card needs context
- Avoid mixing `gap-2`, `gap-3`, `gap-4` within the same card
- Don't duplicate component demos across pages — each component has ONE canonical home
