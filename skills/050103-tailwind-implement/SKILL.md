---
name: 050103-tailwind-implement
description: "Use this skill whenever implementing Tailwind CSS v4 configuration, shadcn/ui component composition, or frontend design tokens. Trigger on: Tailwind CSS configuration, `@theme` blocks, `@import tailwindcss`, `@custom-variant dark`, `@utility` definitions, `@starting-style` animations, container queries, `color-mix()` alpha scales, CVA component factories (cva, cn), shadcn/ui patterns (FieldGroup, InputGroup, ToggleGroup, Card, Dialog, Sheet, Alert, Empty, Badge, Skeleton, Separator, Avatar, Tabs), form validation states, Button loading with Spinner, icon sizing/stroke rules, and the Base vs Radix API differences (asChild, render, Select, Accordion, Slider, ToggleGroup). Do NOT trigger for general CSS, non-Tailwind styling, or design token theory (use 080101-design-foundations instead)."
---

# Tailwind CSS v4 Configuration & shadcn/ui Component Composition

This covers the implementation layer of frontend design — translating design tokens into `@theme` blocks and composing shadcn/ui components following the component system rules.

## PART 1: TAILWIND CSS v4

### 1. CSS-First Configuration

Tailwind v4 moves configuration from JavaScript to CSS:

```css
/* ❌ v3 — tailwind.config.ts */
import type { Config } from "tailwindcss"

/* ✅ v4 — app.css / globals.css */
@import "tailwindcss";
```

#### @theme Block

The `@theme` block replaces `tailwind.config.ts` for all design token definitions:

```css
@import "tailwindcss";

@theme {
  /* Colors — use OKLCH for perceptually uniform colors */
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

  /* Semantic tokens reference the base palette */
  --color-primary: var(--color-brand-500);
  --color-primary-foreground: var(--color-neutral-50);

  /* Spacing */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --spacing-2xl: 48px;

  /* Border radius */
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 12px;

  /* Animations */
  --animate-fade-in: fade-in 0.2s ease-out;
  --animate-slide-up: slide-up 0.3s ease-out;

  /* Fonts */
  --font-sans: "Inter Variable", sans-serif;
  --font-mono: "JetBrains Mono Variable", monospace;
}

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slide-up {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}
```

#### @theme inline

Use `@theme inline` when a token references another CSS custom property that shouldn't be hoisted to Tailwind's utility layer:

```css
@theme inline {
  --color-primary: var(--color-brand-500);
  --color-primary-foreground: var(--color-neutral-50);
  --color-ring: var(--color-brand-300);
}
```

#### @theme static

Use `@theme static` for tokens that should always be output even when unused:

```css
@theme static {
  --font-sans: "Inter Variable", sans-serif;
  --font-mono: "JetBrains Mono Variable", monospace;
}
```

### 2. Dark Mode

```css
/* ❌ v3 — tailwind.config.ts
darkMode: "class"
*/

/* ✅ v4 — CSS @custom-variant */
@custom-variant dark (&:where(.dark, .dark *));

/* Dark mode overrides via semantic tokens */
@layer base {
  :root.dark, .dark, .dark * {
    --color-primary: var(--color-brand-400);
    --color-primary-foreground: var(--color-neutral-950);
    --color-background: oklch(0.15 0.01 260);
    --color-foreground: oklch(0.93 0.01 260);
  }
}
```

Semantic tokens automatically handle dark mode — never write `dark:` color overrides:

```tsx
/* ❌ Bad — manual dark: override */
<div className="bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-50" />

/* ✅ Good — semantic tokens handle it automatically */
<div className="bg-background text-foreground" />
```

### 3. Custom Utilities with @utility

```css
@utility decorative-line {
  content: "";
  display: block;
  width: 48px;
  height: 3px;
  border-radius: 2px;
  background: linear-gradient(90deg, var(--color-brand-400), var(--color-brand-600));
}

@utility text-gradient {
  background: linear-gradient(135deg, var(--color-brand-400), var(--color-brand-600));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

/* Namespace override — prevent collision with standard utilities */
@utility text-gradient {
  --color-*: initial;
  background: linear-gradient(135deg, var(--color-brand-400), var(--color-brand-600));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}
```

