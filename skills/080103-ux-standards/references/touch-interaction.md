# Touch & Interaction Reference

Deep reference for touch targets, gesture design, haptic feedback, safe areas, and mobile interaction patterns.

---

## Touch Target Sizing

### Platform Requirements

| Standard | Minimum Size | Notes |
|---|---|---|
| Apple HIG | 44×44pt | All interactive elements |
| Material Design | 48×48dp | Touch targets |
| WCAG 2.5.8 (Target Size) | 24×24px | AA minimum (small targets exempt if essential) |
| WCAG 2.5.5 (Target Size) | 44×44px | AAA enhanced for pointer input |

### Extending Hit Area

When an icon or compact element must be visually small, extend its touch target with transparent padding:

```css
/* Technique 1: transparent padding */
.compact-icon-button {
  padding: 12px; /* 24px icon + 12+12 = 48px total */
  /* Ensure the visual icon is centered within padding */
}

/* Technique 2: pseudo-element overlap */
.small-button {
  position: relative;
  /* Visual size: 24px */
  min-width: 24px;
  min-height: 24px;
}
.small-button::before {
  content: '';
  position: absolute;
  inset: -10px; /* 24 + 20 = 44px total hit area */
}

/* Technique 3: transparent border */
.small-button {
  border: 10px solid transparent;
  background-clip: padding-box;
}
```

### Spacing Between Targets
- Minimum 8px between touch targets (Apple HIG)
- Insufficient spacing causes incorrect tap registration, especially on small screens
- Measure center-to-center distance as well: aim for ~56dp (Material)

---

## Gesture Design

### Gesture Types

| Gesture | Convention | Avoid |
|---|---|---|
| Tap | Select/activate | Long delay before recognition |
| Double-tap | Zoom or secondary action | Reusing for primary action |
| Long press | Context menu, reorder | Unlabeled actions |
| Swipe | Scroll, dismiss, reveal actions | Content parallax |
| Pinch | Zoom | Navigation |
| Pan | Scroll, drag | Conflicting with swipe |

### Touch-Action CSS

```css
/* Allow vertical scroll only (prevents swipe-to-go-back conflicts) */
.scroll-container {
  touch-action: pan-y;
}

/* Horizontal carousel with snap */
.carousel {
  touch-action: pan-x;
  scroll-snap-type: x mandatory;
  overscroll-behavior-x: contain;
}

/* Element that should not scroll at all */
.draggable-item {
  touch-action: none;
}

/* Remove tap delay on mobile */
.interactive {
  touch-action: manipulation;
}
```

### Gesture Conflicts

| Conflict | Solution |
|---|---|
| Horizontal swipe triggers browser back | `touch-action: pan-y` on main content |
| Pull-to-refresh conflicts with scroll | Set `overscroll-behavior-y: contain` on content |
| Long press triggers context menu | Use `pointer-events` + custom handler with sufficient threshold |
| Double-tap zoom conflicts with tap | `touch-action: manipulation` disables double-tap zoom |

### Custom Gesture Thresholds

```ts
interface GestureConfig {
  threshold: number;      // px movement before gesture starts
  longPressDuration: number; // ms for long press
  swipeVelocityThreshold: number; // px/ms
}

const DRAG_THRESHOLD = 5;      // px before drag starts
const SWIPE_THRESHOLD = 50;    // px minimum swipe distance
const SWIPE_VELOCITY = 0.3;    // px/ms minimum velocity

function handleTouchStart(clientX: number, clientY: number) {
  startX = clientX;
  startY = clientY;
  isDragging = false;
}

function handleTouchMove(clientX: number, clientY: number) {
  const dx = clientX - startX;
  const dy = clientY - startY;
  const distance = Math.sqrt(dx * dx + dy * dy);

  if (distance > DRAG_THRESHOLD && !isDragging) {
    isDragging = true;
    onDragStart();
  }
}
```

---

## Haptic Feedback

### When to Use Haptics

| Action | Haptic Type | Priority |
|---|---|---|
| Confirmation (success, save) | Light/medium impact | High |
| Selection change | Light impact | Medium |
| Error / failure | Heavy impact or warning | High |
| Notification arrival | Custom pattern | Medium |
| Drag start/end | Light impact | Low |
| Button press | None (visual feedback only) | Never |

