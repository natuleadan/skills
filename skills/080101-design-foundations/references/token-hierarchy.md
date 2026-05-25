# Design Token Architecture

## Token Hierarchy

Three-tier system: Brand → Semantic → Component. Each tier is strictly separated. Lower tiers never reference higher tiers.

```
Brand Tokens (abstract values)
    ↓
Semantic Tokens (purpose-bound aliases)
    ↓
Component Tokens (scoped application)
```

---

## Naming Conventions

### Structure

```
<namespace>-<category>-<property>[-<variant>][-<state>]
```

### Namespace

| Prefix | Scope |
|--------|-------|
| `brand-` | Raw brand values. Never used outside token definitions. |
| `color-` | Color tokens (semantic layer). |
| `space-` | Spacing tokens. |
| `font-` | Typography tokens. |
| `shadow-` | Shadow/elevation tokens. |
| `radius-` | Border radius tokens. |
| `motion-` | Animation and transition tokens. |
| `size-` | Sizing tokens (icons, avatars, hit targets). |

### Category + Property

```
color-surface         → background of a container
color-text            → text color
color-border          → border color
color-bg              → background for interactive elements
space-stack           → margin-block (vertical)
space-inline          → margin-inline (horizontal)
font-family           → typeface stack
font-weight           → numerical weight
font-size             → type scale step
font-leading          → line-height
shadow-elevation      → box-shadow by depth
radius-corner         → border-radius by size
motion-duration       → animation timing
motion-easing         → easing function
```

### Variant + State Examples

```
color-surface-raised       → elevated surface (cards, dialogs)
color-surface-sidebar      → secondary surface (navigation)
color-text-secondary       → muted text
color-text-disabled        → disabled text
color-bg-primary-hover     → primary button hover
color-bg-primary-active    → primary button pressed
color-bg-primary-disabled  → primary button disabled
color-border-focus         → focus ring
shadow-elevation-1         → low (cards)
shadow-elevation-2         → medium (dropdowns)
shadow-elevation-3         → high (modals)
motion-duration-fast       → 150ms
motion-duration-normal     → 250ms
motion-duration-slow       → 400ms
```

---

## Token Organization in CSS Custom Properties

### 1. Brand Token Layer (`:root`)

```css
:root {
  /* Hue hub — single source of truth for hue */
  --brand-hue: 260;

  /* Chroma values */
  --brand-chroma-subtle: 0.005;
  --brand-chroma-surface: 0.012;
  --brand-chroma-primary: 0.18;
  --brand-chroma-accent: 0.22;

  /* Typography */
  --brand-font-display: "Instrument Serif", "Georgia", serif;
  --brand-font-body: "Inter", "system-ui", sans-serif;
  --brand-font-mono: "JetBrains Mono", "SF Mono", monospace;

  /* Scale factors */
  --brand-scale-ratio: 1.25;

  /* Radius */
  --brand-radius-sm: 4px;
  --brand-radius-md: 8px;
  --brand-radius-lg: 12px;
  --brand-radius-full: 9999px;

  /* Easing */
  --brand-easing-enter: cubic-bezier(0.16, 1, 0.3, 1);
  --brand-easing-exit: cubic-bezier(0.4, 0, 0.6, 1);
}
```

### 2. Semantic Token Layer (`:root`)