Usage:
```tsx
<div className="decorative-line" />
<h1 className="text-gradient">Brand Heading</h1>
```

### 4. @starting-style for Entry Animations

```css
@starting-style {
  .dialog-panel {
    opacity: 0;
    transform: scale(0.95);
  }
}

.dialog-panel {
  opacity: 1;
  transform: scale(1);
  transition: opacity 0.2s, transform 0.2s;
}
```

### 5. Container Queries

```css
@theme {
  --container-sm: 320px;
  --container-md: 480px;
  --container-lg: 640px;
}

@container (min-width: 480px) {
  .card-grid { grid-template-columns: repeat(2, 1fr); }
}

@container (min-width: 640px) {
  .card-grid { grid-template-columns: repeat(3, 1fr); }
}
```

In JSX, wrap with `className="container"` on the parent:

```tsx
<div className="container">
  <div className="card-grid">...</div>
</div>
```

### 6. color-mix() for Alpha Scales

```css
@theme {
  --color-primary: oklch(0.62 0.17 72);
  --color-primary-alpha-10: color-mix(in oklch, var(--color-primary) 10%, transparent);
  --color-primary-alpha-20: color-mix(in oklch, var(--color-primary) 20%, transparent);
  --color-primary-alpha-50: color-mix(in oklch, var(--color-primary) 50%, transparent);
}
```

### 7. CVA Component Factory Pattern

Use `cva` (class-variance-authority) for component variants:

```tsx
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

/* Button Component */
const buttonVariants = cva(
  /* Base styles */
  "inline-flex items-center justify-center gap-2 rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        sm: "h-9 rounded-md px-3 text-xs",
        md: "h-10 rounded-md px-4 text-sm",
        lg: "h-11 rounded-md px-6 text-base",
        icon: "size-9",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "md",
    },
  }
)

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement>, VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

export function Button({ className, variant, size, asChild = false, ...props }: ButtonProps) {
  const Comp = asChild ? Slot : "button"
  return <Comp className={cn(buttonVariants({ variant, size, className }))} {...props} />
}

/* Responsive Grid */
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
      },
      gap: {
        none: "gap-0",
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

/* Container Component */
const containerVariants = cva(
  "mx-auto w-full px-4",
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
```

### 8. v3 → v4 Migration Checklist

| v3 (JavaScript) | v4 (CSS) |
|---|---|
| `tailwind.config.ts` | `@theme` block in CSS |
| `@tailwind base/components/utilities` | `@import "tailwindcss"` |
| `darkMode: "class"` | `@custom-variant dark (&:where(.dark, .dark *))` |
| `theme.extend.colors` | `--color-*` in `@theme` |
| `theme.extend.spacing` | `--spacing-*` in `@theme` |
| `theme.extend.borderRadius` | `--radius-*` in `@theme` |
| `require("tailwindcss-animate")` | `@keyframes` + `--animate-*` in `@theme` |
| `require("@tailwindcss/container-queries")` | Native `@container` via `--container-*` tokens |
| `plugins: [forms, typography]` | `@plugin` directive or native CSS |
| `safelist: [...]` | No direct equivalent — use `@theme static` |
| `content: [...]` (paths) | Automatic — scans all files in project |
| `@apply` in external CSS | Still supported, but prefer `@utility` for custom patterns |

## PART 2: SHADCN/UI COMPONENTS

### 9. Critical Styling Rules

