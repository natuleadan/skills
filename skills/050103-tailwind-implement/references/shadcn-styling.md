# shadcn/ui Styling Rules

## 1. Semantic Colors Only

Always use shadcn's semantic color tokens. Never use raw Tailwind color values.

```tsx
/* ❌ Incorrect — raw Tailwind colors */
<button className="bg-blue-500 text-white">Submit</button>
<div className="text-red-600 font-semibold">Error</div>
<div className="bg-gray-100 text-gray-900 dark:bg-gray-900 dark:text-gray-50">

/* ✅ Correct — semantic tokens */
<Button>Submit</Button>
<Badge variant="destructive">Error</Badge>
<div className="bg-muted text-foreground">
```

Available semantic tokens:

| Token | Usage | Light | Dark |
|---|---|---|---|
| `bg-background` | Page background | white | near-black |
| `text-foreground` | Primary text | near-black | near-white |
| `bg-muted` | Subtle backgrounds | light gray | dark gray |
| `text-muted-foreground` | Secondary text | medium gray | light gray |
| `bg-primary` | Primary action | brand color | brand color |
| `text-primary-foreground` | Text on primary | white | near-black |
| `bg-secondary` | Secondary action | light gray | dark gray |
| `text-secondary-foreground` | Text on secondary | near-black | near-white |
| `bg-destructive` | Danger | red | red |
| `text-destructive-foreground` | Text on danger | white | white |
| `border-border` | Borders | light gray | dark gray |
| `border-input` | Input borders | light gray | dark gray |
| `ring-ring` | Focus rings | brand color | brand color |

## 2. Use Built-in Variants First

Check if a component has a variant before adding custom classes.

```tsx
/* ❌ Incorrect — custom classes when variants exist */
<button className="bg-red-500 text-white px-4 py-2 rounded-md">

/* ✅ Correct — use variant */
<Button variant="destructive">

/* ❌ Incorrect — custom styling when variant exists */
<span className="text-xs font-medium bg-purple-100 text-purple-700 px-2 py-0.5 rounded-full">

/* ✅ Correct — use variant or Badge */
<Badge variant="secondary">Label</Badge>

/* ❌ Incorrect — custom card */
<div className="rounded-lg border bg-card p-6 shadow-sm">
  <h3 className="text-lg font-semibold">Title</h3>
  <p className="text-sm text-muted-foreground">Description</p>
</div>

/* ✅ Correct — use Card components */
<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
  </CardHeader>
  <CardContent>
    <p className="text-sm text-muted-foreground">Description</p>
  </CardContent>
</Card>
```

## 3. className for Layout Only

Use `className` for positioning and layout. Colors, typography, and spacing values belong in component variants or semantic tokens.

```tsx
/* ❌ Incorrect — className used for styling */
<div className="text-primary font-bold text-lg bg-muted p-4 rounded-md">

/* ✅ Correct — minimal layout className, components handle rest */
<Card className="mb-6">
  <CardHeader>
    <CardTitle>Title</CardTitle>
  </CardHeader>
</Card>

/* ✅ Correct — layout-only className */
<div className="flex items-center gap-2">
  <Badge>Active</Badge>
  <span className="text-sm text-muted-foreground">Updated 2h ago</span>
</div>
```

## 4. Replace space-y / space-x with gap

```tsx
/* ❌ Incorrect — space-y/space-x */
<div className="space-y-4">
<div className="flex items-center space-x-2">

/* ✅ Correct — flex gap */
<div className="flex flex-col gap-4">
<div className="flex items-center gap-2">
```

## 5. Use size-* for Equal Width/Height

```tsx
/* ❌ Incorrect */
<div className="w-10 h-10">

/* ✅ Correct */
<div className="size-10">
```

## 6. Use truncate Shorthand

```tsx
/* ❌ Incorrect */
<div className="overflow-hidden text-ellipsis whitespace-nowrap">

/* ✅ Correct */
<div className="truncate">
```

