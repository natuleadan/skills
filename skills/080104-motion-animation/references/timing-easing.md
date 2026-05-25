# Timing & Easing Reference

## Timing Values by Interaction Type

| Interaction Type | Duration | Context |
|---|---|---|
| **Micro-interaction** | 150-200ms | Button press, toggle, checkbox, like, heart |
| **Micro-interaction (feedback)** | 80-150ms | Press scale, highlight, ripple |
| **Simple transition** | 200-300ms | Hover state, card expand, collapse |
| **Complex transition** | 300-400ms | Panel slide, modal open, page element enter |
| **Page transition** | ≤400ms | Route change, full-view transition |
| **Exit (close/dismiss)** | 120-200ms | Modal close, drawer dismiss, toast dismiss |
| **Stagger per item** | 30-50ms | List enter, grid enter, table row reveal |
| **Overlay fade** | 200-300ms | Backdrop/overlay appear |
| **Drawer / side panel** | 250-350ms | Slide from edge |
| **Skeleton entrance** | 400-600ms | Skeleton shimmer/pulse |

### Platform-specific standards

| Platform | Micro-interaction | Transition | Exit |
|---|---|---|---|
| **Apple HIG** | 150-300ms | 300-400ms | 150-200ms |
| **Material Design** | 100-200ms | 200-350ms | 150-200ms |
| **Fluent (Microsoft)** | 100-200ms | 200-300ms | 100-167ms |

## Easing Curves

### CSS cubic-bezier values

```css
/* DECELERATION — ease-out (entering) */
--ease-out-quad:  cubic-bezier(0.25, 0.46, 0.45, 0.94);
--ease-out-cubic: cubic-bezier(0.215, 0.61, 0.355, 1);
--ease-out-quart: cubic-bezier(0.25, 0.46, 0.45, 0.94);
--ease-out-quint: cubic-bezier(0.23, 1, 0.32, 1);
--ease-out-expo:  cubic-bezier(0.19, 1, 0.22, 1);

/* ACCELERATION — ease-in (exiting) */
--ease-in-quad:  cubic-bezier(0.55, 0.085, 0.68, 0.53);
--ease-in-cubic: cubic-bezier(0.55, 0.055, 0.675, 0.19);
--ease-in-quart: cubic-bezier(0.5, 0, 0.75, 0);
--ease-in-quint: cubic-bezier(0.755, 0.05, 0.855, 0.06);
--ease-in-expo:  cubic-bezier(0.7, 0, 0.84, 0);

/* STANDARD — symmetrical */
--ease-in-out:   cubic-bezier(0.76, 0, 0.24, 1);
```

### Recommended defaults

| Usage | Curve |
|---|---|
| Enter (appear, open, expand) | `ease-out-quint` or `ease-out-expo` |
| Exit (close, dismiss, collapse) | `ease-in-quart` or `ease-in-quint` |
| Hover / active state | `ease-out-quart`, 150-200ms |
| Shared element transition | `ease-in-out`, 300-400ms |
| Page transition | `ease-out-expo`, ≤400ms |
| Spring equivalent (JS) | `{ type: 'spring', stiffness: 300, damping: 30 }` |

### JavaScript equivalents (Framer Motion / GSAP)

```js
// Framer Motion
const easeOutQuint = [0.23, 1, 0.32, 1];
const easeInQuint  = [0.755, 0.05, 0.855, 0.06];
const easeInOut    = [0.76, 0, 0.24, 1];

// Spring
const springConfig = { type: "spring", stiffness: 300, damping: 30, mass: 1 };

// GSAP
gsap.to(el, { duration: 0.3, ease: "power4.out" });       // ease-out-quint
gsap.to(el, { duration: 0.2, ease: "power2.out" });       // ease-out-quart
gsap.to(el, { duration: 0.15, ease: "back.out(1.7)" });   // slight overshoot
```

## Curves by Platform

### Apple (iOS / macOS)
- **Foundation**: `ease-out` for entering, `ease-in` for exiting, material feeling
- **Spring**: `CASpringAnimation` with damping ~20, stiffness ~150 for icons, overlays
- **Custom**: No bounce. Smooth, deliberate, predictable
- **Standard curve (UIKit)**: `UIView.AnimationOptions.curveEaseOut`
- **Spring (UIKit)**:
  ```swift
  UIView.animate(
    withDuration: 0.4,
    delay: 0,
    usingSpringWithDamping: 0.78,
    initialSpringVelocity: 0.5
  )
  ```

### Material (Android / Web)
- **Foundation**: Asymmetric — fast in, slow out (ease-in-out with emphasis)
- **Standard curve**: `cubic-bezier(0.4, 0, 0.2, 1)`
- **Deceleration (enter)**: `cubic-bezier(0, 0, 0.2, 1)`
- **Acceleration (exit)**: `cubic-bezier(0.4, 0, 1, 1)`
- **Sharp**: `cubic-bezier(0.4, 0, 0.6, 1)` — for exit anims that need emphasis

```css
/* Material Design curves */
--mat-standard:    cubic-bezier(0.4, 0, 0.2, 1);
--mat-decelerate:  cubic-bezier(0, 0, 0.2, 1);
--mat-accelerate:  cubic-bezier(0.4, 0, 1, 1);
--mat-sharp:       cubic-bezier(0.4, 0, 0.6, 1);
```

### Fluent (Windows / Web)
- **Foundation**: Fast, crisp, purposeful
- **Control fast**: `cubic-bezier(0, 0, 1, 1)` — linear-ish for 100-150ms
- **Reveal**: `cubic-bezier(0, 0, 0.3, 1)` — decelerate
- **Dismiss**: `cubic-bezier(0.1, 0, 1, 1)` — accelerate
- **Fluent motion** favors faster durations (100-200ms) and minimal easing

## Utility: timing scale (CSS custom properties)

```css
:root {
  /* Duration */
  --duration-instant: 0ms;
  --duration-fast:   100ms;
  --duration-normal: 200ms;
  --duration-slow:   300ms;
  --duration-slower: 400ms;

  /* Easing */
  --ease-enter:  cubic-bezier(0, 0, 0.2, 1);
  --ease-exit:   cubic-bezier(0.4, 0, 1, 1);
  --ease-both:   cubic-bezier(0.4, 0, 0.2, 1);
  --ease-spring: cubic-bezier(0.23, 1, 0.32, 1);
}
```

## Duration comparison chart

```
Micro (80-150ms)    [=======]
Input feedback       [=====]
Touch press          [=====]

Micro (150-200ms)   [=============]
Button / toggle      [=============]
Checkbox             [=============]

Simple (200-300ms)  [===================]
Hover                [======]
Card expand          [===================]
Collapse             [=============]

Complex (300-400ms) [===========================]
Panel slide          [===========================]
Modal enter          [===========================]
Page enter           [===========================]

Exit (120-200ms)    [=========]
Modal close          [=========]
Toast dismiss        [=====]
Drawer dismiss       [===========]

Page (≤400ms)       [=============================]
Route change         [=============================]
Layout shift         [=============================]

Stagger (30-50ms)   [=]
Per item             [=]
```

## Key takeaways

1. **150-300ms** is the sweet spot for micro-interactions on all platforms
2. **Never exceed 500ms** for any UI transition
3. **Exit is always faster** than enter (60-70% duration)
4. **Springs over curves** for interactive elements; curves for passive transitions
5. **Material uses asymmetric curves**; Apple favors spring physics; Fluent favors speed
6. **Linear easing is never acceptable** for UI transitions
