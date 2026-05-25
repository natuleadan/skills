# Tailwind CSS v4 Complete Reference

## @theme Token Reference

### Color Tokens

```css
@theme {
  /* OKLCH color space — preferred over hex/rgb for perceptually uniform gradients */
  --color-primary: oklch(0.62 0.17 72);
  --color-primary-foreground: oklch(0.97 0.01 72);

  /* Color with fixed hue scale (30° step = ~12 hue units in OKLCH) */
  --color-brand-50: oklch(0.97 0.01 72);
  --color-brand-100: oklch(0.93 0.03 72);
  --color-brand-200: oklch(0.86 0.06 72);
  --color-brand-300: oklch(0.78 0.10 72);
  --color-brand-400: oklch(0.70 0.14 72);
  --color-brand-500: oklch(0.62 0.17 72);
  --color-brand-600: oklch(0.54 0.19 72);
  --color-brand-700: oklch(0.46 0.18 72);
  --color-brand-800: oklch(0.38 0.15 72);
  --color-brand-900: oklch(0.30 0.11 72);
  --color-brand-950: oklch(0.22 0.07 72);

  /* Neutral (gray) — hue 260 for cooler neutrals */
  --color-neutral-50: oklch(0.98 0.00 260);
  --color-neutral-100: oklch(0.95 0.00 260);
  --color-neutral-200: oklch(0.90 0.00 260);
  --color-neutral-300: oklch(0.83 0.00 260);
  --color-neutral-400: oklch(0.68 0.00 260);
  --color-neutral-500: oklch(0.54 0.00 260);
  --color-neutral-600: oklch(0.43 0.00 260);
  --color-neutral-700: oklch(0.34 0.00 260);
  --color-neutral-800: oklch(0.26 0.00 260);
  --color-neutral-900: oklch(0.19 0.00 260);
  --color-neutral-950: oklch(0.14 0.00 260);

  /* OKLCH format: oklch(L C H) or oklch(L C H / alpha) */
  /* L: lightness 0-1 | C: chroma 0-0.4 | H: hue 0-360 */
}
```

### Spacing Tokens

```css
@theme {
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --spacing-2xl: 48px;
  --spacing-3xl: 64px;
}
```

### Border Radius Tokens

```css
@theme {
  --radius-none: 0;
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-full: 9999px;
}
```

### Animation Tokens

```css
@theme {
  --animate-fade-in: fade-in 0.2s ease-out;
  --animate-fade-in-up: fade-in-up 0.3s ease-out;
  --animate-slide-down: slide-down 0.3s ease-out;
  --animate-spin: spin 1s linear infinite;
  --animate-pulse: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes fade-in-up {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slide-down {
  from { opacity: 0; transform: translateY(-8px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes pulse {
  50% { opacity: 0.5; }
}
```

### @theme inline

Use `@theme inline` for tokens that reference other custom properties. These are not hoisted to Tailwind utility classes but are available as CSS variables:

```css
@theme inline {
  --color-primary: var(--color-brand-500);
  --color-primary-foreground: var(--color-neutral-50);
  --color-ring: var(--color-brand-300);
  --color-destructive: var(--color-red-500);
  --color-destructive-foreground: var(--color-neutral-50);
  --color-background: var(--color-neutral-50);
  --color-foreground: var(--color-neutral-950);
  --color-muted: var(--color-neutral-100);
  --color-muted-foreground: var(--color-neutral-500);
  --color-accent: var(--color-neutral-100);
  --color-accent-foreground: var(--color-neutral-900);
  --color-border: var(--color-neutral-200);
  --color-input: var(--color-neutral-200);
}
```

### @theme static

Use `@theme static` for tokens that must always be present in the output CSS, even if not directly referenced by Tailwind utilities:

```css
@theme static {
  --font-sans: "Inter Variable", sans-serif;
  --font-mono: "JetBrains Mono Variable", monospace;
}
```

## @custom-variant (Dark Mode)

```css
/* CSS-based dark mode — replaces darkMode: "class" */
@custom-variant dark (&:where(.dark, .dark *));

/* Theme overrides */
@layer base {
  :root.dark, .dark, .dark * {
    --color-background: oklch(0.15 0.01 260);
    --color-foreground: oklch(0.93 0.01 260);
    --color-primary: var(--color-brand-400);
    --color-primary-foreground: var(--color-neutral-950);
    --color-muted: oklch(0.20 0.01 260);
    --color-muted-foreground: oklch(0.60 0.01 260);
    --color-accent: oklch(0.25 0.01 260);
    --color-accent-foreground: oklch(0.93 0.01 260);
    --color-border: oklch(0.25 0.01 260);
    --color-input: oklch(0.25 0.01 260);
  }
}
```

Custom variants for other states:

```css
/* Custom group-based variant */
@custom-variant group-hover-sidebar (&:where(.group:hover .group-hover-sidebar\\:block));

/* Responsive variants are built-in:
   sm:, md:, lg:, xl:, 2xl:
   Motion preferences: motion-safe:, motion-reduce:
   */


## @utility Reference

```css
/* Decorative line */
@utility decorative-line {
  content: "";
  display: block;
  width: 48px;
  height: 3px;
  border-radius: 2px;
  background: linear-gradient(90deg, var(--color-brand-400), var(--color-brand-600));
}

/* Text gradient — use initial to prevent color inheritance */
@utility text-gradient {
  --color-*: initial;
  background: linear-gradient(135deg, var(--color-brand-400), var(--color-brand-600));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

/* Glass morphism */
@utility glass {
  background: color-mix(in oklch, var(--color-background) 60%, transparent);
  backdrop-filter: blur(12px);
  border: 1px solid var(--color-border);
}

/* Hover lift */
@utility hover-lift {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px color-mix(in oklch, var(--color-foreground) 10%, transparent);
  }
}
```

## @starting-style for Entry Animations

```css
/* Entry animation for dialog/sheet panels */
@starting-style {
  .panel-from-bottom {
    opacity: 0;
    transform: translateY(100%);
  }
}

.panel-from-bottom {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 0.3s, transform 0.3s allow-discrete;
}

/* Native popover */
@starting-style {
  .popover-content {
    opacity: 0;
    transform: scale(0.95);
  }
}

.popover-content {
  opacity: 1;
  transform: scale(1);
  transition: opacity 0.2s, transform 0.2s allow-discrete;
}
```

## Container Queries

```css
@theme {
  --container-sm: 320px;
  --container-md: 480px;
  --container-lg: 640px;
}

@container (min-width: 320px) {
  .responsive-card { padding: 12px; }
}

@container (min-width: 480px) {
  .responsive-card {
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: 16px;
    padding: 16px;
  }
}

@container (min-width: 640px) {
  .responsive-card {
    grid-template-columns: 1fr 1fr 1fr;
    gap: 24px;
    padding: 24px;
  }
}
```

In JSX:

```tsx
<div className="container">
  <div className="responsive-card">content</div>
</div>
```

## color-mix() for Alpha Scales

```css
@theme {
  --color-primary: oklch(0.62 0.17 72);

  /* Generate alpha variants with color-mix */
  --color-primary-alpha-5: color-mix(in oklch, var(--color-primary) 5%, transparent);
  --color-primary-alpha-10: color-mix(in oklch, var(--color-primary) 10%, transparent);
  --color-primary-alpha-20: color-mix(in oklch, var(--color-primary) 20%, transparent);
  --color-primary-alpha-30: color-mix(in oklch, var(--color-primary) 30%, transparent);
  --color-primary-alpha-40: color-mix(in oklch, var(--color-primary) 40%, transparent);
  --color-primary-alpha-50: color-mix(in oklch, var(--color-primary) 50%, transparent);
  --color-primary-alpha-60: color-mix(in oklch, var(--color-primary) 60%, transparent);
  --color-primary-alpha-70: color-mix(in oklch, var(--color-primary) 70%, transparent);
  --color-primary-alpha-80: color-mix(in oklch, var(--color-primary) 80%, transparent);
  --color-primary-alpha-90: color-mix(in oklch, var(--color-primary) 90%, transparent);
}

/* Usage */
.bg-primary-alpha-20 {
  background-color: var(--color-primary-alpha-20);
}
```

## CVA Component Factory Patterns

### cn() Utility

```ts
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

### Button Component

```tsx
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"
import { Slot } from "@radix-ui/react-slot"

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground shadow hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground shadow-sm hover:bg-destructive/90",
        outline: "border border-input bg-background shadow-sm hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground shadow-sm hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        sm: "h-8 rounded-md px-3 text-xs",
        md: "h-9 rounded-md px-4 text-sm",
        lg: "h-10 rounded-md px-6 text-base",
        xl: "h-12 rounded-md px-8 text-lg",
        icon: "size-9",
        "icon-sm": "size-8",
        "icon-lg": "size-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "md",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

export function Button({
  className,
  variant,
  size,
  asChild = false,
  ...props
}: ButtonProps) {
  const Comp = asChild ? Slot : "button"
  return (
    <Comp
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  )
}
```

### Badge Component

```tsx
const badgeVariants = cva(
  "inline-flex items-center rounded-md border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
  {
    variants: {
      variant: {
        default: "border-transparent bg-primary text-primary-foreground shadow",
        secondary: "border-transparent bg-secondary text-secondary-foreground",
        destructive: "border-transparent bg-destructive text-destructive-foreground shadow",
        outline: "text-foreground",
        success: "border-transparent bg-emerald-500/15 text-emerald-600 dark:bg-emerald-500/20 dark:text-emerald-400",
        warning: "border-transparent bg-amber-500/15 text-amber-600 dark:bg-amber-500/20 dark:text-amber-400",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)
```

