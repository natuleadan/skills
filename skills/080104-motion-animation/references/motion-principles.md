# Motion Principles Reference

## Physics-Based Animation

Spring-based animation models real-world physics: mass, stiffness, damping, velocity. This produces more natural motion than cubic-bezier curves because it accounts for momentum.

### Key parameters

| Parameter | Effect | UI Range |
|---|---|---|
| **Stiffness** | Resistance to deformation | 100 (soft) — 500 (stiff) |
| **Damping** | Energy dissipation, settling speed | 10 (bouncy) — 50 (overdamped) |
| **Mass** | Inertia of the animated object | 0.5 (light) — 2 (heavy) |
| **Velocity** | Initial speed from gesture | Auto (derived from gesture velocity) |

### Common spring presets

```js
// Framer Motion
const spring = {
  type: "spring",
  stiffness: 300,   // default
  damping: 30,      // default
  mass: 1,
};
```

| Preset | Stiffness | Damping | Use case |
|---|---|---|---|
| Gentle | 100-150 | 15-20 | Large elements, panels, overlays |
| Default | 250-350 | 25-35 | Standard UI transitions |
| Snappy | 400-500 | 35-45 | Micro-interactions, press feedback |
| Overdamped | 400-600 | 50-60 | Dismiss, exit, no-bounce required |
| Underdamped | 150-250 | 10-15 | Brand reveal, decorative (avoid in UI) |

### CSS vs spring

CSS cubic-bezier cannot replicate spring overshoot natively. For spring-like overshoot in CSS:

```css
/* Simulated spring overshoot using keyframes */
@keyframes springUp {
  0%   { transform: translateY(100%); opacity: 0; }
  60%  { transform: translateY(-5%); }
  80%  { transform: translateY(2%); }
  100% { transform: translateY(0); opacity: 1; }
}
```

For true spring behavior, use JavaScript: Framer Motion, GSAP, React Spring, or Motion One.

## Spatial Continuity

Navigation direction must reflect the user's mental model of the interface hierarchy.

### Direction mapping

| Navigation | Direction | Meaning |
|---|---|---|
| Forward (drill-down) | Left or Up | Going deeper into content |
| Back (pop) | Right or Down | Returning to overview |
| Tab switch | No direction | Content crossfade only |
| Modal open | Scale from trigger | Originating from the tapped element |
| Drawer open | From edge (left/right/bottom/top) | Existing in the margins |

### CSS directional transition

```css
/* Forward: content slides in from right, current slides out left */
.page-enter-forward {
  animation: slideInRight 300ms ease-out;
}
.page-exit-forward {
  animation: slideOutLeft 200ms ease-in;
}

/* Back: content slides in from left, current slides out right */
.page-enter-back {
  animation: slideInLeft 300ms ease-out;
}
.page-exit-back {
  animation: slideOutRight 200ms ease-in;
}

@keyframes slideInRight {
  from { transform: translateX(30%); opacity: 0; }
  to   { transform: translateX(0); opacity: 1; }
}
@keyframes slideOutLeft {
  from { transform: translateX(0); opacity: 1; }
  to   { transform: translateX(-30%); opacity: 0; }
}
@keyframes slideInLeft {
  from { transform: translateX(-30%); opacity: 0; }
  to   { transform: translateX(0); opacity: 1; }
}
@keyframes slideOutRight {
  from { transform: translateX(0); opacity: 1; }
  to   { transform: translateX(30%); opacity: 0; }
}
```

## Shared Element Transitions

Shared element (hero) transitions create visual continuity between two views that share content (e.g., a product card → product detail page).

### Principles

1. Identify the shared visual: image, heading, avatar
2. Morph position, size, and border-radius simultaneously
3. Crossfade non-shared content around the hero element
4. Duration: 300-400ms with ease-in-out
5. Both elements must exist in the DOM simultaneously during transition

### CSS approach (View Transitions API)