| Rule | ❌ Incorrect | ✅ Correct |
|---|---|---|
| Use semantic colors | `bg-blue-500 text-white` | `bg-primary text-primary-foreground` |
| No space-y/space-x | `space-y-4` | `flex flex-col gap-4` |
| size-* for equal w/h | `w-10 h-10` | `size-10` |
| truncate shorthand | `overflow-hidden text-ellipsis whitespace-nowrap` | `truncate` |
| No dark: overrides | `bg-white dark:bg-black` | `bg-background` (semantic) |
| cn() for conditionals | `className={variant === "primary" ? "bg-blue..." : "bg-gray..."}` | `cn("base", variant && buttonVariants({variant}))` |
| No z-index on overlays | `z-50` on Dialog content | Don't set z-index — Dialog/Sheet handle it |
| Status colors | `text-red-600 font-semibold` | `<Badge variant="destructive">Error</Badge>` |
| Variants first | Custom styles before variants | Use `cva` variants, then `cn()` overrides |
| className for layout only | `className="text-primary font-bold text-lg"` | `className="flex gap-2 items-center"` |

### 10. Forms & Inputs

```tsx
/* ✅ FieldGroup + Field — not raw divs */
<FieldGroup>
  <Field>
    <Label htmlFor="name">Full Name</Label>
    <Input id="name" placeholder="John Doe" />
    <FieldMessage>Enter your full legal name</FieldMessage>
  </Field>

  <Field>
    <Label htmlFor="email">Email</Label>
    <InputGroup>
      <InputGroupAddon>
        <IconMail className="size-4" />
      </InputGroupAddon>
      <InputGroupInput id="email" type="email" placeholder="you@example.com" />
    </InputGroup>
    <FieldMessage>We'll never share your email</FieldMessage>
  </Field>
</FieldGroup>

/* ✅ ToggleGroup for option sets (2-7 choices) */
<Field>
  <Label>Theme Preference</Label>
  <ToggleGroup type="single" defaultValue="light">
    <ToggleGroupItem value="light">Light</ToggleGroupItem>
    <ToggleGroupItem value="dark">Dark</ToggleGroupItem>
    <ToggleGroupItem value="system">System</ToggleGroupItem>
  </ToggleGroup>
</Field>

/* ✅ FieldSet for grouped checkboxes/radios */
<FieldSet>
  <FieldLegend>Notification Preferences</FieldLegend>
  <Field>
    <Checkbox id="email-notif" />
    <Label htmlFor="email-notif">Email notifications</Label>
  </Field>
  <Field>
    <Checkbox id="sms-notif" />
    <Label htmlFor="sms-notif">SMS notifications</Label>
  </Field>
</FieldSet>

/* ✅ Validation states */
<Field data-invalid>
  <Label htmlFor="password">Password</Label>
  <InputGroup>
    <InputGroupInput
      id="password"
      type="password"
      aria-invalid="true"
      aria-describedby="password-error"
    />
  </InputGroup>
  <FieldMessage id="password-error">Password must be at least 8 characters</FieldMessage>
</Field>
```

### 11. Component Composition

