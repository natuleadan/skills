# shadcn/ui Component Composition

## Composition Rules

### 1. Group Items Always Live Inside Their Group

```tsx
/* ✅ Correct — SelectItem inside SelectGroup */
<Select>
  <SelectGroup>
    <SelectLabel>Fruits</SelectLabel>
    <SelectItem value="apple">Apple</SelectItem>
    <SelectItem value="banana">Banana</SelectItem>
  </SelectGroup>
  <SelectGroup>
    <SelectLabel>Vegetables</SelectLabel>
    <SelectItem value="carrot">Carrot</SelectItem>
  </SelectGroup>
</Select>

/* ✅ Correct — TabsTrigger inside TabsList */
<Tabs defaultValue="account">
  <TabsList>
    <TabsTrigger value="account">Account</TabsTrigger>
    <TabsTrigger value="password">Password</TabsTrigger>
  </TabsList>
  <TabsContent value="account">...</TabsContent>
</Tabs>

/* ❌ Incorrect — TabsTrigger outside TabsList */
<Tabs>
  <TabsTrigger value="account">Account</TabsTrigger>  /* ❌ orphaned */
  <TabsList>
  </TabsList>
</Tabs>
```

### 2. Callouts Use Alert, Not Custom Divs

```tsx
/* ❌ Incorrect */
<div className="rounded-lg border border-amber-200 bg-amber-50 p-4">
  <p className="text-amber-800">This action cannot be undone.</p>
</div>

/* ✅ Correct */
<Alert variant="warning">
  <AlertTriangle className="size-4" />
  <AlertTitle>Warning</AlertTitle>
  <AlertDescription>This action cannot be undone.</AlertDescription>
</Alert>

/* Error */
<Alert variant="destructive">
  <AlertCircle className="size-4" />
  <AlertTitle>Error</AlertTitle>
  <AlertDescription>Failed to save changes.</AlertDescription>
</Alert>

/* Info */
<Alert variant="info">
  <InfoIcon className="size-4" />
  <AlertTitle>Note</AlertTitle>
  <AlertDescription>Your session expires in 5 minutes.</AlertDescription>
</Alert>
```

### 3. Empty States Use Empty Component

```tsx
/* ❌ Incorrect */
<div className="flex flex-col items-center gap-4 py-12 text-center">
  <div className="size-12 rounded-full bg-muted flex items-center justify-center">
    <IconPackage className="size-6 text-muted-foreground" />
  </div>
  <h3 className="text-lg font-semibold">No products</h3>
  <p className="text-sm text-muted-foreground">Get started by creating a product.</p>
  <Button>Create Product</Button>
</div>

/* ✅ Correct */
<Empty
  icon={IconPackage}
  title="No products"
  description="Get started by creating a product."
>
  <Button>Create Product</Button>
</Empty>
```

### 4. Toast via sonner (Not Custom Toast)

```tsx
import { toast } from "sonner"

/* Basic */
toast.success("Changes saved successfully")
toast.error("Something went wrong")
toast.info("New update available")
toast.warning("Session expiring soon")

/* With description */
toast.success("Profile updated", {
  description: "Your changes have been saved.",
})

/* With action */
toast.error("Failed to save", {
  action: {
    label: "Retry",
    onClick: () => save(),
  },
})

/* Custom JSX */
toast(<div className="flex gap-2">
  <IconCheck className="size-4 text-success" />
  <span>Custom toast</span>
</div>)
```

### 5. Dialog / Sheet / Drawer Always Need a Title

Every overlay component must have a `DialogTitle`, `SheetTitle`, or `DrawerTitle`. Use `sr-only` if visually hidden.

```tsx
/* ✅ Title visible */
<Dialog>
  <DialogContent>
    <DialogTitle>Edit Profile</DialogTitle>
    <DialogDescription>Update your personal information</DialogDescription>
    <form>...</form>
  </DialogContent>
</Dialog>

/* ✅ Title visually hidden */
<Dialog>
  <DialogContent>
    <DialogTitle className="sr-only">Confirm Deletion</DialogTitle>
    <DialogDescription className="sr-only">Are you sure you want to delete your account?</DialogDescription>
    <div className="text-center">
      <IconAlertTriangle className="mx-auto size-8 text-destructive" />
      <h2 className="mt-4 text-lg font-semibold">Confirm Deletion</h2>
      <p className="mt-2 text-sm text-muted-foreground">This action cannot be undone.</p>
    </div>
  </DialogContent>
</Dialog>
```

