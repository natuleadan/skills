# Accessibility (a11y) Lesson

Make code accessible to all users: keyboard navigation, screen readers, semantic HTML.

## Semantic HTML

Use semantic elements instead of divs with ARIA roles:

```html
<!-- ✅ GOOD: Semantic -->
<button type="button">Submit</button>
<nav aria-label="Main"></nav>
<main></main>
<header></header>
<footer></footer>

<!-- ❌ BAD: ARIA on non-semantic -->
<div role="button" onclick="submit()">Submit</div>
<div role="navigation"></div>
<div role="main"></div>
```

## ARIA Attributes

Use ARIA for non-semantic interactions:

```html
<!-- ✅ GOOD: ARIA labels -->
<button aria-label="Close menu">×</button>
<div aria-hidden="true">decorative</div>
<ul aria-label="Products" role="list">
  <li role="listitem">Product 1</li>
</ul>

<!-- ❌ BAD: Missing labels -->
<button>×</button> <!-- What does this do? -->
<div role="navigation"></div> <!-- No label -->
```

## Keyboard Navigation

All interactive elements must work with keyboard:

```tsx
// ✅ GOOD: Keyboard + click handlers
<button
  onClick={handleClick}
  onKeyDown={(e) => e.key === 'Enter' && handleClick()}
>
  Click me
</button>

// ✅ GOOD: Tab order
<input type="text" tabIndex={0} />
<button tabIndex={1}>Submit</button>

// ❌ BAD: Click-only
<div onClick={handleClick}>Click me</div>

// ❌ BAD: Disabled keyboard nav
<button tabIndex={-1}>Can't tab here</button>
```

## Screen Reader Support

Provide meaningful text for screen readers:

```html
<!-- ✅ GOOD: Meaningful alt text -->
<img src="chart.png" alt="Sales Q1:$50k Q2:$75k Q3:$100k" />
<a href="/products" aria-label="Browse all products">Products</a>

<!-- ❌ BAD: Generic/missing alt -->
<img src="chart.png" alt="chart" />
<img src="icon.svg" /> <!-- No alt text -->
<a href="/products">Click here</a> <!-- Generic link text -->
```

## Labels & Form Fields

Connect labels to inputs:

```html
<!-- ✅ GOOD: Associated labels -->
<label for="email">Email:</label>
<input type="email" id="email" />

<label>
  Remember me
  <input type="checkbox" />
</label>

<!-- ❌ BAD: Unassociated labels -->
<label>Email:</label>
<input type="email" />

<span>Remember me</span>
<input type="checkbox" />
```

## Color & Contrast

Don't rely on color alone; use text + icons:

```css
/* ✅ GOOD: Text + color */
.error { color: red; }
.error::before { content: "⚠ "; }

/* ❌ BAD: Color only */
.error { color: red; } /* Red-blind users can't see it */
```

## Anti-Patterns

| ❌ WRONG | ✅ RIGHT |
|---------|---------|
| `<div role="button">` | `<button>` |
| `aria-hidden="true"` on focusable | Remove `aria-hidden` or don't focus |
| Missing `alt` on images | Always include meaningful alt text |
| No `for` on labels | `<label for="id">` → `<input id="id">` |
| Generic link text: "Click here" | Descriptive: "View products" |
| Keyboard trap | Always allow Tab/Escape to exit |

## Tools

- **axe DevTools** — Chrome extension for a11y testing
- **WAVE** — Web accessibility checker
- **Lighthouse** — Built-in accessibility audit
- **ESLint plugin** — `@eslint-react/a11y`
