# shadcn/ui Forms & Inputs Reference

## Core Patterns

### FieldGroup + Field Hierarchy

Every form uses `FieldGroup` as the parent container and `Field` for each input group:

```tsx
<FieldGroup>
  <Field>
    <Label htmlFor="name">Full Name</Label>
    <Input id="name" placeholder="John Doe" />
    <FieldMessage>Enter your full legal name</FieldMessage>
  </Field>

  <Field>
    <Label htmlFor="email">Email</Label>
    <Input id="email" type="email" placeholder="you@example.com" />
  </Field>
</FieldGroup>
```

```tsx
/* ❌ Incorrect — raw div layout */
<div className="space-y-4">
  <div>
    <label htmlFor="name">Name</label>
    <input id="name" />
  </div>
</div>

/* ✅ Correct — FieldGroup + Field */
<FieldGroup>
  <Field>
    <Label htmlFor="name">Name</Label>
    <Input id="name" />
  </Field>
</FieldGroup>
```

### InputGroup with Addons

Use `InputGroup` + `InputGroupAddon` + `InputGroupInput` / `InputGroupTextarea` for inputs with icons or buttons:

```tsx
/* Icon prefix */
<Field>
  <Label htmlFor="search">Search</Label>
  <InputGroup>
    <InputGroupAddon>
      <IconSearch className="size-4" />
    </InputGroupAddon>
    <InputGroupInput id="search" placeholder="Search..." />
  </InputGroup>
</Field>

/* Button addon */
<Field>
  <Label htmlFor="quantity">Quantity</Label>
  <InputGroup>
    <InputGroupAddon>
      <Button size="icon-sm" variant="outline">
        <IconMinus className="size-4" />
      </Button>
    </InputGroupAddon>
    <InputGroupInput id="quantity" type="number" defaultValue="1" min={0} className="text-center" />
    <InputGroupAddon>
      <Button size="icon-sm" variant="outline">
        <IconPlus className="size-4" />
      </Button>
    </InputGroupAddon>
  </InputGroup>
</Field>

/* Textarea */
<Field>
  <Label htmlFor="bio">Bio</Label>
  <InputGroup>
    <InputGroupTextarea id="bio" placeholder="Tell us about yourself" />
  </InputGroup>
  <FieldMessage>Maximum 500 characters</FieldMessage>
</Field>
```

### Validation States

```tsx
/* Error state */
<Field data-invalid>
  <Label htmlFor="password">Password</Label>
  <InputGroup>
    <InputGroupInput
      id="password"
      type="password"
      aria-invalid="true"
      aria-describedby="password-error"
    />
  </InputGroup>
  <FieldMessage id="password-error">
    Password must be at least 8 characters
  </FieldMessage>
</Field>

/* Success state */
<Field data-valid>
  <Label htmlFor="email">Email</Label>
  <InputGroup>
    <InputGroupAddon>
      <IconCheck className="size-4 text-success" />
    </InputGroupAddon>
    <InputGroupInput id="email" type="email" value="valid@email.com" />
  </InputGroup>
  <FieldMessage>Email is available</FieldMessage>
</Field>
```

Validation attributes:

| Attribute | Element | When |
|---|---|---|
| `data-invalid` | `Field` parent | Field has error |
| `aria-invalid="true"` | Input control | Field has error |
| `aria-describedby` | Input control | Links to `FieldMessage` id |
| `data-valid` | `Field` parent | Field validated successfully |

### Disabled States

```tsx
<Field data-disabled>
  <Label htmlFor="readonly-field">Read Only</Label>
  <InputGroup>
    <InputGroupInput id="readonly-field" value="Pre-filled value" disabled />
  </InputGroup>
  <FieldMessage>This field cannot be edited</FieldMessage>
</Field>
```

### Option Sets with ToggleGroup

Use `ToggleGroup` for 2-7 mutually exclusive or multi-select options:

```tsx
/* Single select */
<Field>
  <Label>Theme</Label>
  <ToggleGroup type="single" defaultValue="light">
    <ToggleGroupItem value="light">
      <IconSun className="size-4" />
      Light
    </ToggleGroupItem>
    <ToggleGroupItem value="dark">
      <IconMoon className="size-4" />
      Dark
    </ToggleGroupItem>
    <ToggleGroupItem value="system">
      <IconDeviceLaptop className="size-4" />
      System
    </ToggleGroupItem>
  </ToggleGroup>
</Field>

/* Multiple select */
<Field>
  <Label>Filters</Label>
  <ToggleGroup type="multiple" defaultValue={["active"]}>
    <ToggleGroupItem value="active">Active</ToggleGroupItem>
    <ToggleGroupItem value="pending">Pending</ToggleGroupItem>
    <ToggleGroupItem value="archived">Archived</ToggleGroupItem>
  </ToggleGroup>
</Field>
```