## 7. Use cn() for Conditional Classes

```tsx
/* ❌ Incorrect */
<div className={isActive ? "bg-primary text-primary-foreground" : "bg-muted"}>

/* ✅ Correct */
<div className={cn("rounded-md p-4", isActive ? "bg-primary text-primary-foreground" : "bg-muted")}>
```

## 8. No manual dark: Overrides

```tsx
/* ❌ Incorrect */
<div className="bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-50">

/* ✅ Correct */
<div className="bg-background text-foreground">
```

Semantic tokens automatically switch based on `.dark` class on `<html>`. Never write `dark:` variants for colors.

## 9. No z-index on Overlay Components

```tsx
/* ❌ Incorrect */
<DialogContent className="z-50">

/* ✅ Correct — Dialog/Sheet overlay handles stacking */
<DialogContent>
```

Components that handle their own z-index: `Dialog`, `Sheet`, `Drawer`, `Popover`, `HoverCard`, `Tooltip`, `DropdownMenu`, `Select`, `Combobox`.

## 10. Use Badge for Status Labels

```tsx
/* ❌ Incorrect */
<span className="text-red-600 font-semibold text-xs">Error</span>
<span className="bg-green-100 text-green-700 px-2 py-0.5 rounded text-xs">Active</span>

/* ✅ Correct */
<Badge variant="destructive">Error</Badge>
<Badge variant="success">Active</Badge>       /* custom variant */
<Badge variant="warning">Pending</Badge>      /* custom variant */
<Badge variant="secondary">Draft</Badge>
<Badge variant="outline">Archived</Badge>

/* With indicator dot */
<Badge variant="success" className="gap-1 before:size-1.5 before:rounded-full before:bg-current">
  Online
</Badge>
```

## 11. Component Override Order

Correct precedence when overriding styles:

```tsx
/* shadcn variant first, then className overrides */
<Button
  variant="outline"
  size="sm"
  className="border-red-500 text-red-500 hover:bg-red-50"
>
```

The `cn()` function in shadcn merges Tailwind classes so later classes win when conflicting.

## 12. Typography Classes

```tsx
/* Available via shadcn patterns — not raw Tailwind typography */
<h1 className="text-3xl font-bold tracking-tight lg:text-4xl">  /* Page title */
<h2 className="text-2xl font-semibold tracking-tight">           /* Section title */
<h3 className="text-xl font-semibold">                            /* Card title */
<p className="text-sm text-muted-foreground">                     /* Description */
<p className="text-sm">                                            /* Body */
<p className="text-xs text-muted-foreground">                     /* Caption */
<span className="text-xs text-muted-foreground">                  /* Metadata */
<small className="text-sm font-medium leading-none">              /* Label */
```

## 13. Focus Ring Discipline

```tsx
/* ❌ Incorrect — manual focus styles */
<button className="focus:outline focus:outline-2 focus:outline-blue-500">

/* ✅ Correct — use shadcn focus-visible ring */
<Button>  /* ring via component */
<input className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2">
```

## Quick Reference Table

| Rule | ❌ Don't | ✅ Do |
|---|---|---|
| Colors | `bg-blue-500`, `text-gray-600` | `bg-primary`, `text-muted-foreground` |
| Layout spacing | `space-y-4`, `space-x-2` | `gap-4`, `gap-2` |
| Equal dimensions | `w-10 h-10` | `size-10` |
| Text truncation | `overflow-hidden text-ellipsis whitespace-nowrap` | `truncate` |
| Dark mode | `dark:bg-black dark:text-white` | Semantic tokens auto-handle |
| Conditional | Inline ternary strings | `cn()` |
| Overlay z-index | `z-50` on Dialog/Sheet | Don't set — built-in |
| Status text | `text-red-600 font-semibold` | `<Badge variant="destructive">` |
| Focus | `focus:outline-blue-500` | `focus-visible:ring-2 focus-visible:ring-ring` |
