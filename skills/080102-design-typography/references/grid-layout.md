# Grid & Layout Reference

## Grid Fundamentals

### Flexbox vs CSS Grid decision matrix

| Scenario | Use | Why |
|---|---|---|
| Navigation bar, toolbar | Flexbox | 1D row centering with wrapping |
| Card row that wraps | Flexbox | Natural wrapping without media queries |
| Centering a single element | Flexbox | `align-items: center; justify-content: center` |
| Page-level layout (sidebar + header + main) | CSS Grid | 2D alignment of independent regions |
| Homogeneous card grid | CSS Grid | Equal-height columns, consistent gutters |
| Dashboard with panels of different sizes | CSS Grid | Named areas for explicit placement |
| Form layout | Flexbox | Sequential flow, natural wrapping |
| Article with sidebar | CSS Grid | `grid-template-columns: 1fr 300px` |

### The rule of thumb

- If the layout flows in **one direction** (a row or column of items), use Flexbox.
- If the layout needs alignment in **two directions** (items aligned both by row AND column), use CSS Grid.

### Named grid areas (for complex layouts)

```css
.app-layout {
  display: grid;
  grid-template-areas:
    "sidebar  header"
    "sidebar  main"
    "sidebar  footer";
  grid-template-columns: 260px 1fr;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
}

.app-header  { grid-area: header; }
.app-sidebar { grid-area: sidebar; }
.app-main    { grid-area: main; }
.app-footer  { grid-area: footer; }

@media (max-width: 768px) {
  .app-layout {
    grid-template-areas:
      "header"
      "main"
      "footer";
    grid-template-columns: 1fr;
  }
  .app-sidebar {
    display: none; /* or transform off-screen with a toggle */
  }
}
```

Named areas are self-documenting. A new developer can look at `grid-template-areas` and understand the layout in 3 seconds.

---

## Breakpoint System

### The minimum viable breakpoint set

| Name | Width | Target |
|---|---|---|
| Mobile | 375px+ | Small phones |
| Tablet | 768px+ | Portrait tablets, large phones |
| Desktop | 1024px+ | Landscape tablets, small desktops |
| Wide | 1440px+ | Large desktops |

### Why not more?

- Each breakpoint adds maintenance cost and testing overhead
- Most layout problems are solved at 3-4 widths
- Additional breakpoints should solve a **specific layout failure**, not "optimize" for a device

### Mobile-first CSS

```css
/* Base: mobile (375px+) */
.page-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

/* Tablet (768px+) */
@media (min-width: 768px) {
  .page-grid {
    grid-template-columns: 1fr 1fr;
  }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
  .page-grid {
    grid-template-columns: 1fr 1fr 1fr;
  }
}

/* Wide (1440px+) — only if content demands it */
@media (min-width: 1440px) {
  .page-grid {
    grid-template-columns: 1fr 1fr 1fr 1fr;
  }
}
```

### Container queries (modern alternative)

When a component needs to respond to its **container width** rather than viewport width:

```css
@container (min-width: 400px) {
  .card-grid {
    grid-template-columns: 1fr 1fr;
  }
}

@container (min-width: 700px) {
  .card-grid {
    grid-template-columns: 1fr 1fr 1fr;
  }
}
```

Use container queries for reusable component grids that appear in different contexts.

---

## Responsive Strategy

### Mobile-first workflow

1. **Design mobile first**. The narrowest viewport forces prioritization — only the essential content fits.
2. **Add content as viewport grows**. Desktop is mobile plus breathing room, not mobile is desktop minus space.
3. **Never "hide" content on mobile**. Reorder it. If content isn't important enough for mobile, it might not be important at all.

### Layout changes per breakpoint

| Component | Mobile (375) | Tablet (768) | Desktop (1024+) |
|---|---|---|---|
| Sidebar | Off-screen / hamburger | Collapsed (icons only) | Expanded |
| Card grid | 1 column | 2 columns | 3-4 columns |
| Table | Horizontal scroll or card list | Full table | Full table |
| Navigation | Bottom bar or hamburger | Top bar | Top bar + sidebar |
| Hero | Stacked (image below text) | Side-by-side | Side-by-side or split |

### Content priority per viewport

```
Mobile:     [Core CTA] [Value prop] [Features (scroll)] [Footer]
Tablet:     [Core CTA | Image] [Value prop] [Features grid] [Footer]
Desktop:    [Header nav] [Core CTA | Hero image] [Value prop + stats] [Features grid] [Testimonial] [Footer]
```

---

## Visual Hierarchy Techniques

### The Squint Test

Blur your eyes or squint at the page. Without reading a single word, identify:

1. What is the most visually prominent element?
2. What is the second?
3. Is the order correct for the page's goal?

If a secondary element (sidebar nav, decorative image, secondary CTA) catches your eye before the primary heading or primary CTA, hierarchy is wrong.

### Hierarchy tools ranked

| Tool | Impact | Risk |
|---|---|---|
| **Space** (isolation) | High — an isolated element is inherently important | Low — harder to misuse |
| **Weight** (heavy type) | High — weight differences are immediately visible | Low — as long as body is readable |
| **Size** (font size) | Medium-high — bigger = more important | Medium — too much size variation feels chaotic |
| **Color** (accent vs muted) | Medium — color draws the eye | High — overuse creates visual noise |
| **Decoration** (border, shadow, background) | Low-medium — can add or distract | High — decoration is the most common hierarchy mistake |

### Practical hierarchy patterns