### 6. Full Card Structure

```tsx
<Card>
  <CardHeader>
    <CardTitle>Card Title</CardTitle>
    <CardDescription>Optional description text</CardDescription>
  </CardHeader>
  <CardContent>
    <p>Main content</p>
  </CardContent>
  <CardFooter className="flex items-center justify-between">
    <p className="text-sm text-muted-foreground">Footer info</p>
    <Button>Action</Button>
  </CardFooter>
</Card>

/* Minimal card */
<Card>
  <CardHeader>
    <CardTitle>Settings</CardTitle>
  </CardHeader>
  <CardContent>
    <Switch />
  </CardContent>
</Card>
```

### 7. Button Loading State Pattern

Buttons have no built-in `isPending`/`isLoading` prop. Compose with `Spinner`:

```tsx
import { Spinner } from "@/components/ui/spinner"

/* ✅ Loading state */
<Button disabled>
  <Spinner className="size-4" data-icon="inline-start" />
  Saving...
</Button>

/* ✅ Async handler */
function SubmitButton() {
  const [isPending, startTransition] = useTransition()

  return (
    <Button disabled={isPending} onClick={() => startTransition(handleSubmit)}>
      {isPending && <Spinner className="size-4" data-icon="inline-start" />}
      {isPending ? "Saving..." : "Save Changes"}
    </Button>
  )
}
```

### 8. Avatar Always Needs Fallback

```tsx
/* ✅ Correct */
<Avatar>
  <AvatarImage src="/avatars/user.jpg" alt="John Doe" />
  <AvatarFallback>JD</AvatarFallback>
</Avatar>

/* ✅ Grouped avatars */
<div className="flex -space-x-2">
  <Avatar className="ring-2 ring-background">
    <AvatarImage src="/avatars/1.jpg" alt="User 1" />
    <AvatarFallback>U1</AvatarFallback>
  </Avatar>
  <Avatar className="ring-2 ring-background">
    <AvatarImage src="/avatars/2.jpg" alt="User 2" />
    <AvatarFallback>U2</AvatarFallback>
  </Avatar>
</div>
```

### 9. Use Separator, Not hr/Border Divs

```tsx
/* ❌ Incorrect */
<hr className="my-4" />
<div className="border-t my-4" />

/* ✅ Correct */
<Separator />
<Separator className="my-6" />
<Separator orientation="vertical" className="mx-2 h-8" />
```

### 10. Use Skeleton for Loading

```tsx
/* ✅ Card skeleton */
<Card>
  <CardHeader>
    <Skeleton className="h-5 w-2/3" />
    <Skeleton className="h-4 w-1/2" />
  </CardHeader>
  <CardContent>
    <Skeleton className="h-4 w-full" />
    <Skeleton className="mt-2 h-4 w-3/4" />
  </CardContent>
</Card>

/* ✅ Table row skeleton */
<div className="flex items-center gap-4">
  <Skeleton className="size-10 rounded-full" />
  <div className="space-y-2">
    <Skeleton className="h-4 w-[200px]" />
    <Skeleton className="h-4 w-[150px]" />
  </div>
</div>

/* ✅ Avatar skeleton */
<Skeleton className="size-10 rounded-full" />
```

### 11. Use Badge Instead of Custom Styled Spans

```tsx
/* ❌ Incorrect */
<span className="inline-flex items-center rounded-full bg-green-100 px-2.5 py-0.5 text-xs font-medium text-green-700">
  Active
</span>

/* ✅ Correct */
<Badge variant="success">Active</Badge>

/* ✅ With dot indicator */
<Badge variant="success" className="gap-1.5">
  <span className="size-1.5 rounded-full bg-current" />
  Online
</Badge>
```

## Overlay Component Choice Guide

