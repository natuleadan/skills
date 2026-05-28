# RTL CSS Patterns

CSS and component patterns for right-to-left (RTL) language support in Tailwind/shadcn/ui projects.

## Configuration

- Set `"rtl": true` in `components.json` — the shadcn CLI auto-converts physical to logical CSS classes
- Without this flag, components use physical `left`/`right` classes
- The CLI runs this transformation at component install time

## Logical CSS Properties

### Margin

| Physical | Logical | RTL behavior |
|---|---|---|
| `ml-*` (margin-left) | `ms-*` (margin-inline-start) | Flips automatically |
| `mr-*` (margin-right) | `me-*` (margin-inline-end) | Flips automatically |

### Padding

| Physical | Logical | RTL behavior |
|---|---|---|
| `pl-*` (padding-left) | `ps-*` (padding-inline-start) | Flips automatically |
| `pr-*` (padding-right) | `pe-*` (padding-inline-end) | Flips automatically |

### Positioning

| Physical | Logical | RTL behavior |
|---|---|---|
| `left-*` | `start-*` | Flips automatically |
| `right-*` | `end-*` | Flips automatically |

### Border Radius

| Physical | Logical | RTL behavior |
|---|---|---|
| `rounded-l-*` | `rounded-s-*` | Flips automatically |
| `rounded-r-*` | `rounded-e-*` | Flips automatically |
| `border-l` | `border-s` | Flips automatically |
| `border-r` | `border-e` | Flips automatically |

### Text Alignment

| Physical | Logical | RTL behavior |
|---|---|---|
| `text-left` | `text-start` | Flips automatically |
| `text-right` | `text-end` | Flips automatically |

## DirectionProvider

Wrap your app with a `DirectionProvider` from Radix:

```tsx
import { DirectionProvider } from "@radix-ui/react-direction"

function App({ children }) {
  return (
    <DirectionProvider dir="rtl">
      {children}
    </DirectionProvider>
  )
}
```

Portal components (Popover, Tooltip, DropdownMenu, etc.) inherit direction from context.

## Icon Rotation

Chevron and directional icons need `rtl:rotate-180` to flip in RTL:

```tsx
<IconChevronRight className="rtl:rotate-180" />
```

Apply this to: carousel arrows, breadcrumb separators, pagination arrows, submenu triggers, sidebar toggle icons.

## Charts

For chart libraries like Recharts, set `reversed={dir === "rtl"}` on the XAxis to render labels right-to-left. This is commonly needed for bar charts, line charts, and area charts with month/day labels.

## Known Pitfalls

### Positioned Components (Drawer, Sheet)

Components that use physical `left-0`/`right-0` with `data-[side]` attributes need `rtl:` overrides:

```css
data-[side=left]:left-0 rtl:data-[side=left]:right-0
data-[side=right]:right-0 rtl:data-[side=right]:left-0
```

### Calendar Range Selection

Range start/end highlights use `rounded-s-*`/`rounded-e-*` and `after:start-0`/`after:end-0` for correct RTL rendering. If using physical `rounded-l-*`/`rounded-r-*`, the highlight tail appears on the wrong side in RTL.

### Scrub Bar / Slider

Inline `style={{ left }}` should use `style={{ insetInlineStart }}` instead. This ensures the position respects the document direction.
