---
name: 080104-motion-animation
description: "Motion design and animation principles: timing, easing curves, spring physics, micro-interactions, reduced motion, performance optimization for frontend interfaces."
license: MIT
---

# Motion & Animation Principles

Animation and motion design for frontend interfaces — timing, easing, physics, micro-interactions, and performance. Covers both brand (expressive) and product (task-serving) motion.

## References

| Topic | File |
|---|---|
| Timing values, easing curves, CSS/JS implementations, platform standards | [references/timing-easing.md](references/timing-easing.md) |
| Spring physics, spatial continuity, shared transitions, reduced motion, interruption handling | [references/motion-principles.md](references/motion-principles.md) |
| Press feedback, ripple, skeleton, toast, toggle, dropdown, focus, tabs, progress | [references/micro-interactions.md](references/micro-interactions.md) |

## Core Rules

- **Timing**: Micro-interactions 150-300ms. Complex transitions ≤400ms. Exit 60-70% of enter. Stagger 30-50ms per item.
- **Easing**: Ease-out for entering (exponential: quart/quint/expo), ease-in for exiting. No bounce, no elastic, no linear for UI.
- **Performance**: Animate transform/opacity only. Never width/height/top/left. Interruptible animations. 60fps (~16ms/frame).
- **Reduced motion**: Respect `prefers-reduced-motion`. Data readable immediately. No orchestrated page-load sequences.
- **Product vs Brand**: Product = 150-250ms, conveys state only. Brand = more expressive, spring physics, stagger, shared elements.

## When to Use

- Adding micro-interactions to buttons/toggles
- Designing page transitions
- Implementing loading animations
- Creating gesture feedback
- Reviewing motion performance
- Ensuring reduced-motion support
