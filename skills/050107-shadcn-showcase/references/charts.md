# Charts with Recharts

Building charts with Recharts and shadcn/ui's ChartContainer component.

## Dependencies

```bash
npm install recharts
```

## Chart Config

Define a chart config to map data keys to labels and colors:

```typescript
import { type ChartConfig } from "@/components/ui/chart"

const chartConfig = {
  desktop: { label: "Desktop", color: "var(--chart-1)" },
  mobile: { label: "Mobile", color: "var(--chart-2)" },
} satisfies ChartConfig
```

## Common Components

- `ChartContainer` — wraps Recharts components, takes `config` and `className`
- `ChartTooltip` + `ChartTooltipContent` — custom tooltip with `indicator`, `hideLabel`, `labelKey`
- `ChartLegend` + `ChartLegendContent` — custom legend with optional `nameKey`

## Bar Chart

```tsx
<ChartContainer config={chartConfig} className="max-h-[200px] w-full">
  <BarChart data={chartData}>
    <CartesianGrid vertical={false} strokeDasharray="3 3" />
    <XAxis dataKey="month" tickLine={false} axisLine={false} tickMargin={8} reversed={dir === "rtl"} />
    <ChartTooltip content={<ChartTooltipContent indicator="dashed" />} />
    <Bar dataKey="desktop" fill="var(--chart-1)" radius={4} />
    <Bar dataKey="mobile" fill="var(--chart-2)" radius={4} />
    <ChartLegend content={<ChartLegendContent />} />
  </BarChart>
</ChartContainer>
```

## Line Chart

```tsx
<LineChart data={chartData}>
  <CartesianGrid vertical={false} strokeDasharray="3 3" />
  <XAxis dataKey="month" tickLine={false} axisLine={false} reversed={dir === "rtl"} />
  <YAxis tickLine={false} axisLine={false} tickFormatter={(v) => `$${v}`} />
  <ChartTooltip content={<ChartTooltipContent />} />
  <Line type="monotone" dataKey="revenue" stroke="var(--primary)" strokeWidth={2} dot={{ fill: "var(--primary)" }} />
</LineChart>
```

## Area Chart

Use `<defs>` with `<linearGradient>` for gradient fill:

```tsx
<AreaChart data={chartData}>
  <defs>
    <linearGradient id="fillVisitors" x1="0" y1="0" x2="0" y2="1">
      <stop offset="5%" stopColor="var(--primary)" stopOpacity={0.4} />
      <stop offset="95%" stopColor="var(--primary)" stopOpacity={0.05} />
    </linearGradient>
  </defs>
  <Area dataKey="desktop" type="monotone" fill="url(#fillVisitors)" stroke="var(--primary)" strokeWidth={2} />
</AreaChart>
```

## Donut / Pie Chart

Use `innerRadius` for donut effect:

```tsx
<PieChart>
  <Pie data={chartData} dataKey="value" nameKey="name" innerRadius={50} outerRadius={80}>
    {chartData.map((entry) => <Cell key={entry.name} fill={entry.fill} />)}
  </Pie>
  <ChartTooltip content={<ChartTooltipContent hideLabel />} />
  <ChartLegend content={<ChartLegendContent />} />
</PieChart>
```

## Radial Chart (Gauge)

```tsx
<RadialBarChart data={[{ name: "Progress", value: 72 }]} innerRadius="60%" outerRadius="85%" barSize={12} startAngle={90} endAngle={-270}>
  <RadialBar dataKey="value" cornerRadius={6} fill="var(--chart-1)" />
  <ChartTooltip content={<ChartTooltipContent />} />
</RadialBarChart>
```

## Horizontal Bar Chart

Use `layout="vertical"` with `XAxis type="number"` and `YAxis type="category"`:

```tsx
<BarChart data={chartData} layout="vertical">
  <CartesianGrid horizontal={false} strokeDasharray="3 3" />
  <XAxis type="number" tickLine={false} axisLine={false} reversed={dir === "rtl"} />
  <YAxis dataKey="month" type="category" tickLine={false} axisLine={false} />
  <Bar dataKey="desktop" fill="var(--chart-1)" radius={4} />
  <ChartLegend content={<ChartLegendContent />} />
</BarChart>
```

## RTL Support

- Import `useDirection` from your app's direction provider
- Set `reversed={dir === "rtl"}` on XAxis to render right-to-left
- `CartesianGrid` renders correctly without explicit RTL handling
- YAxis stays on the left even in RTL — this is a Recharts limitation

## Color Tokens

Use CSS variables for theming: `var(--chart-1)` through `var(--chart-5)` for chart data, `var(--primary)` for single-series charts.
