# Type Scale Reference

## Modular Scale Concept

A modular scale multiplies a base size by a ratio to produce a sequence of harmonious font sizes.

```
base × ratio^step
```

For base = 16px and ratio = 1.25 (major third):

| Step | Calculation | Size (px) | rem |
|---|---|---|---|
| -2 | 16 × 1.25^-2 | 10.24 | 0.64 |
| -1 | 16 × 1.25^-1 | 12.80 | 0.80 |
| 0 | 16 × 1.25^0 | 16.00 | 1.000 |
| 1 | 16 × 1.25^1 | 20.00 | 1.250 |
| 2 | 16 × 1.25^2 | 25.00 | 1.563 |
| 3 | 16 × 1.25^3 | 31.25 | 1.953 |
| 4 | 16 × 1.25^4 | 39.06 | 2.441 |
| 5 | 16 × 1.25^5 | 48.83 | 3.052 |

### Ratio selection guide

| Ratio | Musical term | Character | Best for |
|---|---|---|---|
| 1.200 | Minor third | Subtle, tight | Dense data UIs, dashboards |
| 1.250 | Major third | Balanced, harmonic | Most product UIs |
| 1.333 | Perfect fourth | Clear hierarchy | Editorial, long-form |
| 1.500 | Perfect fifth | Dramatic | Brand/marketing, heroes |
| 1.618 | Golden ratio | Extreme contrast | Landing pages, posters |

**Rule**: The minimum usable ratio is 1.25. Below this, the steps are too close together to create visible hierarchy.

**Practice**: Pick one ratio and stick to it. Using different ratios for different breakpoints breaks the system's predictability.

---

## Fluid Type Scale (for brand surfaces)

### Fluid vs fixed decision

```
Is this a product UI or brand/marketing surface?
  ├── Product UI → fixed rem scale (predictable, testable)
  └── Brand/marketing → fluid clamp() scale (graceful across viewports)
```

### clamp() formula

The general pattern:

```css
/* Target: 48px at 375px → 80px at 1440px */
/* Step 1: Convert to rem (divide by 16) */
/*   min: 48 / 16 = 3rem */
/*   max: 80 / 16 = 5rem */
/* Step 2: Calculate the preferred value */
/*   slope: (5 - 3) / (1440 / 16 - 375 / 16) = 2 / 66.5625 = 0.03 */
/*   intercept: 3 - 0.03 * (375 / 16) = 3 - 0.703 = 2.297 */
/*   preferred: 2.297rem + 3vw */

--font-size-hero: clamp(3rem, 2.3rem + 3vw, 5rem);
```

Simplified for practical use:

```css
--fs-hero: clamp(3rem, 2rem + 4vw, 5rem);
--fs-section: clamp(2rem, 1.5rem + 2.5vw, 3rem);
--fs-subhead: clamp(1.25rem, 1rem + 1vw, 1.5rem);
--fs-body: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
```

### Modular fluid scale generator

For a systematic approach, define each step as a clamp based on the modular scale at min and max viewports:

```
At 375px viewport:  1rem base × 1.25^step
At 1440px viewport: 1.125rem base × 1.333^step

--fs-1: clamp(0.8rem, 0.7rem + 0.4vw, 0.875rem)
--fs-2: clamp(0.875rem, 0.8rem + 0.3vw, 0.875rem)  // body stays stable
--fs-3: clamp(1rem, 0.9rem + 0.5vw, 1.125rem)
--fs-4: clamp(1.25rem, 1rem + 1vw, 1.5rem)
--fs-5: clamp(1.5rem, 1.1rem + 1.5vw, 2rem)
--fs-6: clamp(2rem, 1.3rem + 2.5vw, 3rem)
--fs-7: clamp(2.5rem, 1.5rem + 4vw, 4.5rem)
```

