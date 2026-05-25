# Brand Register vs Product Register

## Core Distinction

| Dimension | Brand Register | Product Register |
|-----------|---------------|-----------------|
| Relationship | Design IS the product | Design SERVES the product |
| Priority | Expression, distinction, emotion | Efficiency, clarity, familiarity |
| User mindset | Browsing, exploring, deciding | Working, completing, analyzing |
| Session duration | Seconds to minutes | Minutes to hours |
| Typography | Expressive (display + body) | One-family (system or restrained) |
| Color strategy | Committed, Full Palette, Drenched | Restrained, rarely Committed |
| Scale | Modular, fluid clamp(), ≥1.25 ratio | Fixed rem, 1.125–1.2 ratio |
| Motion | Expressive, narrative, decorative | Functional, feedback-only |
| Layout | Editorial freedom, asymmetry | Grid consistency, predictability |
| Personality | High. The brand is the experience. | Low. The data is the experience. |

---

## When to Apply Each Register

### Brand Register

Apply when the page or component is a marketing surface: its purpose is to persuade, inform, or impress, not to enable a task.

Examples: landing pages, about pages, campaign microsites, product launch hubs, seasonal promotions, brand blog hero sections, pricing page headers, case study showcases.

### Product Register

Apply when the page or component is a functional surface: its purpose is to enable the user to complete a task efficiently.

Examples: dashboards, admin panels, data tables, settings screens, checkout flows, onboarding wizards, search results, account management, notification lists, form wizards.

### Hybrid Surfaces

Some surfaces exist at the boundary. Apply a register hierarchy:

- **A settings page inside a marketing site**: Product register wins. The user is in task mode.
- **A promotional banner inside a dashboard**: Brand register wins. The goal is persuasion, not function.
- **An onboarding flow**: Product register until the last step (completion state can use brand register for celebration).
- **A pricing page**: Brand register for the header, product register for the comparison table.

---

## Brand Slop Test (Distinctiveness)

Before shipping any brand-register surface, run this test:

```
1. Cover the logo.
2. Would a visitor know which brand this is?
3. If the answer is "it could be any [category] company," the design is slop.
```

### Examples

**Fails — generic brand**: A fintech landing page with a blue gradient hero, white sans-serif headings, and a three-column feature grid. Every fintech company looks like this. The logo is the only distinguishing element.

**Passes — distinct brand**: A fintech landing page that uses high-contrast typography with a single bold weight, a restrained palette of warm charcoal and one emerald accent, and full-bleed case study imagery instead of feature cards. The brand is recognizable with the logo covered because the typographic voice and color warmth are distinctive.

### The Category-Costume Reflex

Brand register surfaces often suffer from the category-costume reflex:

```
Project management → blue + green kanban illustrations + "streamline" in headline
Coffee brand        → brown + beige + hand-drawn cup illustration + rustic font
Health app          → green + rounded everything + leaf icons + soft gradients
```

These are costumes, not identities. To pass the brand slop test, you must be able to articulate what makes the design specific to this brand, not this category.

### Fixing Brand Slop

1. Strip the category signifiers (remove the coffee cup illustration, the kanban graphic, the leaf icon)
2. Design the layout from content hierarchy, not template
3. Choose a typeface that serves the voice, not the genre
4. Apply the color strategy that fits the brand's expressive need, not the category convention

---

## Product Slop Test (Earned Familiarity)

Before shipping any product-register surface, run this test:

```
1. Show the interface to a new user for 3 seconds.
2. Remove it.
3. Ask: "What can you do here?"
4. If they cannot name the primary action, the design is slop.
```

### Examples

**Fails — confusing familiarity**: A dashboard with five card types (stats, chart, list, activity feed, notifications), all with identical padding, borders, and visual weight. The user sees a wall of equally important information. They cannot locate the primary action.

**Passes — earned familiarity**: The same dashboard with clear visual hierarchy: the primary metric uses a larger type size and a tinted surface, the chart is the central element, secondary lists are de-emphasized with lighter borders and smaller type, and the primary CTA uses the full brand button style. The user sees the same data but knows immediately what matters.

### The Template Reflex

Product register surfaces suffer from template reflex:

```
User settings page → avatar left + name + email + two-column form
Data table         → striped rows + pagination bottom + search top-right
Analytics panel    → date range picker + line chart + KPI cards row
```

These patterns are familiar because they work. The slop test is not about rejecting the pattern—it is about checking whether you applied it without considering the specific content.

### Fixing Product Slop

1. Identify the single most important action on the page and make it visually dominant
2. Group related information with proximity, not borders (reduce visual noise)
3. Use the spacing scale aggressively: the distance between groups should be noticeably larger than the distance within groups
4. Apply the second neutral layer: give the sidebar a distinct surface from the main content
5. Remove any element that survived more than three design iterations untouched (these are the zombies)

---

## Cross-Register Shared Laws

These rules apply in both registers:

### No Observed Differences

- Use the same neutral hue tint across both registers (brand hue in neutrals)
- Maintain the same contrast ratios (WCAG AA minimum, AAA preferred for body text)
- Use the same radius scale (component boundaries should feel like the same system)
- Use the same error, warning, and success colors (semantic states are not register-dependent)
- Use the same interactive state vocabulary (hover, active, disabled, focus tokens)

### Register-Switching Boundaries

When a user moves from a brand surface to a product surface within the same session (e.g., clicks "Sign up" on a landing page to enter the dashboard):

```
Landing page (brand register)
  ↓ "Get started" CTA
Signup flow (product register with elevated brand presence)
  ↓ First login
Dashboard (product register)
```

The transition should be perceptible but not jarring. The easiest way: reduce the brand color coverage gradually. The signup page uses Committed (brand is still present), the dashboard uses Restrained (brand retreats to accent role). The neutral tint and typography family stay consistent.

### When to Break the Rules

Break any shared law when:

- The brand register surface is an interstitial (loading, maintenance, error) — these should feel like the product, not the campaign
- The product register surface is a celebratory state (achievement, milestone, upgrade complete) — these earn a moment of brand register
- Accessibility requires it (a decorative brand register choice fails contrast — the accessibility requirement overrides the register rule)

---

## Register Decision Matrix

| Situation | Surface Type | Register | Rationale |
|-----------|-------------|----------|-----------|
| Visitor lands on homepage | Hero, feature sections | Brand | Persuasion goal |
| Visitor clicks "Pricing" | Comparison table, FAQ | Brand (header), Product (table) | Hybrid — table needs scannability |
| Visitor clicks "Get started" | Signup form | Product (with brand presence) | Task mode begins |
| User opens dashboard | Analytics, navigation | Product | Task mode active |
| User opens settings | Forms, toggles | Product | Task mode active |
| User reaches milestone | Celebration overlay | Brand | Emotional moment |
| User sees error page | Error state | Product | Trust restoration needed |
| Seasonal campaign launches | Campaign page | Brand | Immersion goal |
