---
name: 080104-motion-animation
description: Motion design principles, timing, easing, physics, micro-interactions, and performance for frontend interfaces.
---

# Motion & Animation Principles

## Timing & Duration

| Context | Duration | Notes |
|---|---|---|
| Micro-interactions | 150-300ms | Apple HIG standard range |
| Complex transitions | ≤400ms | Never exceed 500ms |
| Exit (close/dismiss) | 60-70% of enter duration | Exit should feel faster |
| Stagger delay per item | 30-50ms | List/ grid entrances |
| Input feedback | ≤100ms | Visual response within 100ms of tap |
| Touch press feedback | 80-150ms | Press-scale or highlight |
| Long operations | >300ms | Show skeleton or progress indicator |

**Key rules:**
- Micro-interactions at 150-300ms (Apple HIG standard)
- Complex transitions must not exceed 400ms, never 500ms
- Exit animations are shorter than enter: ~60-70% of enter duration
- Stagger sequences: 30-50ms per item
- Input feedback must be visual within 100ms of tap
- Touch feedback: 80-150ms for press response
- Operations >300ms: show skeleton loader or progress

## Easing Curves

- **Entering (appear)**: ease-out (deceleration curve)
- **Exiting (dismiss)**: ease-in (acceleration curve)
- **Natural motion**: exponential curves — ease-out-quart, ease-out-quint, ease-out-expo
- **Preferred**: spring/physics-based over linear or cubic-bezier for natural feel
- **Avoid**: bounce or elastic curves on UI elements
- **Platform-native feel**: easing must match the platform convention
- **Never**: linear easing for UI transitions (feels robotic)

### Common CSS curves

```css
--ease-out-quart: cubic-bezier(0.25, 0.46, 0.45, 0.94);
--ease-out-quint: cubic-bezier(0.23, 1, 0.32, 1);
--ease-out-expo: cubic-bezier(0.19, 1, 0.22, 1);
--ease-in-quart:  cubic-bezier(0.5, 0, 0.75, 0);
--ease-in-out:    cubic-bezier(0.76, 0, 0.24, 1);
```

## Performance

- **Animate only** `transform` and `opacity` — never `width`, `height`, `top`, `left`
- **GPU-accelerated properties**: `transform`, `opacity`, `filter`
- **Avoid layout animations**: animating layout properties causes reflow and CLS
- **`will-change`**: use sparingly, only on currently animating elements; remove after animation
- **60fps target**: ~16ms per frame budget for all animations in the frame
- **Interruptible**: user action must immediately cancel ongoing animation
- **Never block input**: animation must never prevent user interaction

```css
/* Good — GPU composited */
.card {
  transition: transform 200ms ease-out, opacity 200ms ease-out;
}

/* Bad — causes layout thrash */
.card {
  transition: width 200ms, height 200ms, top 200ms, left 200ms;
}
```

## Motion Principles

- **Motion conveys meaning**: every animation must express cause and effect — nothing decorative
- **Spatial continuity**: directional slides for navigation — forward = left/up, back = right/down
- **Shared element transitions**: hero animations connect views visually
- **Hierarchy via direction**: enter from below = deeper level, exit upward = returning up
- **Fade vs slide**: crossfade for content replacement, slide for navigation
- **Scale feedback**: 0.95-1.05 on press for tappable cards and buttons
- **Modal motion**: animate from trigger source position (scale+fade or slide-in edge)
- **Layout shift**: animations must never cause cumulative layout shift (CLS)

## Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

- Respect `prefers-reduced-motion` in all animations
- Reduce or disable animations when requested by the OS
- Chart entrance animations must respect reduced motion
- Parallax must respect reduced motion
- Data must be readable immediately regardless of animation setting
- Provide a manual toggle in settings for users who want reduced motion

## Specific Patterns

### Loading states
- Show skeleton or progress indicator only after 300ms
- Avoid full-page spinners — prefer skeleton screens matching content layout
- Skeleton animation: shimmer or pulse at reduced opacity

### Page transitions
- Maintain spatial continuity — direction must reflect navigation intent
- Content should remain readable during transition

### List entrances
- Stagger items with 30-50ms delay between each
- Avoid all-at-once appearance — too jarring
- Avoid too-slow reveals — user must perceive content immediately

### State transitions
- Hover, active, expanded, collapsed: animate smoothly with 150-250ms
- Use consistent easing across all state changes in the same component

### Drawer / Modal
- Slide in from edge (drawer) or scale from trigger (modal)
- Exit animation: reverse of enter, faster (60-70% duration)
- Overlay fades in/out with 200-300ms

### Product UI
- 150-250ms on most transitions
- Motion conveys state not decoration
- State changes, feedback, loading, reveal — nothing ornamental
- No orchestrated page-load sequences

### Navigation direction
- Keep direction logically consistent throughout the app
- Forward = deeper hierarchy, back = shallower hierarchy
- Tab switches: no directional animation (content crossfade)

### Haptic feedback
- Use for confirmations, not for trivial interactions
- Avoid overuse — haptics lose meaning with excessive repetition
- Pair with visual feedback for accessibility

## Brand UI Motion

- Can be more expressive than product UI
- Parallax: use sparingly, must respect reduced motion
- Spring physics for natural feel in hero or reveal animations
- Stagger for reveal sequences (logos, taglines, features)
- Shared element transitions for narrative continuity

## Product UI Motion

- 150-250ms on most transitions
- Motion conveys state, not decoration
- State change, feedback, loading, reveal — all serve a purpose
- No orchestrated page-load sequences
- Product loads into a task — users do not want to watch it load
- Micro-interactions must feel responsive, not ornamental

## Quick Reference

```css
/* Reduced motion reset */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}

/* Interruptible card press */
.card {
  transition: transform 150ms ease-out;
  cursor: pointer;
}
.card:active {
  transform: scale(0.97);
}

/* Staggered list entrance */
.list-item {
  opacity: 0;
  animation: fadeInUp 300ms ease-out forwards;
}
.list-item:nth-child(1) { animation-delay: 0ms; }
.list-item:nth-child(2) { animation-delay: 40ms; }
.list-item:nth-child(3) { animation-delay: 80ms; }

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}
```
