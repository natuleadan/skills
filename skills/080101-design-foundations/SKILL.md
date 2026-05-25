---
name: 080101-design-foundations
description: "Design foundations: color theory, token hierarchy, brand vs product registers, theming decisions. OKLCH color space, color strategies, absolute bans, slop test."
---

# Design Foundations

## Color Strategy Framework

Four levels on the commitment axis from least to most opinionated:

### Restrained
Tinted neutrals with a single accent color covering ≤10% of surfaces. Use for product UI, data-heavy apps, tools, and interfaces where content must lead. The accent appears only on interactive elements: links, buttons, focus states.

```
Neutral background: oklch(96% 0.005 280)
Neutral surface:    oklch(93% 0.008 280)
Neutral text:       oklch(25% 0.015 280)
Accent:             oklch(55% 0.18 260)
```

The accent never fills large areas. No hero sections in accent. No accent backgrounds on cards.

### Committed
One saturated color occupies 30–60% of surfaces. Choose this when the brand needs to be felt throughout the experience—a SaaS landing page, a creative portfolio, a branded checkout. The color appears on navigation bars, section backgrounds, primary buttons, and key illustrations.

```
Primary surface:  oklch(45% 0.17 260)
Primary text:     oklch(90% 0.04 260)
Neutral surface:  oklch(93% 0.008 280)
Neutral text:     oklch(25% 0.015 280)
```

The risk is visual fatigue. Balance with generous negative space and neutral breathing room.

### Full Palette
Three to four named color roles—primary, secondary, accent, and sometimes tertiary—each with distinct jobs in the system. Use for complex brand ecosystems that need expressive range: editorial platforms, design tools, multi-brand dashboards.

```
Primary:   oklch(45% 0.17 260)    — navigation, headings
Secondary: oklch(55% 0.14 180)    — supporting sections, tags
Accent:    oklch(60% 0.19 30)     — CTAs, highlights, badges
Neutral:   oklch(25% 0.015 280)   — body text
```

Every color must earn its role. If a color only appears once, eliminate it.

### Drenched
The surface IS the color. Background and primary are the same hue at different lightness levels. Used for immersive brand experiences: a flagship storefront, a campaign microsite, a brand film landing page.

```
Background:  oklch(35% 0.15 260)
Surface:     oklch(40% 0.16 260)
Text:        oklch(90% 0.04 260)
Accent:      oklch(70% 0.2 40)    — small, high-chroma relief
```

Drenched is hostile to reading. Only use when the goal is feeling, not scanning. Never on dashboards, settings, or data tables.

---

## The Scene Sentence Method

Write one sentence describing the physical context of use. This determines dark vs light mode, contrast requirements, and ambient color decisions.

```
"A developer writes SQL at 2am in a dim bedroom with a single monitor."
→ Dark mode required. Low contrast ratios. Desaturated chroma. Warm tint to reduce blue light strain.
```

```
"A photographer edits prints in a north-facing studio with daylight-balanced LEDs."
→ Light mode required. High contrast. Neutral gray with no hue cast. Precise chroma rendering.
```

```
"A warehouse worker scans barcodes on a handheld terminal outdoors in direct sunlight."
→ Light mode. Extreme contrast. High-chroma accent for readability. Matte finish (not relevant to color, but affects perceived contrast).
```

```
"A couple browses vacation packages on a couch in a living room at golden hour."
→ Flexible. Offer both modes. Medium contrast. Warm-leaning neutrals. Restrained or Committed palette depending on brand ambition.
```

If the scene sentence could be answered either way, you haven't written enough detail. Add who, where, ambient light, mood, and task duration.

---

## OKLCH Color Space

### Why OKLCH

OKLCH is perceptually uniform: the same chroma value produces the same perceived saturation regardless of hue. HSL is not uniform—it compresses yellow and inflates blue. OKLCH fixes this.

### Chroma at Extremes

Chroma behaves differently at high and low lightness:

- **High lightness (L > 90%)**: Chroma quickly becomes invisible. A pastel with `chroma 0.02` is near-white. To get a visible pastel, push chroma to 0.04–0.06.
- **Low lightness (L < 20%)**: Chroma collapses. A dark blue with `chroma 0.12` at L=15% looks nearly black. Dark colors need higher relative chroma to register than light colors.
- **Mid lightness (L 40–70%)**: Chroma is fully expressive. This is where saturated colors live.

### Why Never Use #000 or #fff

- `#000` (oklch(0% 0 none)) creates uncomfortable contrast against any light surface—it simulates an abyss, not a shadow.
- `#fff` (oklch(100% 0 none)) is equally harsh. It causes eye strain in dark mode and feels sterile in light mode.
- Instead, compute your lightest and darkest from your neutral hue at L=2–5% and L=95–98%.

```css
--color-black: oklch(3% 0.008 280);
--color-white: oklch(97% 0.005 280);
```

The 3% vs 97% split gives a soft, natural contrast that is easier to read.

### Tinting Neutrals Toward Brand Hue

Neutrals are never truly neutral. Tint them toward your brand hue at 5–10% of the brand's chroma:

```css
--neutral-50:  oklch(99% 0.002 260);
--neutral-100: oklch(95% 0.004 260);
--neutral-200: oklch(90% 0.006 260);
--neutral-700: oklch(40% 0.012 260);
--neutral-800: oklch(30% 0.015 260);
--neutral-900: oklch(20% 0.018 260);
```

Lower chroma on the light end (0.002–0.006), slightly higher on the dark end (0.012–0.018). This keeps the tint subtle—the user should not consciously perceive the hue, only feel that the neutrals are "warm" or "cool."

---

## Design Token Hierarchy

### Brand Tokens (Abstract)

Raw values that express the brand's material properties. Never used directly in components.

```css
--brand-hue: 260;
--brand-chroma-primary: 0.18;
--brand-chroma-accent: 0.22;
--brand-font-display: "Instrument Serif", serif;
--brand-font-body: "Inter", sans-serif;
--brand-radius-sm: 4px;
--brand-radius-md: 8px;
--brand-easing-enter: cubic-bezier(0.16, 1, 0.3, 1);
```

### Semantic Tokens (Purpose)

Transformed brand tokens into functional roles. This is the layer used by component authors.

```css
--color-surface: oklch(96% 0.005 var(--brand-hue));
--color-text-primary: oklch(25% 0.015 var(--brand-hue));
--color-border-subtle: oklch(88% 0.008 var(--brand-hue));
--color-brand-primary: oklch(45% var(--brand-chroma-primary) var(--brand-hue));
--font-heading: var(--brand-font-display);
--font-body: var(--brand-font-body);
--space-stack: 16px;
--space-inline: 12px;
--shadow-card: 0 1px 3px oklch(0% 0 0 / 10%);
```

### Component Tokens (Specific)

Aliases that map semantic tokens to specific component parts. Only used within component scope.

```css
.button {
  --_bg: var(--color-brand-primary);
  --_color: var(--color-text-inverse);
  --_border: var(--color-border-subtle);
  --_radius: var(--brand-radius-md);
  --_padding: var(--space-stack) var(--space-inline);
}

.card {
  --_bg: var(--color-surface);
  --_shadow: var(--shadow-card);
  --_radius: var(--brand-radius-sm);
}
```

---

## Two Registers

### Brand Register (Design IS the Product)

Brand register is for surfaces where the design itself communicates brand value: marketing landing pages, campaign microsites, "about us" pages, product launch hubs, seasonal promotions. The work is the message.

Rules: opinionated typography (display fonts, expressive scale), committed or drenched color strategy, liberal motion and animation, full editorial layout freedom, experimental interactions.

### Product Register (Design SERVES the Product)

Product register is for surfaces where the design enables function: app dashboards, admin panels, data tables, settings screens, checkout flows, onboarding wizards. The work disappears behind the task.

