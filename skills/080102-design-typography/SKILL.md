---
name: 080102-design-typography
description: >-
  Comprehensive guide to typography, spacing, and layout for frontend design.
  Covers font selection methodology, modular type scales, 4/8pt spacing systems,
  grid theory, and visual hierarchy for both brand and product UI contexts.
---

# Design Typography, Spacing & Layout

## 1. Font Selection

### Procedure

1. **Write 3 concrete brand-voice words** — physical objects, not abstract qualities. If the brand were a room, what objects would be in it? "Terrazzo floor, brass lamp, leather journal" — never "elegant, modern, clean."

2. **List the 3 reflex fonts** — the typefaces that immediately come to mind for those words. Common reflex fonts below.

3. **Reject them.** The reflex pick is the tired mainstream choice. Move past it.

4. **Browse a real catalog** (Google Fonts, Fontsource, Velvetyne, Future Fonts) with the 3 words as filters. Look at pages 2-5, not the first result.

5. **Cross-check** that the final pick doesn't match the original reflex list.

### Reflex-reject font list

These fonts are banned from consideration — they are the default choices of designers who stopped looking:

| Font | Why rejected |
|---|---|
| Fraunces | The "soft serif" darling of 2020-2023. Every DTC brand used it. |
| Newsreader | Fraunces' quieter cousin. Still oversaturated. |
| Lora | The default serif on every "minimal blog" theme. |
| Crimson / Crimson Pro / Crimson Text | Academic-poster default. Overused in editorial. |
| Playfair Display | The "luxury" go-to. Instantly recognizable as default. |
| Cormorant / Cormorant Garamond | Playfair's artier sibling. Still in every coffee shop brand. |
| Syne | The "tech-forward" variable font. Used everywhere. |
| IBM Plex Mono / Sans / Serif | The "we think about design" corporate default. |
| Space Mono / Space Grotesk | Developer-presentation default. |
| Inter | The "we're a serious product" sans. Legible but tired. |
| DM Sans / DM Serif Display / DM Serif Text | Google's own editorial family. Oversaturated. |
| Outfit | The "rounded modern" default for soft brands. |
| Plus Jakarta Sans | Outfit's more refined cousin. Still everywhere. |
| Instrument Sans / Instrument Serif | The 2024 default. Already saturated. |

### Reflex-reject aesthetic lanes

Even if you avoid the specific fonts above, whole aesthetic directions become reflex when saturated. Reject these too:

- **Editorial-typographic**: Display serif heading + mono body + ruled horizontal separators + generous leading. Looks like every "design publication" since 2019.
- **Brutalist-utility**: System-ui stack + black borders + no decoration + massive type. Tired tech-brand minimalism.
- **Acid-maximalism**: Warped type, variable-axis distortion, chaotic color, retro-future. Saturated in creative-agency portfolios.

### Pairing strategies by genre

| Genre | Strategy | Example pattern |
|---|---|---|
| Editorial / long-form / luxury | Display serif for headings + sans for body. Contrast of voice. | Fraunces refused → try Söhne-like sans + Garibaldi |
| Tech / dev / fintech | One committed sans family with strong weight contrast (200-900). | Inter refused → try Uncut Sans, Departure Mono |
| Consumer / food / travel | Warmer pairs. Sans body with humanist details + serif for accent. | Satoshi + Domaine Display, or General Sans + Tiempos |
| Creative studios | Rule-breaking. Mono + display, or one variable axis across all. | Helvetica Now + plain serif, or single family pushed |

### One family > timid pair

When you are unsure, commit to one strong family instead of a safe display+body pair that says nothing. A single well-chosen family with enough weight and width axes can do more than two mediocre fonts that "go well together."

---

## 2. Type Scale

### Modular scale concept

A type scale is a sequence of font sizes that increase by a constant ratio. The ratio ensures visual harmony across the interface.

- Standard ratios: 1.25 (major third), 1.333 (perfect fourth)
- Minimum ratio for visible difference: **1.25**
- Base size: typically 16px (1rem) for body text

### Fluid vs fixed scales

| Context | Approach | Why |
|---|---|---|
| Brand surfaces (hero, marketing pages) | Fluid `clamp()` | Scales gracefully across viewports without breakpoint jumps |
| Product UI (dashboards, forms, tables) | Fixed `rem` | Predictable, testable, accessible. No unexpected text size changes |