```
Strong hierarchy:
  ┌────────────────────────────┐
  │  Page Title (2rem, 700)    │  ← large, bold
  │                            │
  │  Section heading (1.25rem, │
  │  600)                      │  ← smaller, less bold
  │  Body text (1rem, 400)     │  ← small, regular
  │  Body text (1rem, 400)     │
  │                            │
  │  Section heading (1.25rem, │  ← same as above
  │  600)                      │
  │  Body text (1rem, 400)     │
  └────────────────────────────┘

Weak hierarchy (everything competes):
  ┌────────────────────────────┐
  │ Page Title (1.5rem, 600)   │  ← too close to section
  │ Section heading            │
  │ (1.25rem, 600)             │  ← same weight as title
  │ Body text (1rem, 500)      │  ← body is medium,
  │                            │     steals attention
  │ Body button                │  ← colorful button
  │ [ACCENT COLOR]             │     competes with title
  └────────────────────────────┘
```

---

## Line Length

### The 65-character rule

Optimal line length for readability is:

- **35-60 characters** on mobile
- **60-75 characters** on desktop
- **Max 90 characters** absolute maximum (user will struggle returning to next line)

### Implementation

```css
/* For text-heavy content */
article, .prose, .reading-content {
  max-width: 65ch;           /* 65 characters wide */
}

/* For wider content with defined columns */
.grid-article {
  grid-template-columns: minmax(0, 65ch) 1fr;
  /* Left column capped at readable width */
  /* Right column (sidebar) fills remaining space */
}
```

### When to break the 65ch rule

- **Data tables**: Width is determined by content, not readability
- **Code blocks**: Longer lines are expected; horizontal scroll is acceptable
- **Navigation / labels**: Short strings don't need constraint
- **Hero titles**: Can be wider by design (large type, short text)

---

## Card Components: When and When Not

### Cards are often lazy

Cards wrap content in a visible container (border, shadow, background). They are the default pattern because they're easy to implement, not because they're the best solution.

### When to use cards

| Use case | Why |
|---|---|
| Heterogeneous content | Items with mixed media (image + text + button) need containment |
| Interactive items | Each item is clickable or has its own actions |
| Dashboard widgets | Cards define independent widget boundaries |
| Article/blog grids | Cards provide consistent container for varied content lengths |

### When to avoid cards

| Alternative | When |
|---|---|
| Flat list | Homogeneous content (all text items, all same type) |
| Table | Dense structured data (sortable, filterable) |
| Simple text with dividers | Article lists, search results, comments |
| Direct grid | Items that don't need visual container — whitespace is enough |

### Card vs no-card comparison

```
Card-heavy (lazy):
┌──────┐ ┌──────┐ ┌──────┐
│ img  │ │ img  │ │ img  │
│ text │ │ text │ │ text │
└──────┘ └──────┘ └──────┘

No-cards (cleaner):
Product A     Product B     Product C
description   description   description
─── ───       ─── ───       ─── ───
$29.99        $34.99        $24.99
```

The no-card version communicates the same information with less visual noise.

---

## Container vs Fluid Approaches

### The container trap

The instinct to wrap every section in `<div class="mx-auto max-w-6xl px-4">` creates monotony. If every section looks contained, none are special.

### Hybrid container strategy

```html
<!-- Contained section — for focus -->
<section class="contained">
  <div class="container">
    <h2>Our mission</h2>
    <p>Text that needs focused reading...</p>
  </div>
</section>

<!-- Full-bleed section — for impact -->
<section class="full-bleed accent-bg">
  <div class="container">
    <h2>Numbers that matter</h2>
    <!-- Stats that should feel expansive -->
  </div>
</section>

<!-- Breaking out of container — for emphasis -->
<section class="contained">
  <div class="container">
    <h2>Featured work</h2>
  </div>
  <!-- This image bleeds past the container edge -->
  <div class="breakout">
    <img src="hero.jpg" alt="" />
  </div>
</section>
```

### Breakout pattern CSS

```css
.breakout {
  width: 100vw;
  margin-inline: calc(-50vw + 50%);
}
```

This makes an element expand to full viewport width while staying within its parent's flow. The image starts inside the container, breaks out to `100vw`, then the negative margin centers it.

---

## Practical Layout Patterns

### Dashboard grid

```css
.dashboard {
  display: grid;
  grid-template-columns: 260px 1fr;
  grid-template-rows: auto 1fr;
  grid-template-areas:
    "sidebar header"
    "sidebar main";
  min-height: 100vh;
}

@media (max-width: 768px) {
  .dashboard {
    grid-template-columns: 1fr;
    grid-template-areas:
      "header"
      "main";
  }
}
```

### Article with sidebar

```css
.article-layout {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 2rem;
  max-width: 72rem;
  margin-inline: auto;
  padding-inline: 1.5rem;
}

@media (max-width: 1024px) {
  .article-layout {
    grid-template-columns: 1fr;
  }
}
```

### Card grid (responsive, no media queries needed)

```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}
```

Auto-fill with `minmax` creates a responsive grid without a single media query. Items are at minimum 280px wide and expand to fill available space.

### Aside: avoiding containeritis

```html
<!-- Over-wrapped — every section has a container -->
<section>
  <div class="container"><!-- ... --></div>
</section>
<section class="dark">
  <div class="container"><!-- ... --></div>
</section>
<section>
  <div class="container"><!-- ... --></div>
</section>

<!-- Intentional — container only where needed -->
<section>
  <div class="container"><!-- Focused content --></div>
</section>
<section class="full-bleed dark">
  <!-- Content lives in padding, no container boundary -->
  <h2>Impact statement</h2>
</section>
<section>
  <div class="container"><!-- Focused content --></div>
</section>
```

The second approach uses the container as a deliberate tool, not a reflex.