| Need | Component | When |
|---|---|---|
| Confirm action | `AlertDialog` | Destructive actions, irreversible changes |
| Form or content | `Dialog` | Quick edits, detail view, short forms |
| Side panel | `Sheet` | Complex forms, settings, long content |
| Bottom panel (mobile) | `Drawer` | Mobile-first, action sheets |
| Quick info on hover | `HoverCard` | Previews, user profiles, links |
| Small popup | `Popover` | Date picker, color picker, quick actions |
| Command palette | `Command` | Search, navigation, quick actions |
| Context menu | `ContextMenu` | Right-click actions |
| Dropdown | `DropdownMenu` | Actions menu, user menu, overflow |
| Navigation | `NavigationMenu` | Site navigation, mega menus |
| Tooltip | `Tooltip` | Short descriptive text on hover |

```tsx
/* AlertDialog — confirm destructive action */
<AlertDialog>
  <AlertDialogTrigger asChild>
    <Button variant="destructive">Delete Account</Button>
  </AlertDialogTrigger>
  <AlertDialogContent>
    <AlertDialogHeader>
      <AlertDialogTitle>Are you sure?</AlertDialogTitle>
      <AlertDialogDescription>
        This action cannot be undone. Your account will be permanently deleted.
      </AlertDialogDescription>
    </AlertDialogHeader>
    <AlertDialogFooter>
      <AlertDialogCancel>Cancel</AlertDialogCancel>
      <AlertDialogAction>Delete</AlertDialogAction>
    </AlertDialogFooter>
  </AlertDialogContent>
</AlertDialog>

/* Sheet — side panel for complex forms */
<Sheet>
  <SheetTrigger asChild>
    <Button variant="outline">Edit Profile</Button>
  </SheetTrigger>
  <SheetContent side="right" className="w-full sm:max-w-lg">
    <SheetHeader>
      <SheetTitle>Edit Profile</SheetTitle>
      <SheetDescription>Update your personal information</SheetDescription>
    </SheetHeader>
    <form className="mt-6 space-y-4">
      ...
    </form>
  </SheetContent>
</Sheet>

/* Drawer — bottom panel for mobile */
<Drawer>
  <DrawerTrigger asChild>
    <Button variant="outline">Open Drawer</Button>
  </DrawerTrigger>
  <DrawerContent>
    <DrawerHeader>
      <DrawerTitle>Settings</DrawerTitle>
      <DrawerDescription>Configure your preferences</DrawerDescription>
    </DrawerHeader>
    ...
  </DrawerContent>
</Drawer>

/* Popover — quick action popup */
<Popover>
  <PopoverTrigger asChild>
    <Button variant="outline">Open</Button>
  </PopoverTrigger>
  <PopoverContent className="w-80">
    <div className="grid gap-4">
      <div className="space-y-2">
        <h4 className="font-medium leading-none">Dimensions</h4>
        <p className="text-sm text-muted-foreground">Set dimensions for the layer.</p>
      </div>
    </div>
  </PopoverContent>
</Popover>
```

## Component Groups That Must Stay Together

| Component | Required Children |
|---|---|
| `Select` | `SelectTrigger` (with children) + `SelectContent` + `SelectGroup` + `SelectItem` |
| `Tabs` | `TabsList` + `TabsTrigger` inside it + `TabsContent` |
| `Card` | `CardHeader` + optional `CardTitle`/`CardDescription` + `CardContent` + optional `CardFooter` |
| `Avatar` | `AvatarImage` + `AvatarFallback` |
| `AlertDialog` | `AlertDialogTrigger` + `AlertDialogContent` + `AlertDialogHeader` + `AlertDialogFooter` + `AlertDialogCancel` + `AlertDialogAction` |
| `Sheet` | `SheetTrigger` + `SheetContent` + `SheetHeader` + `SheetTitle` |
| `Drawer` | `DrawerTrigger` + `DrawerContent` + `DrawerHeader` + `DrawerTitle` |
| `Alert` | `AlertTitle` + `AlertDescription` |
| `Dialog` | `DialogTrigger` + `DialogContent` + `DialogTitle` |