### Responsive Grid Component

```tsx
const gridVariants = cva(
  "grid",
  {
    variants: {
      cols: {
        1: "grid-cols-1",
        2: "grid-cols-1 sm:grid-cols-2",
        3: "grid-cols-1 sm:grid-cols-2 lg:grid-cols-3",
        4: "grid-cols-1 sm:grid-cols-2 lg:grid-cols-4",
        auto: "grid-cols-[repeat(auto-fill,minmax(280px,1fr))]",
        "auto-sm": "grid-cols-[repeat(auto-fill,minmax(240px,1fr))]",
        "auto-lg": "grid-cols-[repeat(auto-fill,minmax(320px,1fr))]",
      },
      gap: {
        none: "gap-0",
        xs: "gap-2",
        sm: "gap-3",
        md: "gap-4",
        lg: "gap-6",
        xl: "gap-8",
      },
    },
    defaultVariants: {
      cols: 1,
      gap: "md",
    },
  }
)

export interface GridProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof gridVariants> {}

export function Grid({ className, cols, gap, ...props }: GridProps) {
  return <div className={cn(gridVariants({ cols, gap, className }))} {...props} />
}
```

### Container Component

```tsx
const containerVariants = cva(
  "mx-auto w-full px-4 sm:px-6",
  {
    variants: {
      size: {
        sm: "max-w-2xl",
        md: "max-w-4xl",
        lg: "max-w-6xl",
        xl: "max-w-7xl",
        full: "max-w-full",
      },
    },
    defaultVariants: {
      size: "lg",
    },
  }
)

export interface ContainerProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof containerVariants> {}

export function Container({ className, size, ...props }: ContainerProps) {
  return <div className={cn(containerVariants({ size, className }))} {...props} />
}
```

## v3 → v4 Full Migration Checklist

| v3 (JavaScript/PostCSS) | v4 (CSS-first) | Notes |
|---|---|---|
| `@tailwind base;` `@tailwind components;` `@tailwind utilities;` | `@import "tailwindcss";` | Single import replaces three directives |
| `tailwind.config.ts` with `theme.extend` | `@theme` block in CSS | All tokens move to CSS |
| `darkMode: "class"` or `"media"` | `@custom-variant dark (&:where(.dark, .dark *))` | Custom variant replaces config option |
| `theme.extend.colors = { brand: { 500: "..." } }` | `--color-brand-500: oklch(...)` | Flat CSS custom properties |
| `theme.extend.spacing = { 18: "72px" }` | `--spacing-18: 72px;` | Token-based spacing |
| `theme.extend.borderRadius = { xl: "16px" }` | `--radius-xl: 16px;` | Token-based radius |
| `theme.extend.fontFamily = { sans: ["Inter"] }` | `--font-sans: "Inter Variable", sans-serif;` | Simple string value |
| `require("tailwindcss-animate")` | `--animate-*` + `@keyframes` | CSS keyframes replace plugin |
| `require("@tailwindcss/container-queries")` | `--container-*` tokens + `@container` | Native container queries |
| `plugins: [require("@tailwindcss/forms")]` | `@plugin "@tailwindcss/forms"` | Inline plugin import |
| `content: ["./src/**/*.{ts,tsx}"]` | Automatic | v4 detects all project files |
| `safelist: ["bg-red-500"]` | `@theme static` + generate utilities | Static token output |
| `@apply bg-blue-500 text-white` | `@apply bg-primary text-primary-foreground` | Same syntax, prefers semantic tokens |
| `important: true` | `@important "tailwindcss"` | Different syntax |
| `prefix: "tw-"` | `@prefix "tw-"` | Same concept, CSS-based |
| `npx tailwindcss init` | No init needed | CSS-first from scratch |
| `PostCSS` + `tailwindcss` + `autoprefixer` | `@import "tailwindcss"` bundles autoprefixer | Fewer dependencies |
| `theme.extend.keyframes` | `@keyframes` inside CSS + `--animate-*` in `@theme` | Keyframes decoupled from theme |

### Notable removals in v4

| Feature | v3 | v4 |
|---|---|---|
| `@layer utilities` | Custom utility classes | `@utility` directive |
| `@variants` / `@responsive` | Generated variant classes | Automatic — all utilities work with variants |
| `@screen` | Media query aliases | Use standard `@media` or container queries |
| `theme()` function | Access theme values in CSS | Use `var(--token-name)` directly |
| Config `safelist` | Prevent purging unused utilities | No direct equivalent — use dynamic classes or `@theme static` |