**Fluid formula:**

```css
/* Target: 48px at 375px viewport → 80px at 1440px viewport */
--font-size-hero: clamp(3rem, 2.5rem + 3vw, 5rem);
```

General pattern: `clamp(<min>, <preferred>, <max>)` where preferred is `(<min_in_rem> + <max_minus_min_in_vw/vw_at_scaling_viewport>)`.

### Example scale (product UI, fixed rem)

| Token | Value | Usage |
|---|---|---|
| --fs-xs | 0.75rem (12px) | Captions, metadata |
| --fs-sm | 0.875rem (14px) | Body small, form labels |
| --fs-base | 1rem (16px) | Body text, paragraphs |
| --fs-md | 1.125rem (18px) | Large body, intro text |
| --fs-lg | 1.5rem (24px) | Subheadings |
| --fs-xl | 2rem (32px) | Section headings |
| --fs-2xl | 2.5rem (40px) | Page headings |
| --fs-3xl | 3.5rem (56px) | Hero titles |

### Weight hierarchy

- **Headings**: 600-700 (semibold to bold)
- **Body**: 400 (regular)
- **Labels**: 500 (medium)
- **Captions**: 400 or 500 depending on context

### Light text on dark backgrounds

Dark-on-light contrast is sharper than light-on-dark at the same weight. Compensate:

- Increase line-height by **0.05-0.1** (e.g., from 1.5 to 1.6)
- Prefer weight 450-500 over 400 for body text on dark backgrounds
- Avoid thin weights (100-300) on dark — they become illegible

---

## 3. Spacing Systems

### 4pt / 8dp incremental system

The foundational spacing unit is 4px. All spacing values are multiples of 4px:

```
 4px  → 0.25rem
 8px  → 0.5rem
12px  → 0.75rem
16px  → 1rem    (base unit)
20px  → 1.25rem
24px  → 1.5rem
32px  → 2rem
40px  → 2.5rem
48px  → 3rem
64px  → 4rem
80px  → 5rem
96px  → 6rem
```

Deviation from 4px only when optical alignment demands it (e.g., centering an icon inside a 44px touch target — use 2px offset).

### Semantic spacing tokens

```css
:root {
  --space-xs:  0.25rem;   /*  4px — micro-adjustments */
  --space-sm:  0.5rem;    /*  8px — tight gaps */
  --space-md:  1rem;      /* 16px — default */
  --space-lg:  1.5rem;    /* 24px — section gaps */
  --space-xl:  2rem;      /* 32px — between sections */
  --space-2xl: 3rem;      /* 48px — major sections */
  --space-3xl: 4rem;      /* 64px — page-level */
  --space-4xl: 6rem;      /* 96px — hero spacing */
}
```

### Rhythm through contrast

Good spacing is not uniform distance — it is **pattern**:

```
Too uniform:  [Card]  16px  [Card]  16px  [Card]  16px  [Card]
Better:      [Card]  32px  [Card]  32px  [Card]
               |--- 16px gap within card ---|
```

The principle: **tight groupings + generous separations**. Elements that belong together are visually bound by tighter spacing. The separation between groups uses a visibly larger step.

### When to use tight vs generous spacing

| Context | Density | Reason |
|---|---|---|
| Data tables, dashboards | Tight (--sm to --md) | Minimize scrolling, compare many values |
| Settings forms | Moderate (--md to --lg) | Scan-and-fill |
| Marketing landing pages | Generous (--lg to --3xl) | Breathe, direct attention |
| Article body | Generous leading (1.6-1.8 line-height) | Readability |
| Mobile navigation | Tight (--sm to --md) | Screen efficiency |

### Container width consistency

- Content containers: `max-w-6xl` (72rem / 1152px) or `max-w-7xl` (80rem / 1280px)
- Article / reading containers: `max-w-prose` (65ch)
- Full-width brand sections intentionally break the container
- Consistent container width across pages = familiarity. Change only when content demands it.

---

## 4. Grid & Layout

### Grid theory: Flex vs Grid

| Technique | When to use |
|---|---|
| **Flexbox** | 1-dimensional layouts. Items in a row or column. Wrapping lists, nav bars, centering, small component layouts. |
| **CSS Grid** | 2-dimensional layouts. Aligning rows AND columns. Page-level layout, card grids, dashboard sections. |
| **Named grid areas** | Complex layouts with distinct zones (sidebar, header, main). Map template areas in `grid-template-areas` for self-documenting layouts. |

