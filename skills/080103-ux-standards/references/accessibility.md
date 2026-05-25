# Accessibility Reference (WCAG)

Deep reference for WCAG compliance, ARIA patterns, focus management, and screen reader support.

---

## Contrast Ratios

### Calculating Contrast
Relative luminance formula (WCAG 2.1):
```
L = 0.2126 * R + 0.7152 * G + 0.0722 * B
```
where R, G, B are sRGB values linearized:
```
if (channel <= 0.04045):
  channel = channel / 12.92
else:
  channel = ((channel + 0.055) / 1.055) ^ 2.4
```
Contrast ratio = `(L1 + 0.05) / (L2 + 0.05)` where L1 is lighter, L2 is darker.

### Required Ratios

| SC | Normal Text | Large Text (≥18px bold / ≥24px) | UI Components | AAA Normal |
|---|---|---|---|---|
| 1.4.3 (AA) | 4.5:1 | 3:1 | — | — |
| 1.4.6 (AAA) | 7:1 | 4.5:1 | — | — |
| 1.4.11 (AA) | — | — | 3:1 | — |

### Non-Text Contrast (SC 1.4.11)
- UI components and graphical objects (icons, chart lines, focus indicators) must have 3:1 against adjacent colors
- States: hover, focus, pressed, selected must be distinguishable
- Disabled elements are exempt from contrast requirements

```ts
function hexToRgb(hex: string): [number, number, number] {
  const val = parseInt(hex.replace('#', ''), 16);
  return [(val >> 16) & 255, (val >> 8) & 255, val & 255];
}

function relativeLuminance([r, g, b]: [number, number, number]): number {
  const [sr, sg, sb] = [r, g, b].map(c => {
    const s = c / 255;
    return s <= 0.04045 ? s / 12.92 : ((s + 0.055) / 1.055) ** 2.4;
  });
  return 0.2126 * sr + 0.7152 * sg + 0.0722 * sb;
}

function contrastRatio(fg: string, bg: string): number {
  const l1 = relativeLuminance(hexToRgb(fg));
  const l2 = relativeLuminance(hexToRgb(bg));
  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);
  return (lighter + 0.05) / (darker + 0.05);
}
```

### Color Blindness Simulation
- Protanopia (red-blind, ~1% male): red/green confusion, perceive yellows/blues
- Deuteranopia (green-blind, ~6% male): similar to protanopia
- Tritanopia (blue-blind, rare): blue/yellow confusion
- Simulate with CSS filters or tools like Stark, Colorblindly

```css
/* Protanopia simulation */
.cvd-protanopia {
  filter: url('data:image/svg+xml,...') /* or use a library */
}
```

---

## Focus Management

### Focus Indicators
```css
/* Custom focus ring using box-shadow (doesn't clip border-radius) */
*:focus-visible {
  box-shadow: 0 0 0 3px var(--color-focus-ring);
  outline: none;
}

/* Mouse click should NOT show focus ring (browser default behavior with :focus-visible) */
*:focus:not(:focus-visible) {
  outline: none;
  box-shadow: none;
}
```

### Focus Trapping (Modals)
```ts
function trapFocus(container: HTMLElement, previousActive: HTMLElement | null) {
  const focusable = container.querySelectorAll<HTMLElement>(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  const first = focusable[0];
  const last = focusable[focusable.length - 1];

  container.addEventListener('keydown', (e) => {
    if (e.key !== 'Tab') return;
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  });

  first?.focus();

  return () => {
    previousActive?.focus();
  };
}
```

### Focus on Route Change
```ts
function focusOnRouteChange(headingId: string = 'main-heading') {
  const heading = document.getElementById(headingId);
  if (heading) {
    heading.setAttribute('tabindex', '-1');
    heading.focus({ preventScroll: true });
    // Remove tabindex after focus so it doesn't stay in tab order
    heading.addEventListener('blur', () => {
      heading.removeAttribute('tabindex');
    }, { once: true });
  }
}
```

---

## ARIA Patterns

### Landmarks (SC 1.3.1)
```html
<header role="banner">
  <nav aria-label="Main">…</nav>
</header>
<main role="main" id="main-content">
  <h1>Page title</h1>
  …
</main>
<aside role="complementary" aria-label="Related articles">…</aside>
<footer role="contentinfo">…</footer>
```

### Dynamic Content
```html
<!-- Toast / live region -->
<div role="status" aria-live="polite" aria-atomic="true">
  <!-- Updated content: screen reader announces changes -->
</div>

<!-- Error alert -->
<div role="alert">
  <!-- Error message: immediate announcement, no user action needed -->
</div>

<!-- Progress bar -->
<div role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100" aria-label="Upload progress">
  60%
</div>
```