### Avoid Haptics For:
- Every keystroke on a keyboard
- Page transitions / navigations
- Advertisements or promotional content
- Actions that happen more than once per second
- Decorative animations

### Platform APIs

**iOS (Haptic Feedback via HIG):**
- Notification (`UINotificationFeedbackGenerator`): success, warning, error
- Impact (`UIImpactFeedbackGenerator`): light, medium, heavy
- Selection (`UISelectionFeedbackGenerator`): passive clicks

**Web (Vibration API — limited Android support):**
```js
// Single vibration (ms)
navigator.vibrate(10); // short tap
navigator.vibrate([50, 100, 50]); // pattern: vibrate 50ms, pause 100ms, vibrate 50ms
```

**Android (VibrationEffect):**
```java
// Android 8+
VibrationEffect effect = VibrationEffect.createOneShot(20, VibrationEffect.DEFAULT_AMPLITUDE);
vibrator.vibrate(effect);
```

---

## Safe Areas

### CSS Environment Variables

```css
/* Full safe area inset */
.safe-padding {
  padding-top: env(safe-area-inset-top, 0px);
  padding-right: env(safe-area-inset-right, 0px);
  padding-bottom: env(safe-area-inset-bottom, 0px);
  padding-left: env(safe-area-inset-left, 0px);
}

/* Fixed bottom element (e.g., tab bar) */
.bottom-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: calc(56px + env(safe-area-inset-bottom, 0px));
  padding-bottom: env(safe-area-inset-bottom, 0px);
}

/* Fixed top element */
.top-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  padding-top: env(safe-area-inset-top, 0px);
}
```

### Dynamic Island & Notch
- Keep interactive content outside the notch/Dynamic Island area (safe-area-inset-top)
- Do not place buttons, tabs, or critical information in the top 44px (notch) or top 54px (Dynamic Island)
- Landscape: safe-area-inset-left and safe-area-inset-right for devices with rounded corners

### Gesture Bar (Home Indicator)
- Bottom navigation must account for the home indicator (safe-area-inset-bottom ~34px on iPhone X+)
- Interactive elements should be at least 12px above the gesture bar
- Do not extend swipeable content behind the gesture bar

### Viewport Meta Tag
```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
```
Without `viewport-fit=cover`, the viewport avoids safe areas entirely (black bars on iPhone X+).

---

## Touch Events

### Pointer Events (Modern, Unified)
```ts
element.addEventListener('pointerdown', handleDown);
element.addEventListener('pointermove', handleMove);
element.addEventListener('pointerup', handleUp);
element.addEventListener('pointercancel', handleCancel);
```
- `pointer: coarse` = touch input, `pointer: fine` = mouse/stylus
- `any-pointer: coarse` = device has touch capability
```css
@media (pointer: coarse) {
  .button {
    min-height: 48px;
  }
}
```

### Touch vs Mouse vs Stylus

| Property | Touch | Mouse | Stylus |
|---|---|---|---|
| `pointerType` | `"touch"` | `"mouse"` | `"pen"` |
| `pointer: coarse` | Yes | No | No (fine) |
| Hover | No | Yes | Hover events limited |

### Preventing Scroll Interference
```css
/* Interactive carousel — horizontal only, prevent vertical scroll while swiping */
.carousel-content {
  touch-action: pan-y pinch-zoom;
  overscroll-behavior-x: contain;
}
```

---

## Screen Rotation & Orientation

- Test all touch interactions in both portrait and landscape
- Landscape: touch targets on the horizontal axis should be as generous as vertical
- Avoid locking orientation unless absolutely necessary (video, game)
- If orientation must be locked, use `screen.orientation.lock()` with a fallback

---

## Platform-Specific Touch Patterns

### iOS
- Swipe-to-go-back: left edge swipe (do NOT block with `touch-action: none` on edges)
- 3D Touch / Haptic Touch: for previews and quick actions
- Pull-to-refresh: system-provided, available in scroll views
- Long press on text: selection/lookup

### Android
- Back gesture: left or right edge swipe (do NOT block)
- Long press for context menu (replaces iOS 3D Touch)
- System navigation bar at bottom with gesture hints
- Split-screen: avoid assumptions about available vertical space

### Web
- Pinch zoom must not be disabled (`user-scalable=no` violates WCAG)
- `overscroll-behavior` controls scroll chaining
- Context menus: `contextmenu` event for long-press on touch devices