```css
/* View Transitions API (Chrome 111+, Safari 18+) */
::view-transition-old(root) {
  animation: 300ms ease-out both exit;
}
::view-transition-new(root) {
  animation: 300ms ease-out both enter;
}

@keyframes exit {
  to { opacity: 0; transform: scale(0.95); }
}
@keyframes enter {
  from { opacity: 0; transform: scale(1.05); }
}

/* Named view transition for shared element */
.product-card {
  view-transition-name: product-hero;
}
```

### Framer Motion shared layout

```jsx
// Both components must share the same layoutId
function ProductCard({ id }) {
  return (
    <motion.div layoutId={`product-${id}`} layout="position">
      <motion.img layoutId={`product-img-${id}`} src={product.image} />
      <motion.h3 layoutId={`product-title-${id}`}>{product.name}</motion.h3>
    </motion.div>
  );
}
```

## Hierarchy Through Motion

Direction and timing establish visual hierarchy:

| Direction | Perceived relationship |
|---|---|
| Enter from below | Deeper level, subordinate content |
| Enter from above | Parent, higher-level context |
| Enter from right | Forward, next step in sequence |
| Enter from left | Backward, previous step |
| Scale up from center | Expanding to reveal detail |
| Scale down and fade | Closing or dismissing |

### Timing hierarchy

- Primary content animates first (fastest, 150-200ms)
- Secondary content follows (200-300ms)
- Decorative/ambient content animates last (300-400ms)
- Never exceed 500ms total from first to last element

## Reduced Motion Strategy

### OS-level detection

```css
/* CSS: disable all animations */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

```js
// JavaScript detection
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const shouldAnimate = !prefersReducedMotion.matches;

prefersReducedMotion.addEventListener('change', (e) => {
  shouldAnimate = !e.matches;
  // Re-render or disable/enable animations
});
```

### Implementation patterns

1. **Accessible animations** — Use `MotionConfig` (Framer Motion) or gsap.ticker to disable globally
2. **Respect system settings** — read `prefers-reduced-motion` at init, update on change
3. **Manual toggle** — provide in-app setting for users who need reduced motion but don't set OS preference
4. **Data visualization** — chart entrances should be instant when reduced motion is active
5. **Parallax** — must be fully disabled; replace with static layout
6. **Transforms** — all transform-based entrances should show the final state when reduced motion is active

```jsx
// Framer Motion — respects reduced-motion
import { MotionConfig } from 'framer-motion';

function App() {
  return (
    <MotionConfig reducedMotion="user">
      <YourRoutes />
    </MotionConfig>
  );
}
```

## Interruption Handling

All UI animations must be interruptible.

### Rules

1. **User tap cancels** any ongoing animation immediately
2. **Reverse transition** (dismiss before enter completes) must work cleanly
3. **Stagger sequences** must stop immediately — do not complete remaining items
4. **Hover-out** should cancel hover-in animation and reverse from current state
5. **Rapid interactions** (double-tap, fast swipe) — only final state matters; skip intermediate animations

### CSS interruptible transitions

```css
/* CSS transitions are interruptible by default */
.card {
  transition: transform 200ms ease-out;
}
.card:hover {
  transform: translateY(-4px);
}
.card:active {
  transform: scale(0.97);
}
/* Moving from hover→active→hover is smooth because transitions interpolate */
```

### JS animation interruption

```js
// GSAP — kill previous before new
function animateCard(el) {
  gsap.killTweensOf(el);             // interrupt any running tween
  gsap.to(el, {
    scale: 0.97,
    duration: 0.15,
    ease: 'power2.out',
    overwrite: 'auto',               // auto-overwrite on restart
  });
}

// Framer Motion — useAnimate with cancel
const [scope, animate] = useAnimate();
async function handlePress() {
  await animate(scope.current, { scale: 0.97 }, { duration: 0.1 });
  await animate(scope.current, { scale: 1 }, { duration: 0.15 });
}
// calling again cancels previous and starts new
```

## Gesture Feedback

### Touch feedback chain

```
Touch start (80-150ms)     → Visual feedback (scale/highlight)
Touch move (if drag)       → Transform follows finger, no delay
Touch end / cancel         → Return to neutral state
  if tap (≤200ms hold)     → Action + confirm animation
  if drag (distance > X)   → Snap or dismiss animation
  if cancel                 → Immediate return, no action