Tools: [typescale.com](https://typescale.com), [utopia.fyi](https://utopia.fyi), [fluid-type-generator](https://fluid-type-generator.vercel.app)

---

## Fixed rem Scale (for product UI)

Product UIs need predictability. A fixed rem scale ensures that type does not change size unpredictably across viewports.

### Recommended scale for product UI

| Token | Value | Tailwind equivalent | Usage |
|---|---|---|---|
| --fs-xs | 0.75rem | text-xs | Captions, timestamps, metadata |
| --fs-sm | 0.875rem | text-sm | Labels, secondary text, form help |
| --fs-base | 1rem | text-base | Body text, paragraphs |
| --fs-md | 1.125rem | text-lg | Large body, intro, lead paragraph |
| --fs-lg | 1.5rem | text-2xl | Subheadings, section titles |
| --fs-xl | 2rem | text-4xl | Major headings, page titles |
| --fs-2xl | 2.5rem | text-5xl | Section hero titles |
| --fs-3xl | 3.5rem | text-7xl | Landing page heroes |

### Why fixed rem for product UI

1. **Accessibility**: Users who set a browser default font size get a proportional scale. `clamp()` can override user preferences.
2. **Predictability**: A 1.5rem subhead is the same size on mobile and desktop. Product UI elements don't need to "feel bigger" on desktop — that's what layout (sidebar, multi-column) does.
3. **Testing**: Fixed sizes are deterministic. No viewport-dependent behavior to debug.

---

## Weight Hierarchy

### Standard weight tokens

```css
:root {
  --fw-light: 300;
  --fw-regular: 400;
  --fw-medium: 500;
  --fw-semibold: 600;
  --fw-bold: 700;
  --fw-extrabold: 800;
}
```

### Usage by element

| Element | Weight | Rationale |
|---|---|---|
| Page headings (h1) | 700 | Maximum emphasis |
| Section headings (h2-h3) | 600 | Clearly subordinated to h1 |
| Subheadings (h4-h6) | 600 | Same weight as h2-h3 but smaller |
| Body text | 400 | Readability at length |
| Strong / emphasis | 600 | Stands out without shouting |
| Labels | 500 | Visible but attached to input |
| Captions | 400 | De-emphasized |
| Navigation links | 500 | Active can be 600 |

### Dark background adjustments

Light-on-dark text suffers from **halation** — light bleeds optically into dark surroundings, making thin strokes appear thinner.

| Adjustment | Light-on-dark (vs dark-on-light) |
|---|---|
| Weight | Add 50-100 (e.g., 400 → 450 or 500) |
| Line-height | Increase by 0.05-0.1 |
| Letter-spacing | Add 0.01-0.02em for sizes under 16px |
| Avoid | Weights under 400 for body text |

---

## Line-height Guidelines

### Per size and platform

```css
:root {
  /* Display / Hero */
  --lh-display: 1.0;     /* 3rem+ type — tight for impact */
  --lh-heading: 1.15;    /* 1.5-2.5rem — moderate */
  --lh-subhead: 1.25;    /* 1.125-1.5rem — slightly open */
  --lh-body: 1.5;        /* 1rem body — comfortable reading */
  --lh-body-large: 1.6;  /* 1rem body, long-form */
  --lh-small: 1.4;       /* < 1rem — compact */
}
```

### Platform differences

| Platform | Line-height preference | Reason |
|---|---|---|
| Web (desktop) | 1.5-1.6 body | Longer reading sessions, wider screens |
| Web (mobile) | 1.4-1.5 body | Smaller viewport, less text per line |
| iOS | 1.4-1.5 body | System default is tighter |
| Android | 1.4-1.5 body | Material Design guidelines |
| Email | 1.5-1.7 body | Email clients render inconsistently; generous leading is safer |
| Print | 1.3-1.5 body | Higher DPI, ink spread, narrower columns |

---

## Practical Implementation

### CSS custom properties setup

```css
:root {
  /* Type scale — fixed rem */
  --fs-xs: 0.75rem;
  --fs-sm: 0.875rem;
  --fs-base: 1rem;
  --fs-md: 1.125rem;
  --fs-lg: 1.5rem;
  --fs-xl: 2rem;
  --fs-2xl: 2.5rem;
  --fs-3xl: 3.5rem;

  /* Fluid scale — brand */
  --fs-hero: clamp(3rem, 2rem + 4vw, 5rem);
  --fs-brand-lg: clamp(2rem, 1.5rem + 2.5vw, 3.5rem);
  --fs-brand-md: clamp(1.5rem, 1.25rem + 1.5vw, 2rem);
  --fs-brand-body: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);

  /* Weights */
  --fw-regular: 400;
  --fw-medium: 500;
  --fw-semibold: 600;
  --fw-bold: 700;

  /* Line heights */
  --lh-display: 1.0;
  --lh-heading: 1.15;
  --lh-subhead: 1.25;
  --lh-body: 1.5;
  --lh-small: 1.4;
}
```
