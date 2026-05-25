---
name: 080103-ux-standards
description: "Use this skill whenever you need to design, review, or critique user interfaces for accessibility, touch interaction, form UX, navigation, UX writing, or cognitive load. Also trigger when the user asks about WCAG compliance, keyboard navigation, focus management, screen reader support, touch targets, gesture design, form validation patterns, error recovery, progressive disclosure, navigation architecture, deep linking, back stack management, bottom nav, breadcrumbs, UX copy, error messages, empty states, CTAs, confirmation dialogs, information density, chunking, visual hierarchy, squint test, heuristic evaluation, or UX review checklists. Do NOT trigger for graphic design, illustration, brand identity, or marketing copy."
---

# UX Standards

This skill provides comprehensive standards for user experience design across web and mobile applications. Use it to ensure accessibility, interaction quality, form design, navigation, and copywriting meet production-grade requirements.

## How to use this skill

1. Determine which UX domain(s) the task involves
2. Read this SKILL.md for the high-level checklist and standards
3. Read the relevant reference file(s) for deep guidance, code examples, and platform specs

---

## Section 1: Accessibility (CRITICAL)

Read `references/accessibility.md` for WCAG ratios, ARIA patterns, focus trapping code, and screen reader testing.

### Checklist
- [ ] Color contrast: AA 4.5:1 normal / 3:1 large text. AAA 7:1 for enhanced
- [ ] Never communicate via color alone — add icons, patterns, or text
- [ ] Visible focus ring on `:focus-visible` (2–4px, 3:1 contrast against background)
- [ ] All interactive elements keyboard accessible (Enter, Space, Escape, Arrows)
- [ ] Tab order matches visual reading order (no positive `tabindex`)
- [ ] Skip link as first focusable element
- [ ] Heading hierarchy: sequential `h1`→`h6`, no level skip
- [ ] Alt text on meaningful images, `alt=""` or `role="presentation"` on decorative
- [ ] `aria-label` on icon-only buttons
- [ ] Form labels: `<label>` with `for` attribute (never placeholder-only)
- [ ] `aria-describedby` for helper text, `aria-invalid` on errors
- [ ] Error messages: `role="alert"`. Toasts: `aria-live="polite"`, no focus steal
- [ ] Modals: close button + Escape + backdrop dismiss + focus trap + return focus on close
- [ ] `prefers-reduced-motion` respected (animation-duration: 0.01ms)
- [ ] Do NOT override system keyboard shortcuts (Cmd+W, Cmd+T, F5, F12, etc.)
- [ ] Focus moves to `<h1>` or main content on route change

---

## Section 2: Touch & Interaction (CRITICAL)

Read `references/touch-interaction.md` for platform specs, gesture design, haptic feedback, and safe areas.