### Visual hierarchy through space + weight alone

Good hierarchy needs no color or decoration. Apply the **squint test**: blur your eyes at the page — the most prominent element should be the most important. If a secondary element catches your eye first, spacing or weight is wrong.

Hierarchy tools (in order of preference):

1. **Space** — more space around an element elevates its importance
2. **Weight** — heavier weight demands attention before lighter
3. **Size** — larger type draws the eye
4. **Color** — decorative, not structural

### Responsive breakpoints

```css
/* Mobile-first base: 375px+ */
/* Tablet:           768px+ */
/* Desktop:         1024px+ */
/* Wide:            1440px+ */
```

Rule: **don't add breakpoints for every device.** Four is enough. Each breakpoint should solve a real layout problem (collapse sidebar, reflow cards, resize type).

### Mobile-first: core content first

Mobile layout forces prioritization. On mobile:

- Show core content first (the reason the user is on this page)
- Scroll secondary content below the fold
- Navigation collapses to a hamburger / bottom nav
- Cards stack vertically, single column

Don't "hide" content on mobile. Reorder it.

### Line length

- Mobile: **35-60 characters** per line
- Desktop: **60-75 characters** per line
- Use `max-width: 65ch` on text containers
- Longer lines reduce readability — the eyes get lost returning to the next line

### Cards are the lazy answer

Cards are the default layout pattern of every framework and every developer. Before reaching for a card:

- **Ask**: does this item need a container, or can it breathe as a flat list?
- **Ask**: is the visual separation from the background necessary, or is whitespace enough?
- **When cards help**: heterogeneous content (mixed media, text, images), interactive items (clickable panels), dashboard widgets
- **When cards hurt**: homogeneous lists, dense data displays, long-form reading

### Don't wrap everything in a container

A centered `max-w-6xl` container on every page creates monotony. Let some sections go full width. Let an image bleed to the edge. Trust the content to define the edge, not the container.

---

## 5. Product UI Specifics

### Predictable grids = affordance

Users of product interfaces (dashboards, admin panels, financial tools) expect predictability. Surprising layouts erode trust.

- Use consistent column counts
- Keep gutters uniform
- Align all elements to the grid

### Consistent densities

- Choose a density: comfortable (generous) or compact (tight)
- Apply it consistently across all surfaces
- Offer a density toggle for power users (spreadsheets, data dashboards)

### Familiar navigation patterns

- Sidebar for multi-section apps, top bar for simple tools
- Don't invent new navigation paradigms for product UI
- Breadcrumbs on 3+ level pages

### Responsive behavior is structural, not fluid

In product UI:

- **Collapse** the sidebar to icons, then to a hamburger
- **Stack** table columns or switch to a list view
- **Never** use fluid `clamp()` typography in dense product UIs
- **Fixed rem** type scale keeps layouts predictable

### System fonts are legitimate

For product UI, system font stacks are often the best choice:

```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
  'Helvetica Neue', Arial, sans-serif;
```

Advantages: Zero load time, native rendering, consistent with OS, no CLS from font swap. Pair a system font body with a distinct heading font for character.

---

## 6. Brand UI Specifics

### Asymmetric compositions

Brand surfaces (landing pages, heroes, about pages) should not be perfectly symmetric. Asymmetry creates tension, guides the eye, and feels designed.

- Offset the hero image from center
- Let text align differently on alternating sections
- Break the grid deliberately for emphasis

### Fluid spacing with `clamp()`

Brand sections should not jump between discrete spacing values at breakpoints. Use fluid spacing:

```css
--section-padding: clamp(3rem, 2rem + 4vw, 8rem);
```

This scales smoothly from mobile to desktop.

### Intentional grid-breaking for emphasis

- Let a key element (testimonial, CTA, hero image) span beyond the grid
- Align one element edge to the center while another goes full bleed
- The break must look deliberate, not like a mistake

### Rhythm through contrast

Brand rhythm is about variety: tight section followed by generous section, dark section after light, dense text followed by open space. The contrast itself creates energy.

### One well-chosen family > timid display + body pair

A single typeface with enough axes (weight, width, optical size) can express more range than two mediocre faces that "pair well." Before adding a second family, push the first one harder.
