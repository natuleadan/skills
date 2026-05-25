# Spacing Systems Reference

## The 4pt / 8dp System

The 4pt base unit is the industry standard for digital interfaces. All spacing values are multiples of 4px (0.25rem).

### Why 4pt?

1. **Divisibility**: 4 divides evenly into most screen widths (375 / 4 = 93.75, 1440 / 4 = 360).
2. **Optical tolerance**: At 4px increments, the human eye perceives smooth, continuous spacing changes.
3. **Icon alignment**: Most icon sets (phosphor, tabler, lucide) use 16, 20, 24, 32px bounding boxes — all multiples of 4.
4. **Cross-platform consistency**: 4pt maps cleanly to iOS (points), Android (dp), and web (rem at 16px base).

### The complete spacing scale

```css
:root {
  --space-0:   0px;
  --space-1:   0.25rem;  /*  4px */
  --space-2:   0.5rem;   /*  8px */
  --space-3:   0.75rem;  /* 12px */
  --space-4:   1rem;     /* 16px — base unit */
  --space-5:   1.25rem;  /* 20px */
  --space-6:   1.5rem;   /* 24px */
  --space-7:   1.75rem;  /* 28px */
  --space-8:   2rem;     /* 32px */
  --space-9:   2.25rem;  /* 36px */
  --space-10:  2.5rem;   /* 40px */
  --space-11:  2.75rem;  /* 44px */
  --space-12:  3rem;     /* 48px */
  --space-14:  3.5rem;   /* 56px */
  --space-16:  4rem;     /* 64px */
  --space-20:  5rem;     /* 80px */
  --space-24:  6rem;     /* 96px */
}
```

### When to break the 4pt rule

- **Optical centering**: An icon inside a 44px touch target may need 2px (not 4px) offset to appear centered.
- **Type-specific**: Descender clearance may need fractional rem values.
- **Existing design system**: If you're working within Material Design (8dp grid), use 8px increments.
- Never break the rule for "it looked better" — adjust in rare, documented exceptions.

---

## Semantic Spacing Tokens

Raw numeric spacing values (`--space-4`) encode magnitude. Semantic tokens encode **purpose**. Use both: the token tells you how much, the semantic token tells you why.

```css
:root {
  /* Micro spacing — subtle adjustments */
  --space-stack-xs:  0.25rem;  /* Stack: very tight */
  --space-inline-xs: 0.25rem;  /* Inline: icon to text */
  --space-inset-xs:  0.25rem;  /* Padding: badge */

  /* Tight spacing — dense UI */
  --space-stack-sm:  0.5rem;   /* Stack: label to input */
  --space-inline-sm: 0.5rem;   /* Inline: between chips */
  --space-inset-sm:  0.5rem;   /* Padding: compact button */

  /* Default spacing — most UI */
  --space-stack-md:  1rem;     /* Stack: heading to paragraph */
  --space-inline-md: 1rem;     /* Inline: between cards */
  --space-inset-md:  1rem;     /* Padding: card content */

  /* Generous spacing — section separation */
  --space-stack-lg:  1.5rem;   /* Stack: between form groups */
  --space-inline-lg: 1.5rem;   /* Inline: between sections */
  --space-inset-lg:  1.5rem;   /* Padding: generous card */

  /* Section spacing — major boundaries */
  --space-section:   3rem;     /* Between page sections */
  --space-page:      4rem;     /* Page top/bottom padding */
  --space-hero:      6rem;     /* Hero section padding */
}
```

### Shorthand utility approach (Tailwind-style)

```css
/* Stack (vertical) */
.stack-xs > * + * { margin-block-start: 0.25rem; }
.stack-sm > * + * { margin-block-start: 0.5rem; }
.stack-md > * + * { margin-block-start: 1rem; }
.stack-lg > * + * { margin-block-start: 1.5rem; }
.stack-xl > * + * { margin-block-start: 2rem; }
.stack-2xl > * + * { margin-block-start: 3rem; }
.stack-3xl > * + * { margin-block-start: 4rem; }

/* Inline (horizontal) */
.inline-xs > * + * { margin-inline-start: 0.25rem; }
.inline-sm > * + * { margin-inline-start: 0.5rem; }
.inline-md > * + * { margin-inline-start: 1rem; }
.inline-lg > * + * { margin-inline-start: 1.5rem; }
.inline-xl > * + * { margin-inline-start: 2rem; }
```

---

## Density Guidelines

### Density levels

| Density | Base unit | Best for |
|---|---|---|
| Comfortable | 16px (--space-4) | Consumer apps, reading, marketing |
| Default | 12px (--space-3) | Most web apps |
| Compact | 8px (--space-2) | Data tables, dashboards, power tools |
| Touch | 12px minimum (--space-3) | Mobile, any touch target |

### Choosing density