### Checklist
- [ ] Touch targets: min 44×44pt (Apple) / 48×48dp (Material). Extend hit area with `::before`
- [ ] 8px minimum spacing between touch targets
- [ ] Do not rely on `:hover` — essential actions must work with tap alone
- [ ] Buttons disabled + spinner during async operations
- [ ] Error feedback near the problematic field (cause + fix)
- [ ] `cursor: pointer` on clickable elements
- [ ] Press feedback (ripple, highlight, or scale) on touch
- [ ] `touch-action: manipulation` on interactive elements (removes tap delay)
- [ ] `touch-action: pan-y` on scrollable content (prevents swipe conflicts)
- [ ] Do NOT block system gestures (edge back swipe, Control Center, notification center)
- [ ] Safe area awareness: `env(safe-area-inset-*)` for notch, Dynamic Island, home indicator
- [ ] Drag threshold (~5px movement) before drag starts
- [ ] Swipe affordance: visible cues for swipeable actions
- [ ] Use haptic feedback for confirmations, avoid overuse
- [ ] Provide visible controls for critical actions (don't rely on gesture-only)

---

## Section 3: Performance & Perceived Speed

### Checklist
- [ ] Images: WebP/AVIF, `srcset`, `loading="lazy"`, declare `width`/`height`
- [ ] Fonts: `font-display: swap` or `optional`, reserve space
- [ ] Critical CSS inlined in `<head>`
- [ ] Dynamic imports for non-critical components
- [ ] Route-based code splitting
- [ ] Reserve space for async content (skeleton) to prevent CLS
- [ ] Virtualize lists with 50+ items
- [ ] Main thread budget: ~16ms per frame
- [ ] Debounce search (~300ms), throttle scroll (~100ms)
- [ ] Offline support: degraded mode with cached content

---

## Section 4: Style Selection (HIGH)

### Checklist
- [ ] Visual style matches product type (enterprise, consumer, utility)
- [ ] Consistent across pages: same components look/behave identically
- [ ] No emoji as icons — use SVG icons
- [ ] Icons: consistent stroke width and corner radius from a single set
- [ ] Consistent elevation/shadow scale (sm, md, lg, xl)
- [ ] Light and dark mode designed together (CSS custom properties)
- [ ] States: hover, pressed, focused, disabled visually distinct
- [ ] One primary CTA per screen (brand color, filled). Secondary is subordinate

---

## Section 5: Forms & Feedback (MEDIUM)

Read `references/form-ux.md` for validation timing, error patterns, autofill, multi-step flows, and mobile form design.

### Checklist
- [ ] Visible labels (never placeholder-only). Floating labels acceptable if done correctly
- [ ] Errors: below the field, role="alert", cause + how to fix
- [ ] Error summary at top with anchor links to invalid fields
- [ ] Validate on blur, not keystroke. Focus first invalid field on submit
- [ ] Submit button: loading state → success/error feedback
- [ ] Correct `type` attributes: `email`, `tel`, `number`, `url`, `password`
- [ ] `autocomplete` attributes on all common fields
- [ ] Password show/hide toggle
- [ ] Confirm before destructive actions (specify exactly what will happen)
- [ ] Undo option (time-limited toast) after destructive actions
- [ ] Unsaved changes warning on sheet/modal dismiss
- [ ] Multi-step forms: step indicator, back navigation preserves data
- [ ] Form autosave for long forms (draft to localStorage)
- [ ] `aria-describedby` for helper text
- [ ] Disabled elements: opacity 0.38–0.5 + `cursor: not-allowed`
- [ ] Touch-friendly input height ≥44px
- [ ] Toast: `aria-live="polite"`, auto-dismiss 3–5s, no focus steal

---

## Section 6: Navigation Patterns (HIGH)

Read `references/navigation-patterns.md` for navigation types, platform idioms, deep linking, and state preservation.

### Checklist
- [ ] Bottom tab bar: max 5 items, labels + icons, top-level only
- [ ] Sidebar/drawer: for secondary navigation only
- [ ] Active navigation item clearly highlighted
- [ ] Primary vs secondary navigation visually separated
- [ ] Adaptive: sidebar on large screens, bottom/top nav on small
- [ ] Every key screen reachable via URL (deep linking)
- [ ] Back navigation preserves scroll, filter, and input state
- [ ] Back stack never silently reset
- [ ] Modals: close button + Escape + swipe down (mobile). Not for primary flows
- [ ] Skip link present on every page
- [ ] Focus on route change: to main content or `<h1>`
- [ ] Consistent nav placement across all pages
- [ ] Avoid mixing Tab + Sidebar + Bottom Nav in same app
- [ ] System gesture navigation supported (no conflict)
- [ ] Overflow menu instead of cramming nav items

---

## Section 7: UX Writing & Clarity

Read `references/ux-writing.md` for detailed copy patterns, voice/tone, and formatting.

### Principles
- Every word earns its place — cut everything that doesn't serve the user
- No restated headings — the heading already tells them where they are
- No em dashes — use commas, colons, or semicolons
- Positive phrasing: "Enter at least 8 characters" not "Password too short"

### Patterns
- Error: cause + fix — "Enter a valid email (e.g., user@example.com)"
- Empty state: why + what to do — "No products yet — add your first product"
- CTA: specific verbs — "Create account", not "Submit"
- Confirmation: specify exactly what happens + scope + reversibility
- Success: brief and action-specific — "Changes saved", not "Success!"

---

## Section 8: Critique & Review

Read `references/cognitive-load.md` for information density, chunking, progressive disclosure, and decision fatigue.

### The Squint Test
Half-close your eyes. Does the primary action pop? Is hierarchy clear? Does anything compete for attention that shouldn't?

### Heuristic Scoring (1–5)
| Heuristic | Score | Must Fix < 3 |
|---|---|---|
| Visibility of system status | | |
| Match system & real world | | |
| User control & freedom | | |
| Consistency & standards | | |
| Error prevention | | |
| Recognition over recall | | |
| Flexibility & efficiency | | |
| Aesthetic & minimalist design | | |
| Help recognize/diagnose/recover from errors | | |
| Help & documentation | | |

### Pre-Delivery Checklist

- [ ] All interactive elements keyboard accessible
- [ ] Focus order matches visual order
- [ ] Touch targets ≥44px with adequate spacing
- [ ] Color contrast passes AA (4.5:1 normal, 3:1 large)
- [ ] No information conveyed by color alone
- [ ] Meaningful alt text on images
- [ ] Labels visible on all form fields
- [ ] Errors near field, cause + fix, error summary at top
- [ ] Submit shows loading state
- [ ] Navigation: active state visible, label + icon
- [ ] Inputs use correct semantic `type`
- [ ] Back navigation preserves state
- [ ] Deep links work for all key screens
- [ ] Empty states have helpful content + action
- [ ] CTAs are specific verbs
- [ ] Modals have close + Escape + backdrop + focus trap
- [ ] System gesture navigation not blocked
- [ ] `prefers-reduced-motion` respected
- [ ] Skip link present
- [ ] Toasts use `aria-live="polite"`, no focus steal

### Systematic Improvement

1. Surface the actual problem, not the symptom (users abandon at step 3 → no progress indicator + vague error message)
2. Ask: "What is the user trying to accomplish right now?"
3. Isolate: is it cognitive (unclear), physical (hard to tap), or emotional (anxiety)?
4. Propose the simplest change that removes friction
5. Validate with squint test before and after
