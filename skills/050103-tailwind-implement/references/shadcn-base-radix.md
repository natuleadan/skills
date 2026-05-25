# shadcn/ui: Base vs Radix API Differences

## Core API Difference

| Feature | Radix UI (shadcn default) | Base UI |
|---|---|---|
| Element override | `asChild` prop + `Slot` from `@radix-ui/react-slot` | `render` prop |
| Slot utility | `<Slot>` wraps children, merges props | No slot — `render` replaces element |

### asChild (Radix)

```tsx
import { Slot } from "@radix-ui/react-slot"

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  asChild?: boolean
}

export function Button({ asChild = false, ...props }: ButtonProps) {
  const Comp = asChild ? Slot : "button"
  return <Comp {...props} />
}

/* Usage */
<DialogTrigger asChild>
  <Button variant="outline">Open</Button>
</DialogTrigger>
```

### render (Base)

```tsx
<Select
  items={[
    { value: "apple", label: "Apple" },
    { value: "banana", label: "Banana" },
  ]}
  render={{
    renderValue: (value) => <span className="text-primary">{value.label}</span>,
    renderOption: (item) => <div className="flex items-center gap-2">{item.label}</div>,
  }}
/>
```

## Component-Specific Differences

### Select

| Aspect | Radix UI | Base UI |
|---|---|---|
| Options | Children: `<SelectItem value="apple">Apple</SelectItem>` | `items` prop: `[{value: "apple", label: "Apple"}]` |
| Groups | `<SelectGroup>` + `<SelectLabel>` | `group` key in items array |
| Custom render | Wrapping children | `render.renderValue`, `render.renderOption` |
| Trigger content | `<SelectValue placeholder="Select..." />` | Default shows selected label |

```tsx
/* Radix — children-based */
<Select onValueChange={handleChange}>
  <SelectTrigger>
    <SelectValue placeholder="Select a fruit" />
  </SelectTrigger>
  <SelectContent>
    <SelectGroup>
      <SelectLabel>Fruits</SelectLabel>
      <SelectItem value="apple">Apple</SelectItem>
      <SelectItem value="banana">Banana</SelectItem>
    </SelectGroup>
  </SelectContent>
</Select>

/* Base — items prop */
<Select
  placeholder="Select a fruit"
  items={[
    { value: "apple", label: "Apple" },
    { value: "banana", label: "Banana" },
  ]}
  onValueChange={handleChange}
/>
```

### ToggleGroup

| Aspect | Radix UI | Base UI |
|---|---|---|
| Multiple selection | `type="multiple"` string prop | `multiple` boolean prop |
| Single selection | `type="single"` string prop | Omit `multiple` or set `false` |
| Value type | string (single) or string[] (multiple) | string or string[] |

```tsx
/* Radix */
<ToggleGroup type="single" defaultValue="light">
  <ToggleGroupItem value="light">Light</ToggleGroupItem>
  <ToggleGroupItem value="dark">Dark</ToggleGroupItem>
</ToggleGroup>

<ToggleGroup type="multiple" defaultValue={["bold", "italic"]}>
  <ToggleGroupItem value="bold">Bold</ToggleGroupItem>
  <ToggleGroupItem value="italic">Italic</ToggleGroupItem>
</ToggleGroup>

/* Base */
<ToggleGroup defaultValue="light">
  <ToggleGroupItem value="light">Light</ToggleGroupItem>
  <ToggleGroupItem value="dark">Dark</ToggleGroupItem>
</ToggleGroup>

<ToggleGroup multiple defaultValue={["bold", "italic"]}>
  <ToggleGroupItem value="bold">Bold</ToggleGroupItem>
  <ToggleGroupItem value="italic">Italic</ToggleGroupItem>
</ToggleGroup>
```

### Slider

| Aspect | Radix UI | Base UI |
|---|---|---|
| Single value | `value={[50]}` (array with one element) | `value={50}` (number) |
| Range value | `value={[20, 80]}` (array with two elements) | Not supported — use two separate Sliders |
| onChange | `onValueChange={(val) => setValue(val)}` where val is number[] | `onValueChange={(val) => setValue(val)}` where val is number |