**When to go comfortable**:
- Consumer-facing interfaces (users scan, don't read every element)
- Long-form content (reading needs breathing room)
- Brand/landing pages (spacing conveys quality)

**When to go compact**:
- Data-dense displays (spreadsheets, logs, monitoring)
- Internal tools (productivity over polish)
- Power user interfaces (users work fast, know the layout)

**When to offer a toggle**:
- Applications with both casual and power users
- Admin panels used 8+ hours/day
- Let users choose and persist preference

---

## Rhythm Through Contrast

### The Principle

Uniform spacing everywhere is monotonous. Rhythm comes from **variation** — tight groups separated by generous space.

### Bad rhythm (uniform)

```
┌──────────────────────────────────┐
│  Heading                         │  ← 24px bottom
│  ────────────────────────────    │
│  Body text paragraph one. This   │
│  continues into paragraph two.   │  ← 24px bottom
│  ────────────────────────────    │
│  Body text paragraph three.      │
│  This continues into paragraph   │  ← 24px bottom
│  ────────────────────────────    │
│  [Button]                        │
└──────────────────────────────────┘
```

Everything is evenly spaced. Nothing stands out. The eye has no guidance.

### Good rhythm (contrast)

```
┌──────────────────────────────────┐
│  Heading                         │
│  ────────────────────────────    │  ← 8px (tight — heading belongs to body)
│  Body text paragraph one. This   │
│  continues seamlessly into the   │
│  next paragraph because they     │  ← 24px (generous — different section)
│  are the same thought.           │
│                                  │
│  ────────────────────────────    │
│  Body text paragraph three is    │
│  a separate point. You can feel  │
│  the break.                      │  ← 12px (moderate — call to action is related)
│  [Button]                        │
└──────────────────────────────────┘
```

### Rhythm techniques

1. **Lobotomized owl selector** (`* + *`) for consistent stack spacing, then override for specific groupings
2. **Section padding contrast**: alternate generous (--space-16) and moderate (--space-8) section padding
3. **Zebra pattern**: alternating light/dark sections naturally create rhythmic separation
4. **Cluster + isolate**: group related items tightly (--space-2), separate groups generously (--space-8)
5. **The 3-step rule**: use exactly 3 spacing sizes in any viewport — tight (stack), default (group), generous (section)

---

## Container Width Consistency

### Standard container widths

| Container | Max-width | Usage |
|---|---|---|
| `max-w-xs` | 20rem (320px) | Narrow sidebar, detail panel |
| `max-w-sm` | 24rem (384px) | Form container |
| `max-w-md` | 28rem (448px) | Modal, card max |
| `max-w-lg` | 32rem (512px) | Single-column article |
| `max-w-xl` | 36rem (576px) | Medium-width content |
| `max-w-2xl` | 42rem (672px) | Blog post |
| `max-w-3xl` | 48rem (768px) | Article body |
| `max-w-4xl` | 56rem (896px) | Wide content |
| `max-w-5xl` | 64rem (1024px) | Page content |
| `max-w-6xl` | 72rem (1152px) | Default page container |
| `max-w-7xl` | 80rem (1280px) | Wide layout, marketing |

### Container strategy

**For product UI**:
- Use ONE consistent container width across authenticated pages (`max-w-6xl` or `max-w-7xl`)
- Full-width sections (header, footer) intentionally break the container
- Consistent container = familiar layout = faster user orientation

**For brand / marketing**:
- Alternate between contained sections (`max-w-6xl`) and full-width sections
- Let some sections bleed — hero, testimonial carousel, CTA
- The container break itself becomes a design tool

### When not to use a container

```
❌ Every section wrapped in <div class="mx-auto max-w-6xl">
✅ Sections that need focus use the container
✅ Sections that need impact break out of it
```

Not everything needs a container:
- Hero images that span edge-to-edge
- Background color sections that bleed full width (content can still be contained)
- Decorative elements that live in the gutter

---

## Practical Patterns

### Card spacing

```css
.card {
  padding: var(--space-inset-md);
  display: flex;
  flex-direction: column;
  gap: var(--space-stack-sm);
}

.card__title {
  margin: 0;
}

.card__body {
  /* Stack paragraphs within card */
  > * + * {
    margin-block-start: var(--space-stack-xs);
  }
}

.card__actions {
  margin-block-start: var(--space-stack-md);
  display: flex;
  gap: var(--space-inline-sm);
}
```

### Form spacing

```css
.form-group + .form-group {
  margin-block-start: var(--space-stack-lg);  /* Separates form groups */
}

.form-label {
  margin-block-end: var(--space-stack-xs);    /* Label hugs input */
}

.form-input {
  padding: var(--space-inset-sm);             /* Compact input padding */
}

.form-hint {
  margin-block-start: var(--space-stack-xs);  /* Hint hugs input */
  font-size: var(--fs-sm);
}
```

### Page layout

```css
.page {
  max-width: 72rem;       /* max-w-6xl */
  margin-inline: auto;
  padding-inline: var(--space-inset-lg);      /* 1.5rem gutters */
  padding-block: var(--space-page);           /* 4rem top/bottom */
}

.page-section + .page-section {
  margin-block-start: var(--space-section);   /* 3rem between sections */
}
```
