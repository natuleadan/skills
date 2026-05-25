# Micro-interactions Reference

## Principles

Micro-interactions serve four purposes:
1. **Acknowledge** — confirm the user's action was received
2. **Feedback** — communicate the result of the action
3. **Guide** — reveal what's happening or what to do next
4. **Delight** — elevate the experience (sparingly, never at cost of utility)

## Press Feedback

### Scale press

```css
.button {
  transition: transform 150ms ease-out;
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
}

.button:hover {
  transform: translateY(-1px);
}

.button:active {
  transform: scale(0.97);
}
```

```jsx
// Framer Motion
<motion.button
  whileHover={{ scale: 1.02 }}
  whileTap={{ scale: 0.97 }}
  transition={{ type: "spring", stiffness: 400, damping: 25 }}
/>
```

### Ripple effect (Material)

```css
.ripple {
  position: relative;
  overflow: hidden;
}

.ripple::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: radial-gradient(circle, currentColor 10%, transparent 10%);
  background-position: center;
  background-repeat: no-repeat;
  background-size: 1000%;
  opacity: 0;
  transition: none;
  pointer-events: none;
}

.ripple:active::after {
  background-size: 0%;
  opacity: 0.3;
  transition: background-size 0.6s, opacity 0.6s;
}
```

### Highlight press (iOS style)

```css
.cell {
  transition: background-color 100ms ease-out;
}

.cell:active {
  background-color: rgba(0, 0, 0, 0.05);
}
```

## Loading States

### Skeleton screen

```css
.skeleton {
  background: linear-gradient(
    90deg,
    var(--skeleton-base) 25%,
    var(--skeleton-shine) 50%,
    var(--skeleton-base) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s ease-in-out infinite;
  border-radius: 4px;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* Pulse variant */
.skeleton-pulse {
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 0.4; }
  50% { opacity: 0.8; }
}
```

### Timing for skeleton visibility

```js
// Show skeleton only after 300ms delay
let timer = setTimeout(() => showSkeleton(), 300);
// If data arrives before 300ms, cancel skeleton
clearTimeout(timer);
// Once data arrives, fade out skeleton
skeleton.style.opacity = '0';
skeleton.style.transition = 'opacity 200ms ease-out';
```

### Spinner (only for brief waits)

```css
.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid var(--color-border);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
```

## Success / Error Feedback

### Input validation feedback

```css
.input-wrapper {
  transition: border-color 200ms ease-out;
}

.input-wrapper.success {
  border-color: var(--color-success);
}

.input-wrapper.error {
  border-color: var(--color-error);
  animation: shake 300ms ease-out;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-4px); }
  50% { transform: translateX(4px); }
  75% { transform: translateX(-4px); }
}
```

### Success checkmark animation

```css
.checkmark {
  stroke-dasharray: 36;
  stroke-dashoffset: 36;
  animation: drawCheck 300ms ease-out 100ms forwards;
}

@keyframes drawCheck {
  to { stroke-dashoffset: 0; }
}
```

### Error flash

```css
.error-flash {
  animation: flashError 600ms ease-out;
}

@keyframes flashError {
  0%   { background-color: var(--color-error-bg); }
  100% { background-color: transparent; }
}
```

## Toast / Notification

### Toast entrance

```css
.toast {
  transform: translateY(100%);
  opacity: 0;
  transition:
    transform 300ms ease-out,
    opacity 300ms ease-out;
}

.toast.visible {
  transform: translateY(0);
  opacity: 1;
}

.toast.exiting {
  transform: translateY(100%);
  opacity: 0;
  transition:
    transform 200ms ease-in,
    opacity 200ms ease-in;
}
```

### Stacking toasts

- When multiple toasts appear, stack with 4-8px offset
- New toast pushes existing ones up
- Exit from bottom (oldest dismisses first or user manually closes)

## Toggle / Switch Animation

```css
.switch {
  width: 44px;
  height: 24px;
  border-radius: 12px;
  background: var(--color-surface-3);
  transition: background-color 200ms ease-out;
  cursor: pointer;
  position: relative;
}

.switch[aria-checked="true"] {
  background: var(--color-primary);
}

.switch-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: white;
  position: absolute;
  top: 2px;
  left: 2px;
  transition: transform 200ms ease-out;
}

.switch[aria-checked="true"] .switch-thumb {
  transform: translateX(20px);
}
```

### With spring (JS)

```jsx
<motion.div
  className="switch-thumb"
  animate={{ x: isOn ? 20 : 0 }}
  transition={{ type: "spring", stiffness: 400, damping: 25 }}
/>
```

## Dropdown / Collapse Animation

### Accordion / Collapse

```css
.collapse-content {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows 300ms ease-out;
}

.collapse-content.open {
  grid-template-rows: 1fr;
}

.collapse-content > div {
  overflow: hidden;
}
```

### Alternative: max-height trick

```css
.collapse-content {
  max-height: 0;
  overflow: hidden;
  transition: max-height 300ms ease-out;
}

.collapse-content.open {
  max-height: 500px; /* Large enough for content */
}
```

### Dropdown menu