```tsx
/* Radix — always array */
<Slider
  value={[volume]}
  onValueChange={([v]) => setVolume(v)}
  max={100}
  step={1}
/>

/* Radix — range */
<Slider
  value={[min, max]}
  onValueChange={([mn, mx]) => setRange(mn, mx)}
  min={0}
  max={100}
/>

/* Base — scalar */
<Slider
  value={volume}
  onValueChange={setVolume}
  max={100}
  step={1}
/>
```

### Accordion

| Aspect | Radix UI | Base UI |
|---|---|---|
| Single/Multiple | `type="single"` or `type="multiple"` string prop | `multiple` boolean prop |
| defaultValue | string (single) or string[] (multiple) | Always string[] |
| Collapsible | default in single type | `collapsible` boolean prop |

```tsx
/* Radix — single (default collapsible) */
<Accordion type="single" defaultValue="item-1" collapsible>
  <AccordionItem value="item-1">
    <AccordionTrigger>Section 1</AccordionTrigger>
    <AccordionContent>Content 1</AccordionContent>
  </AccordionItem>
  <AccordionItem value="item-2">
    <AccordionTrigger>Section 2</AccordionTrigger>
    <AccordionContent>Content 2</AccordionContent>
  </AccordionItem>
</Accordion>

/* Radix — multiple */
<Accordion type="multiple" defaultValue={["item-1"]}>
  ...
</Accordion>

/* Base — always array defaultValue */
<Accordion defaultValue={["item-1"]}>
  ...
</Accordion>

/* Base — multiple selection */
<Accordion multiple defaultValue={["item-1", "item-3"]}>
  ...
</Accordion>
```

### Non-Button Elements

| Aspect | Radix UI | Base UI |
|---|---|---|
| Trigger element | Must be `<button>` (or `asChild` with `<button>`-based component) | `render` allows any HTML element |
| Example | `<DialogTrigger asChild><Button>Open</Button></DialogTrigger>` | `<Select render={{ renderTrigger: (props) => <div {...props}>Open</div> }} />` |

```tsx
/* Radix — only button elements */
<DropdownMenuTrigger asChild>
  <Button variant="outline">Menu</Button>
</DropdownMenuTrigger>

/* Base — any element via render */
<Select
  render={{
    renderTrigger: (props) => (
      <div {...props} className="flex items-center gap-2 cursor-pointer">
        <span>Select option</span>
        <IconChevronDown className="size-4" />
      </div>
    ),
  }}
/>
```

## Quick Decision Table

| Pattern | Radix | Base |
|---|---|---|
| Element override | `asChild` + `<Slot>` | `render` prop |
| Select options | Children (`<SelectItem>`) | `items` array prop |
| ToggleGroup mode | `type="single"` / `type="multiple"` | `multiple` boolean |
| Slider value type | Always `number[]` | `number` (scalar) |
| Accordion value | String or string[] by `type` | Always `string[]` |
| Non-button triggers | Not supported natively | `render` supports any element |

## Migration Patterns

```tsx
/* Radix → Base: Select */
/* Before (Radix) */
<Select onValueChange={setValue}>
  <SelectTrigger><SelectValue placeholder="Select" /></SelectTrigger>
  <SelectContent>
    {items.map(item => (
      <SelectItem key={item.value} value={item.value}>
        {item.label}
      </SelectItem>
    ))}
  </SelectContent>
</Select>

/* After (Base) */
<Select
  placeholder="Select"
  items={items}
  onValueChange={setValue}
/>

/* Radix → Base: ToggleGroup */
/* Before (Radix) */
<ToggleGroup type="multiple" value={selected} onValueChange={setSelected}>
  {options.map(opt => (
    <ToggleGroupItem key={opt.value} value={opt.value}>
      {opt.label}
    </ToggleGroupItem>
  ))}
</ToggleGroup>

/* After (Base) */
<ToggleGroup multiple value={selected} onValueChange={setSelected}>
  {options.map(opt => (
    <ToggleGroupItem key={opt.value} value={opt.value}>
      {opt.label}
    </ToggleGroupItem>
  ))}
</ToggleGroup>
```