```css
:root {
  /* Surfaces */
  --color-surface: oklch(97% var(--brand-chroma-subtle) var(--brand-hue));
  --color-surface-raised: oklch(99% var(--brand-chroma-subtle) var(--brand-hue));
  --color-surface-sidebar: oklch(93% var(--brand-chroma-surface) var(--brand-hue));

  /* Text */
  --color-text-primary: oklch(25% var(--brand-chroma-surface) var(--brand-hue));
  --color-text-secondary: oklch(45% var(--brand-chroma-surface) var(--brand-hue));
  --color-text-disabled: oklch(70% var(--brand-chroma-subtle) var(--brand-hue));
  --color-text-inverse: oklch(90% 0.04 var(--brand-hue));

  /* Brand colors */
  --color-brand-primary: oklch(45% var(--brand-chroma-primary) var(--brand-hue));
  --color-brand-accent: oklch(60% var(--brand-chroma-accent) 30);

  /* Borders */
  --color-border-subtle: oklch(88% var(--brand-chroma-subtle) var(--brand-hue));
  --color-border-strong: oklch(75% var(--brand-chroma-surface) var(--brand-hue));
  --color-border-focus: oklch(50% var(--brand-chroma-primary) var(--brand-hue));

  /* Interactive backgrounds */
  --color-bg-primary: var(--color-brand-primary);
  --color-bg-primary-hover: oklch(48% var(--brand-chroma-primary) var(--brand-hue));
  --color-bg-primary-active: oklch(40% var(--brand-chroma-primary) var(--brand-hue));
  --color-bg-primary-disabled: oklch(80% 0.08 var(--brand-hue));

  /* Shadows */
  --shadow-elevation-1: 0 1px 2px oklch(0% 0 0 / 8%);
  --shadow-elevation-2: 0 2px 8px oklch(0% 0 0 / 10%);
  --shadow-elevation-3: 0 8px 24px oklch(0% 0 0 / 12%);

  /* Spacing */
  --space-stack-xs: 4px;
  --space-stack-sm: 8px;
  --space-stack-md: 16px;
  --space-stack-lg: 24px;
  --space-stack-xl: 40px;
  --space-inline-xs: 4px;
  --space-inline-sm: 8px;
  --space-inline-md: 12px;
  --space-inline-lg: 20px;
  --space-inline-xl: 32px;

  /* Typography (fixed, product register) */
  --font-size-xs: 0.75rem;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-size-xl: 1.25rem;
  --font-size-2xl: 1.5rem;

  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  --font-leading-tight: 1.15;
  --font-leading-normal: 1.5;
  --font-leading-relaxed: 1.75;

  /* Motion */
  --motion-duration-fast: 150ms;
  --motion-duration-normal: 250ms;
  --motion-duration-slow: 400ms;
  --motion-easing-enter: var(--brand-easing-enter);
  --motion-easing-exit: var(--brand-easing-exit);
  --motion-easing-linear: linear;

  /* Radius */
  --radius-sm: var(--brand-radius-sm);
  --radius-md: var(--brand-radius-md);
  --radius-lg: var(--brand-radius-lg);
  --radius-full: var(--brand-radius-full);
}
```

### 3. Component Token Layer (Scoped)

```css
.button {
  /* Component-level aliases */
  --_bg: var(--color-bg-primary);
  --_color: var(--color-text-inverse);
  --_border: var(--color-border-subtle);
  --_radius: var(--radius-md);
  --_padding-block: var(--space-stack-sm);
  --_padding-inline: var(--space-inline-lg);
  --_font: var(--font-size-sm);
  --_font-weight: var(--font-weight-medium);
  --_motion: var(--motion-duration-fast) var(--motion-easing-enter);

  background: var(--_bg);
  color: var(--_color);
  border: 1px solid var(--_border);
  border-radius: var(--_radius);
  padding: var(--_padding-block) var(--_padding-inline);
  font-size: var(--_font);
  font-weight: var(--_font-weight);
  transition: background var(--_motion), box-shadow var(--_motion);
}

.button:hover {
  --_bg: var(--color-bg-primary-hover);
  --_shadow: var(--shadow-elevation-1);
  box-shadow: var(--_shadow);
}

.button:active {
  --_bg: var(--color-bg-primary-active);
}

.button:disabled {
  --_bg: var(--color-bg-primary-disabled);
  --_color: var(--color-text-disabled);
  --_border: var(--color-border-subtle);
  pointer-events: none;
}
```

---

## Dark Mode Adaptation

### Lower chroma, not darker colors

Dark mode should reduce chroma, not just invert lightness:

```css
:root[data-theme="dark"] {
  --color-surface: oklch(15% 0.008 var(--brand-hue));
  --color-surface-raised: oklch(20% 0.01 var(--brand-hue));
  --color-surface-sidebar: oklch(12% 0.006 var(--brand-hue));

  --color-text-primary: oklch(85% 0.02 var(--brand-hue));
  --color-text-secondary: oklch(65% 0.015 var(--brand-hue));

  --color-brand-primary: oklch(55% 0.16 var(--brand-hue));
  /* Higher L, lower chroma than light mode — the brand color glows rather than shouts */

  --shadow-elevation-1: 0 1px 2px oklch(0% 0 0 / 30%);
  --shadow-elevation-2: 0 2px 8px oklch(0% 0 0 / 40%);
  --shadow-elevation-3: 0 8px 24px oklch(0% 0 0 / 50%);
}
```

The key difference: text has lower chroma in dark mode (0.02 vs 0.015 for secondary), and surfaces use tighter lightness spreads (15–20% instead of 93–99%).

---

## Token Audit Checklist

- [ ] Every brand token is consumed by at least one semantic token (no orphan brand values)
- [ ] Every semantic token is consumed by at least one component (no orphan design decisions)
- [ ] No component uses a brand token directly (aliasing is strictly through semantic layer)
- [ ] No token name uses a color name (blue, red, green) — use functional role names
- [ ] All luminance values (light/dark) maintain WCAG 2.1 AA contrast against their paired text color
- [ ] Chroma values respect the lightness/chroma calibration table
- [ ] Every interactive state (hover, active, disabled, focus) has a defined token
- [ ] Shadow tokens use oklch() with alpha transparency, not rgba or hsla
