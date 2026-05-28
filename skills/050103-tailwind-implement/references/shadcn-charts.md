# shadcn Charts with Recharts

Building charts with Recharts and shadcn/ui's ChartContainer component.

## Prerequisites

```bash
npm install recharts
```

## Chart Config

The chart config is decoupled from data. Define labels and colors with `satisfies ChartConfig`:

```typescript
import { type ChartConfig } from "@/components/ui/chart"

const config = {
  revenue: { label: "Revenue", color: "var(--primary)" },
  expenses: { label: "Expenses", color: "var(--chart-2)" },
} satisfies ChartConfig
```

## ChartContainer

Wraps Recharts components. Requires a `min-h-*` or `aspect-*` for responsive measurement:

```tsx
<ChartContainer config={config} className="max-h-[200px] w-full">
  {/* Recharts chart */}
</ChartContainer>
```

## ChartTooltip

Custom tooltip wrapper. Props:

- `indicator` — `"dot"` | `"line"` | `"dashed"`
- `hideLabel` — hide the tooltip label
- `hideIndicator` — hide the indicator
- `labelKey` — custom config key for label
- `nameKey` — custom data key for name

## ChartLegend

Custom legend wrapper. Use `nameKey` when data keys differ from config keys.

## Chart Types

### Bar Chart

Use `BarChart` with `<Bar dataKey="..." fill="var(--color-key)" radius={4} />`. Stack bars with `stackId="a"`.

### Line Chart

Use `LineChart` with `<Line type="monotone" dataKey="..." stroke="var(--color-key)" strokeWidth={2} />`. Add `dot` and `activeDot` props.

### Area Chart

Use `AreaChart` with `<Area type="monotone" dataKey="..." fill="url(#gradient-id)" />`. Define `<linearGradient>` in `<defs>` for gradient fill.

### Pie / Donut Chart

Use `PieChart` with `<Pie innerRadius={50} outerRadius={80}>`. Map data to `<Cell fill={...} />`. For donut (hole in center), set `innerRadius > 0`.

### Radial Gauge

Use `RadialBarChart` with a single data point. Set `innerRadius`, `outerRadius`, `barSize`, `startAngle` (90 for top), `endAngle` (-270 for full circle).

## RTL

Use `useDirection()` to get the current direction and set `reversed={dir === "rtl"}` on XAxis. This renders month labels right-to-left in RTL mode.

## Colors

Use CSS variables for theming: `var(--chart-1)` through `var(--chart-5)`. Single-series charts can use `var(--primary)`.