```tsx
/* ✅ Select — items inside their group */
<Select>
  <SelectGroup>
    <SelectLabel>Fruits</SelectLabel>
    <SelectItem value="apple">Apple</SelectItem>
    <SelectItem value="banana">Banana</SelectItem>
  </SelectGroup>
  <SelectGroup>
    <SelectLabel>Vegetables</SelectLabel>
    <SelectItem value="carrot">Carrot</SelectItem>
  </SelectGroup>
</Select>

/* ✅ Callout — use Alert, not custom divs */
<Alert variant="destructive">
  <AlertCircle className="size-4" />
  <AlertTitle>Error</AlertTitle>
  <AlertDescription>Failed to save changes. Please try again.</AlertDescription>
</Alert>

/* ✅ Empty state */
<Empty title="No products found" description="Try adjusting your filters.">
  <Button variant="outline">Clear Filters</Button>
</Empty>

/* ✅ Toast via sonner */
import { toast } from "sonner"
toast.success("Changes saved")
toast.error("Something went wrong")

/* ✅ Dialog with Title */
<Dialog>
  <DialogTrigger asChild>
    <Button variant="outline">Open</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogTitle>Edit Profile</DialogTitle>
    {/* or sr-only if visually hidden */}
    <DialogDescription className="sr-only">Edit your profile settings</DialogDescription>
    ...
  </DialogContent>
</Dialog>

/* ✅ Full Card structure */
<Card>
  <CardHeader>
    <CardTitle>Card Title</CardTitle>
    <CardDescription>Optional description</CardDescription>
  </CardHeader>
  <CardContent>
    <p>Main content here</p>
  </CardContent>
  <CardFooter>
    <Button>Save</Button>
  </CardFooter>
</Card>

/* ✅ Button loading — compose with Spinner */
<Button disabled>
  <Spinner className="size-4" data-icon="inline-start" />
  Saving...
</Button>

/* ✅ Avatar with fallback */
<Avatar>
  <AvatarImage src="/avatar.jpg" alt="John Doe" />
  <AvatarFallback>JD</AvatarFallback>
</Avatar>

/* ✅ Separator instead of hr */
<Separator />
<p className="text-muted-foreground">Content below separator</p>

/* ✅ Skeleton for loading */
<div className="space-y-3">
  <Skeleton className="h-4 w-[250px]" />
  <Skeleton className="h-4 w-[200px]" />
</div>

/* ✅ Badge instead of custom spans */
<Badge variant="secondary">In Progress</Badge>
<Badge variant="destructive">Blocked</Badge>
<Badge variant="outline">Draft</Badge>
```

### 12. Icons

```tsx
/* ✅ Use iconLibrary icons (lucide-react, @tabler/icons-react, etc.) */
import { IconMail, IconX } from "@tabler/icons-react"

/* ✅ data-icon attributes in buttons */
<Button>
  <IconX className="size-4" data-icon="inline-start" />
  Cancel
</Button>

<Button>
  Edit
  <IconPencil className="size-4" data-icon="inline-end" />
</Button>

/* ❌ No sizing classes on icons inside components */
<Button>
  <IconX size={24} />      /* ❌ — component handles sizing via CSS */
  Cancel
</Button>

/* ✅ */
<Button>
  <IconX className="size-4" />
  Cancel
</Button>

/* ✅ Pass icons as component objects */
const menuItems = [
  { icon: IconHome, label: "Home" },
  { icon: IconSettings, label: "Settings" },
]

/* ✅ Consistent icon sizing */
<IconMail className="icon-sm" />   /* 16pt */
<IconMail className="size-4" />    /* 16pt */
<IconMail className="size-5" />    /* 20pt */
<IconMail className="icon-md" />   /* 24pt */
<IconMail className="size-6" />    /* 24pt */
<IconMail className="icon-lg" />   /* 32pt */
```

### 13. Base vs Radix API Differences

| Aspect | Radix UI | Base UI |
|---|---|---|
| Element override | `asChild` prop + `Slot` | `render` prop |
| Select | `SelectItem` children (nested `<Select.Item value="">`) | `items` prop (array of `{value, label, disabled?}`) |
| ToggleGroup | `type="single"` or `type="multiple"` | `multiple` boolean prop |
| Slider value | scalar (single) or array (range) | scalar only (array via `min/max` values) |
| Accordion | `type="single"` or `type="multiple"`, `defaultValue` as string or array | `defaultValue` always array, `multiple` boolean |
| Non-button elements | Can't — trigger must be `<button>` | `render` allows any element |

```tsx
/* Radix — asChild for element override */
<DialogTrigger asChild>
  <Button variant="outline">Open</Button>
</DialogTrigger>

/* Base — render for element override */
<Select
  items={[
    { value: "apple", label: "Apple" },
    { value: "banana", label: "Banana" },
  ]}
  render={{ renderValue: (value) => <span>{value.label}</span> }}
/>

/* ❌ Don't wrap triggers in extra elements */
<DialogTrigger>
  <div>                          /* ❌ extra wrapper */
    <Button>Open</Button>
  </div>
</DialogTrigger>

/* ✅ Direct asChild or render */
<DialogTrigger asChild>
  <Button>Open</Button>
</DialogTrigger>
```