### Tabs Pattern
```html
<div role="tablist" aria-label="Settings">
  <button role="tab" aria-selected="true" aria-controls="panel-1" id="tab-1">General</button>
  <button role="tab" aria-selected="false" aria-controls="panel-2" id="tab-2">Security</button>
</div>
<div role="tabpanel" id="panel-1" aria-labelledby="tab-1">…</div>
<div role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden>…</div>
```
Keyboard: Arrow keys to switch tabs, Home/End for first/last.

### Disclosure / Accordion
```html
<button aria-expanded="false" aria-controls="content-1">Section title</button>
<div id="content-1" role="region" aria-labelledby="…" hidden>…</div>
```

### Combobox / Autocomplete
Use `role="combobox"`, `aria-expanded`, `aria-activedescendant`, `role="listbox"`, `role="option"`.

---

## Keyboard Navigation (SC 2.1)

### Tab Order
- Use semantic HTML to get correct tab order (`<a>`, `<button>`, `<input>`, `<select>`, `<textarea>` are inherently focusable)
- Never use positive `tabindex` values — only `0` (in order) or `-1` (programmatically focusable, not in tab order)
- Tab order matches visual reading order (left-to-right, top-to-bottom)

### Arrow Key Navigation
Custom widgets (tabs, sliders, listboxes, tree views) must use arrow keys for internal navigation, Tab to enter/exit the widget:

```ts
function handleTabKeydown(e: KeyboardEvent, items: HTMLElement[]) {
  const current = document.activeElement as HTMLElement;
  const idx = items.indexOf(current);

  if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
    e.preventDefault();
    const next = items[(idx + 1) % items.length];
    next.focus();
  } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
    e.preventDefault();
    const prev = items[(idx - 1 + items.length) % items.length];
    prev.focus();
  }
}
```

### Escape & Close
- Escape: dismiss modals, popovers, dropdowns, menus
- Escape: cancel in-progress interactions (e.g., dragging, editing)
- Escape: close autocomplete/combo lists

---

## Form Accessibility

### Labels
```html
<!-- Correct: label with for attribute -->
<label for="name">Full name</label>
<input id="name" name="name" autocomplete="name" />

<!-- Correct: aria-label -->
<input aria-label="Search" type="search" />

<!-- Correct: aria-labelledby -->
<h2 id="section-title">Shipping Address</h2>
<input aria-labelledby="section-title name-label" id="name" />

<!-- Wrong: placeholder-only -->
<input placeholder="Full name" />
```

### Error Association
```html
<div class="field" role="group" aria-labelledby="email-label">
  <label id="email-label" for="email">Email</label>
  <input
    id="email"
    type="email"
    aria-describedby="email-hint email-error"
    aria-invalid="true"
    required
    autocomplete="email"
  />
  <p id="email-hint" class="hint">We'll never share your email</p>
  <p id="email-error" class="error" role="alert">Enter a valid email address</p>
</div>
```

### Required Fields
```css
.required::after {
  content: ' *';
  color: var(--color-error);
}
```
Add `aria-required="true"` to required inputs.

---

## Reduced Motion (SC 2.3.3)

```css
/* Complete reduced motion reset */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

For animations that require motion but should still exist:
```css
@media (prefers-reduced-motion: no-preference) {
  .fade-in {
    animation: fadeIn 0.3s ease;
  }
}
@media (prefers-reduced-motion: reduce) {
  .fade-in {
    opacity: 1; /* immediately visible */
  }
}
```

---

## Screen Reader Testing

### What to test
1. Navigate page by Tab (interactive elements)
2. Navigate by headings (H key in VoiceOver/NVDA)
3. Navigate by landmarks (W key in NVDA)
4. Navigate by form fields (F key in NVDA)
5. Test dynamic content updates (toast, live regions)
6. Test modal open/close focus behavior
7. Test error announcement

### Common Issues
| Issue | Fix |
|---|---|
| Missing alt text | Add descriptive `alt` |
| Non-semantic div/span clickable | Use `<button>` or `<a>` |
| Missing form labels | Add `<label>` or `aria-label` |
| No skip link | Add skip-to-content |
| Dynamic content not announced | Add `aria-live` region |
| Focus not managed in modals | Trap focus, return on close |
| Tab order broken | Fix DOM order, remove positive tabindex |
| Heading levels skipped | Renumber headings sequentially |

---

## Testing Tools

| Tool | Use |
|---|---|
| axe DevTools | Automated audit in browser |
| Lighthouse | Built-in Chrome a11y audit |
| VoiceOver (macOS) | `Cmd+F5` to enable |
| NVDA (Windows) | Free screen reader |
| TalkBack (Android) | Android screen reader |
| Colour Contrast Analyser | Pick colors, check ratios |
| Stark | Figma/Sketch plugin |
| Pa11y | CI integration |