```css
.dropdown-menu {
  opacity: 0;
  transform: translateY(-4px);
  pointer-events: none;
  transition:
    opacity 200ms ease-out,
    transform 200ms ease-out;
}

.dropdown-menu.open {
  opacity: 1;
  transform: translateY(0);
  pointer-events: auto;
}

/* Item stagger on open */
.dropdown-menu.open > .dropdown-item {
  opacity: 0;
  animation: fadeIn 150ms ease-out forwards;
}

.dropdown-menu.open > .dropdown-item:nth-child(1) { animation-delay: 20ms; }
.dropdown-menu.open > .dropdown-item:nth-child(2) { animation-delay: 40ms; }
.dropdown-menu.open > .dropdown-item:nth-child(3) { animation-delay: 60ms; }
.dropdown-menu.open > .dropdown-item:nth-child(4) { animation-delay: 80ms; }

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-2px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

### Select / Combobox

- Open: scale from trigger, 150-200ms, ease-out
- Close: scale to trigger, 100-120ms, ease-in
- Option selection: highlight background transition 80ms

## Focus Ring Animation

```css
.focus-ring {
  outline: none;
  position: relative;
}

.focus-ring:focus-visible::after {
  content: '';
  position: absolute;
  inset: -3px;
  border-radius: inherit;
  border: 2px solid var(--color-primary);
  opacity: 0;
  animation: focusAppear 150ms ease-out forwards;
}

@keyframes focusAppear {
  from { opacity: 0; }
  to { opacity: 1; }
}

.focus-ring:focus-visible:not(:focus-visible)::after {
  animation: focusDisappear 100ms ease-in forwards;
}

@keyframes focusDisappear {
  from { opacity: 1; }
  to { opacity: 0; }
}
```

## Tabs

### Tab underline / indicator

```css
.tab-indicator {
  position: absolute;
  bottom: 0;
  height: 2px;
  background: var(--color-primary);
  transition:
    left 250ms ease-out,
    width 250ms ease-out;
}
```

### Content transition

```css
.tab-content {
  position: relative;
}

.tab-panel {
  opacity: 0;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  transition: opacity 200ms ease-out;
}

.tab-panel.active {
  opacity: 1;
  position: relative;
}
```

## Progress / Stepper

### Determinate progress bar

```css
.progress-bar {
  height: 4px;
  background: var(--color-surface-3);
  border-radius: 2px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--color-primary);
  border-radius: 2px;
  transition: width 300ms ease-out;
}
```

### Indeterminate (loading)

```css
.progress-indeterminate {
  width: 100%;
  height: 4px;
  background: var(--color-surface-3);
  overflow: hidden;
}

.progress-indeterminate::after {
  content: '';
  display: block;
  width: 40%;
  height: 100%;
  background: var(--color-primary);
  animation: indeterminate 1.4s ease-in-out infinite;
}

@keyframes indeterminate {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(350%); }
}
```

## Rating / Star Animation

```css
.star {
  transition: transform 150ms ease-out;
  cursor: pointer;
}

.star:hover {
  transform: scale(1.2);
}

.star.active {
  animation: starPop 300ms ease-out;
}

@keyframes starPop {
  0%   { transform: scale(1); }
  50%  { transform: scale(1.3); }
  100% { transform: scale(1); }
}
```

## Timing Reference (Micro-interactions)

| Interaction | Duration | Easing | Notes |
|---|---|---|---|
| Press scale | 80-150ms | ease-out | On press, not on release |
| Hover highlight | 100-200ms | ease-out | Background or elevation |
| Ripple expand | 600ms | ease-out | Continues after finger lifts |
| Toggle switch | 200ms | ease-out / spring | Thumb + track |
| Checkbox | 150-200ms | ease-out | Check mark + box fill |
| Accordion open | 250-300ms | ease-out | Height transition |
| Dropdown menu | 150-200ms | ease-out | Scale + fade from trigger |
| Toast appear | 200-300ms | ease-out | Slide in or fade |
| Toast dismiss | 150-200ms | ease-in | Reverse of appear |
| Skeleton shimmer | 1.5s | linear | Infinite loop |
| Progress fill | 300ms | ease-out | Width transition |
| Focus ring | 150ms | ease-out | Opacity + border |
| Tab indicator | 200-250ms | ease-out | Position + width |
| Star hover | 150ms | ease-out | Scale |
| Star select | 300ms | ease-out | Scale with pop |
| Input error shake | 300ms | ease-out | TranslateX oscillation |
| Success checkmark | 300ms | ease-out | Stroke dashoffset |
| Loading spinner | 600ms | linear | Infinite rotation |
| Notification badge | 200ms | spring (JS) | Scale from 0 to 1 |

## Checklist

- [ ] Press feedback within 100ms (scale, highlight, or both)
- [ ] Ripple continues through release for tactile feel
- [ ] Loading state appears only after 300ms delay
- [ ] Skeleton matches content layout (not generic)
- [ ] Success/error feedback clear within 200ms
- [ ] Toggle animates thumb AND track background
- [ ] Dropdown scales from trigger position
- [ ] Accordion animates height smoothly (grid or max-height)
- [ ] Focus ring visible and animated
- [ ] Tab indicator follows active tab with transition
- [ ] Toast stack pushes older toasts up
- [ ] All micro-interactions interruptible
- [ ] All micro-interactions respect reduced-motion