### FieldSet for Related Groups

Use `FieldSet` + `FieldLegend` for grouped checkboxes, radios, or toggles:

```tsx
<FieldSet>
  <FieldLegend>Notification Preferences</FieldLegend>
  <Field className="flex items-center gap-2">
    <Checkbox id="email-notif" />
    <Label htmlFor="email-notif">Email notifications</Label>
  </Field>
  <Field className="flex items-center gap-2">
    <Checkbox id="sms-notif" />
    <Label htmlFor="sms-notif">SMS notifications</Label>
  </Field>
  <Field className="flex items-center gap-2">
    <Checkbox id="push-notif" />
    <Label htmlFor="push-notif">Push notifications</Label>
  </Field>
</FieldSet>

/* Radio Group inside FieldSet */
<FieldSet>
  <FieldLegend>Plan Type</FieldLegend>
  <RadioGroup defaultValue="free">
    <Field className="flex items-center gap-2">
      <RadioGroupItem value="free" id="free" />
      <Label htmlFor="free">Free — up to 3 projects</Label>
    </Field>
    <Field className="flex items-center gap-2">
      <RadioGroupItem value="pro" id="pro" />
      <Label htmlFor="pro">Pro — unlimited projects</Label>
    </Field>
  </RadioGroup>
</FieldSet>
```

## Component Choice Matrix

| Choice count | Component | Example |
|---|---|---|
| 2 options | `Switch` or `Checkbox` | Enable/disable, yes/no |
| 2-7 options | `ToggleGroup` | Plan type, theme, status filter |
| 2-7 options (exclusive) | `RadioGroup` | Payment method, gender |
| 5-20 options | `Select` or `Combobox` | Country, timezone, language |
| 20+ options | `Combobox` (with search) | Product, user, tag |
| Multi-select (few) | `Checkbox` group | Feature toggles, permissions |
| Multi-select (many) | `Combobox` `multiple` | Tags, categories, roles |
| Single binary | `Switch` | Dark mode, notifications on/off |

## Form Layout Patterns

### Single Column

```tsx
<FieldGroup>
  <Field>
    <Label htmlFor="title">Title</Label>
    <Input id="title" placeholder="Product name" />
  </Field>
  <Field>
    <Label htmlFor="description">Description</Label>
    <InputGroup>
      <InputGroupTextarea id="description" placeholder="Describe your product" />
    </InputGroup>
  </Field>
  <Field>
    <Label htmlFor="price">Price</Label>
    <InputGroup>
      <InputGroupAddon>$</InputGroupAddon>
      <InputGroupInput id="price" type="number" step="0.01" />
    </InputGroup>
  </Field>
  <Button type="submit">Create Product</Button>
</FieldGroup>
```

### Two Column Grid

```tsx
<FieldGroup className="grid grid-cols-2 gap-4">
  <Field>
    <Label htmlFor="first-name">First Name</Label>
    <Input id="first-name" />
  </Field>
  <Field>
    <Label htmlFor="last-name">Last Name</Label>
    <Input id="last-name" />
  </Field>
  <Field className="col-span-2">
    <Label htmlFor="email">Email</Label>
    <Input id="email" type="email" />
  </Field>
</FieldGroup>
```

### Inline Field

```tsx
<Field className="flex flex-row items-center justify-between rounded-lg border p-4">
  <div>
    <Label>Dark Mode</Label>
    <FieldMessage>Toggle dark theme across the app</FieldMessage>
  </div>
  <Switch defaultChecked />
</Field>
```

## Attributes Summary

| Element | States | Attributes |
|---|---|---|
| `Field` | normal, error, success, disabled | `data-invalid`, `data-valid`, `data-disabled` |
| `Field` (error) | has visible error | `data-invalid` |
| `InputGroupInput` | error | `aria-invalid="true"`, `aria-describedby="field-id"` |
| `InputGroupInput` | disabled | `disabled` |
| `Checkbox` | checked | `checked`, `onCheckedChange` |
| `RadioGroupItem` | selected | `value`, `id` |
| `Switch` | toggled | `checked`, `onCheckedChange` |
| `Select.Item` | selected | `value` |
| `ToggleGroupItem` | pressed | `value`, `aria-pressed` |
| `Input` | password | `type="password"` |
| `Input` | numeric | `type="number" min max step` |