Rules: restrained or committed color strategy, system fonts or restrained one-family design, fixed scale (not fluid), tight ratios, minimal motion (only functional feedback), standard affordances, accessibility first.

### When They Conflict

When brand register and product register meet—a marketing page inside an app, an app-like tool on a campaign site—the interaction designer chooses which register wins for that specific user flow. A settings page inside a brand landing page still follows product register. A promotional banner inside a dashboard still follows brand register.

---

## Absolute Bans

These apply to both registers:

- **Side-stripe borders**: A colored bar along the left edge of a card or section. It is a CSS demo from 2015, not a design decision.
- **Gradient text**: Illusionary depth on type. Reduces readability universally. If you need visual interest on headings, use typographic weight or letter-spacing.
- **Glassmorphism as default**: Frosted glass backgrounds work for exactly one use case—overlays on photography. Using it as a card style is a trend artifact.
- **Hero-metric template**: Big headline + subdued subheading + two-column feature grid + CTA. This is not a layout; it is a reflex.
- **Identical card grids**: Three cards in a row, same size, same padding, same icon position. Your content is not that uniform. Let the layout respond to content shape.
- **Modal as first thought**: Before reaching for a modal, ask: could this be a page? An inline section? A side panel? Modal as default is a UX failure.
- **Nested cards**: A card inside a card. If you need to group things, use a section with a subtle background, not another card.

---

## The Slop Test

### First-Order Reflex (Category → Theme)

The designer maps a content category directly to a pre-existing visual theme without questioning fit:

```
"E-commerce → dark mode + neon accents + glass cards"
"Fintech → blue gradient hero + security badges + clean sans"
"SaaS → white + green buttons + illustrated characters"
```

How to check: for any design decision, ask "What would this look like if I reversed the most obvious expectation?" If the answer is terrible, you are not designing—you are pattern-matching.

### Second-Order Reflex (Category → Aesthetic Lane)

More subtle. The designer picks an aesthetic lane based on category alone:

```
"Health/wellness → Calm: pastels, rounded corners, ample whitespace, organic shapes"
"Developer tool → Hacker: dark mode, monospace elements, terminal aesthetics, muted green accents"
"Creative agency → Bold: full-bleed images, asymmetric grids, expressive typography, high contrast"
```

The category gives you constraints, not a costume. A developer tool could use high-chroma restrained palette with system fonts and generous spacing—not because Notion does, but because the tool's users spend 10 hours inside it.

### The Category-Reflex Check Process

1. Name the category (e.g., "fitness tracking app")
2. Identify your reflex theme explicitly (e.g., "neon green on dark, angular typography, progress rings")
3. Write it down—this is what you must argue against
4. Derive from context, not category: who uses it? Where? For how long? In what state of mind?
5. Only keep a reflex choice if it survives the context test

---

## Brand Register Specifics

### Typography

Font selection procedure:
1. Define the brand voice in three words (e.g., "sharp, warm, precise")
2. Evaluate typefaces against voice, not against category convention
3. Test the typeface in its intended context: at small sizes, as headings, in long paragraphs
4. If you cannot articulate why this font and not another, reject it

Reflex-reject list (banned training-data fonts): Montserrat, Open Sans, Lato, Poppins, Raleway, Nunito, Ubuntu, Roboto (for brand work; Roboto is acceptable in product register), Playfair Display, Merriweather, Source Sans Pro.

Aesthetic lane rejection: if a font choice maps directly to "this is a [category] font," reject it. The font should serve the voice, not the genre.

### Color

Strategy per brand: choose the commitment level from the four-tier framework based on how much of the story the color must carry. A brand with strong typography and illustration can afford Restrained. A brand with no other visual assets needs Committed or Drenched.

### Scale

Use a modular, fluid clamp() scale with a ratio of at least 1.25:

```css
--text-xs:  clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);
--text-sm:  clamp(0.875rem, 0.8rem + 0.375vw, 1rem);
--text-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
--text-lg:  clamp(1.125rem, 1rem + 0.625vw, 1.375rem);
--text-xl:  clamp(1.25rem, 1.1rem + 0.75vw, 1.75rem);
--text-2xl: clamp(1.5rem, 1.3rem + 1vw, 2.25rem);
--text-3xl: clamp(1.75rem, 1.5rem + 1.25vw, 3rem);
```

The fluid range tightens on small screens and opens on large screens. The minimum ratio between any two steps is 1.25.

---

## Product Register Specifics

### System Fonts Are Legitimate

In product register, system fonts (`system-ui, -apple-system, sans-serif`) are not a compromise—they are the correct choice for interfaces where reading speed and familiarity matter more than personality. A single well-chosen font family is preferable to a multi-font system.

### One-Family Design

Product register uses one typeface family for everything: headings, body, UI labels, code if possible. Weight and size create hierarchy, not font switching. If a second font is necessary (e.g., for monospace), it is the only exception.

### Fixed rem Scale (Not Fluid)

```css
--text-xs:  0.75rem;
--text-sm:  0.875rem;
--text-base: 1rem;
--text-lg:  1.125rem;
--text-xl:  1.25rem;
--text-2xl: 1.5rem;
--text-3xl: 1.875rem;
```

No viewport units. Product UI does not need to scale with screen width. Use container queries for component-level adjustments if needed.

### Tighter Scale Ratio (1.125–1.2)

Product register uses a minor-third to major-second ratio. The steps are closer together than in brand register because hierarchy in product UI is flatter—a heading is rarely more than 2x the body size.

### State-Rich Semantic Vocabulary

Product register needs distinct tokens for every interactive state:

```css
--color-bg-primary: oklch(45% 0.18 260);
--color-bg-primary-hover: oklch(48% 0.19 260);
--color-bg-primary-active: oklch(40% 0.17 260);
--color-bg-primary-disabled: oklch(80% 0.08 260);

--color-text-primary: oklch(25% 0.015 280);
--color-text-secondary: oklch(45% 0.012 280);
--color-text-disabled: oklch(70% 0.008 280);
```

Hover, active, disabled, focus, selected, error, success, warning—each needs its own token chain.

### Restrained as Floor

Product register starts at Restrained. You may escalate to Committed if the product demands it, but you must justify the escalation. Full Palette and Drenched are almost never appropriate for product UI.

### Second Neutral Layer for Sidebars

Product registers with persistent navigation need a second neutral surface to differentiate sidebar from main content:

```css
--color-surface:      oklch(97% 0.005 260);
--color-surface-raised: oklch(99% 0.003 260);
--color-surface-sidebar: oklch(93% 0.008 260);
```

The sidebar surface is darker (lower lightness) than the main content surface. This creates hierarchy without using a brand color.

---

## Product Bans

On top of the shared absolute bans:

- **Decorative motion**: Animations that serve no functional purpose—bouncing icons, spinning loaders when content loads in under 200ms, parallax on dashboard cards. Motion in product register must communicate state change, not personality.
- **Inconsistent component vocabulary**: The same visual pattern (a dropdown, a tag, a button) rendered differently in different parts of the app because two developers built similar components independently. Enforce one vocabulary per pattern.
- **Display fonts in UI labels**: A decorative typeface used for button text, form labels, or table headers. Display fonts are for editorial headings only.
- **Reinventing standard affordances**: Custom scrollbars (unless for brand register), custom selects that behave worse than native, drag handles that require discovery. Users have learned the OS patterns—do not unteach them.
- **Heavy color on inactive states**: A disabled button with full brand color. Inactive states should fade to neutral with reduced opacity or chroma. The visual weight must communicate non-interactivity.

---

## References

- `references/color-strategies.md` — Deep dive into the four color strategies with before/after examples
- `references/token-hierarchy.md` — Design token naming, organization, and CSS custom property architecture
- `references/brand-product-register.md` — Full comparison of brand vs product registers with slop tests