```

### Drag gesture physics

```js
// GSAP Draggable — match velocity for throw
Draggable.create('.card', {
  type: 'x,y',
  inertia: true,                    // applies momentum on release
  throwResistance: 3000,            // resistance value
  maxDuration: 0.5,                 // throw animation never exceeds 500ms
  onDragEnd: function() {
    if (this.endX > 200) this.disable(); // snap out
  }
});

// Framer Motion — gesture with spring
<motion.div
  drag="x"
  dragElastic={0.2}
  dragConstraints={{ left: 0, right: 0 }}
  onDragEnd={(_, info) => {
    if (info.offset.x > 100) {
      // dismiss
    }
  }}
/>
```

### Scale feedback presets

| Element | Press scale | Release scale | Easing |
|---|---|---|---|
| Button | 0.97 | 1.0 | 150ms ease-out |
| Card | 0.97 | 1.0 | 200ms ease-out |
| Thumbnail | 0.95 | 1.0 | 150ms ease-out |
| Icon button | 0.90 | 1.0 | 100ms ease-out |
| List row | 0.97 | 1.0 | 100ms ease-out |

## Haptic Integration

### When to use haptics

| Context | Haptic type | Effect |
|---|---|---|
| Confirm action | Success/notification | Heavy or rigid impact |
| Success state | Notification | Soft or medium impact |
| Error/warning | Warning/error | Rigid or heavy impact (sparingly) |
| Toggle reach limit | Selection | Tick or alignment |
| Drag snap | Alignment | Light impact |
| Pull to refresh | Medium impact | At threshold crossing |
| Swipe action | Light impact | On action threshold |

### When NOT to use haptics

- Every keypress in a keyboard
- Every scroll tick
- Generic button taps
- Non-critical notifications
- Repeated within 500ms of the last haptic
- When `prefers-reduced-motion` is active (consider disabling)

### Web Haptics API

```js
// Navigator.vibrate (limited, single pattern)
navigator.vibrate(10);              // short pulse
navigator.vibrate([20, 50, 20]);    // pattern: buzz-pause-buzz

// HapticFeedback API (iOS Safari 16.4+, Android Chrome)
if (navigator.haptics) {
  // not yet widely implemented — use platform bridge
}

// For mobile web: use platform bridge via custom events
// On iOS/Android native wrappers, postMessage or URL scheme
```

### Platform haptics

```swift
// iOS (UIKit)
let generator = UIImpactFeedbackGenerator(style: .medium)
generator.prepare()
generator.impactOccurred()

// Available styles: .light, .medium, .heavy, .soft, .rigid
// UINotificationFeedbackGenerator for success/warning/error
// UISelectionFeedbackGenerator for selection changes
```

```kotlin
// Android (HapticFeedbackConstants)
view.performHapticFeedback(HapticFeedbackConstants.CONFIRM)
view.performHapticFeedback(HapticFeedbackConstants.REJECT)

// Vibrator
val vibrator = getSystemService(Vibrator::class.java)
vibrator.vibrate(VibrationEffect.createOneShot(10, VibrationEffect.DEFAULT_AMPLITUDE))
```

## Summary: Principles Checklist

- [ ] Every animation communicates cause and effect
- [ ] Direction reflects spatial continuity (forward/back)
- [ ] Shared elements morph, not crossfade
- [ ] Reduced motion respected at OS and app level
- [ ] All animations are interruptible
- [ ] Exit is faster than enter
- [ ] Touch feedback within 100ms
- [ ] Haptics enhance, never annoy
- [ ] Scale press feedback between 0.95-0.97
- [ ] Spring for interactive, curve for passive
