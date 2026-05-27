# React Best Practices Lesson

Write efficient, maintainable React code with Server Components, proper hooks, and composition patterns.

## Server Components by Default

Use Server Components for data fetching; Client Components only for interactivity:

```tsx
// ✅ GOOD: Server Component (data fetching)
export default async function Page() {
  const data = await fetchData();
  return <div>{data}</div>;
}

// ✅ GOOD: Client Component (interactive)
'use client';
import { useState } from 'react';

export function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}

// ❌ BAD: Client Component fetching data
'use client';
export function Page() {
  const [data, setData] = useState(null);
  useEffect(() => { fetch().then(setData); }, []);
  // Slow waterfall, poor UX, extra JS
  return <div>{data}</div>;
}
```

## Hooks Rules

Hooks must be called at top level, not inside conditions:

```tsx
// ✅ GOOD: Hooks at top level
export function Form() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');

  return <input value={name} onChange={(e) => setName(e.target.value)} />;
}

// ❌ BAD: Hook inside condition
export function BadForm() {
  if (someCondition) {
    const [name, setName] = useState(''); // Runtime error!
  }
}
```

## Keys in Lists

```tsx
const items = [{ id: 1, name: 'A' }, { id: 2, name: 'B' }];

// ✅ GOOD: Stable unique ID
items.map((item) => <li key={item.id}>{item.name}</li>);

// ❌ BAD: Array index as key (breaks state, focus, and accessibility)
items.map((item, index) => <li key={index}>{item.name}</li>);
```

## Composition & Prop Drilling

```tsx
// ✅ GOOD: Component composition (children, slots)
function Layout({ header, sidebar, children }: { header: React.ReactNode; sidebar: React.ReactNode; children: React.ReactNode }) {
  return (
    <div>
      <header>{header}</header>
      <aside>{sidebar}</aside>
      <main>{children}</main>
    </div>
  );
}

// ❌ BAD: Prop drilling through 5+ levels
function Page({ user }: { user: User }) {
  return <MainLayout user={user} />;
}
function MainLayout({ user }: { user: User }) {
  return <Sidebar user={user} />;
}
```

## Dependencies in Hooks

```tsx
// ✅ GOOD: All dependencies listed
useEffect(() => {
  fetchData(id);
}, [id, fetchData]);

// ❌ BAD: Missing dependency (stale closure)
useEffect(() => {
  fetchData(id);
}, []); // id changes silently ignored

// ✅ GOOD: useCallback for function stability
const handleSave = useCallback(async () => {
  await api.save(data);
}, [data]);
```

## Client Component Best Practices

```tsx
// ✅ GOOD: Push interactivity to leaf components
'use client';
function LikeButton({ postId }: { postId: string }) {
  const [liked, setLiked] = useState(false);
  return <button onClick={() => setLiked(!liked)}>Like</button>;
}

// ✅ GOOD: Separate auth-dependent content with mounted pattern
function DashboardSidebar() {
  const { data: session } = authClient.useSession();
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);

  return (
    <div>
      {mounted ? (
        <span>{session?.user?.name ?? "Guest"}</span>
      ) : (
        <span>...</span>  // Same content on server + client during hydration
      )}
    </div>
  );
}
```

## Hydration Pattern

Client Components that depend on browser-only data (auth session, localStorage, window size) must handle hydration mismatch:

```tsx
function OrgSwitcher() {
  const { data: orgs } = authClient.useListOrganizations();
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);

  return (
    <span>
      {mounted ? (orgs?.[0]?.name ?? "No org") : "..."}
    </span>
  );
}
```

**Why it works:** Server renders `"..."` (no session). Client hydrates with `"..."`. After hydration, `useEffect` flips `mounted` to `true`, showing real data. No mismatch.

## Dashboard Tab Pattern

For detail pages with multiple sections, use shadcn `Tabs` with a `TabsTrigger` per tab and `TabsContent` per section:

```tsx
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

function OrgDetailPage() {
  const [tab, setTab] = useState("settings")

  return (
    <Tabs value={tab} onValueChange={setTab}>
      <TabsList>
        <TabsTrigger value="settings">Settings</TabsTrigger>
        <TabsTrigger value="members">Members</TabsTrigger>
      </TabsList>
      <TabsContent value="settings">
        <SettingsForm />
      </TabsContent>
      <TabsContent value="members">
        <MembersList />
      </TabsContent>
    </Tabs>
  )
}
```

## Preference for Cards

Group related form fields inside shadcn `Card` components:

```tsx
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Field, FieldGroup, FieldLabel } from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

<Card>
  <CardHeader>
    <CardTitle>Profile</CardTitle>
    <CardDescription>Update your display name and avatar.</CardDescription>
  </CardHeader>
  <CardContent>
    <FieldGroup className="grid grid-cols-2 gap-3">
      <Field>
        <FieldLabel htmlFor="name">Name</FieldLabel>
        <Input id="name" placeholder="John Doe" />
      </Field>
    </FieldGroup>
    <div className="mt-4 flex justify-end gap-2">
      <Button type="submit">Save</Button>
    </div>
  </CardContent>
</Card>
```

## Anti-Patterns

- Do NOT use `useEffect` for derived state — compute directly
- Do NOT store props in `useState` — read them directly or use `useMemo`
- Do NOT nest Client Components inside other Client Components unnecessarily
- Do NOT use `useState` + `useEffect` for data fetching — use React Query, SWR, or Server Components

## Composition Pattern (Server + Client)

```tsx
// Page.server.tsx — Server Component
import { ClientList } from './ClientList';

export default async function Page() {
  const items = await db.findMany(); // Fetch on server
  return <ClientList items={items} />; // Pass data to client
}

// ClientList.client.tsx — Client Component
'use client';
export function ClientList({ items }: { items: Item[] }) {
  const [filter, setFilter] = useState('');
  const filtered = items.filter(i => i.name.includes(filter));
  return (
    <div>
      <input value={filter} onChange={e => setFilter(e.target.value)} />
      {filtered.map(i => <div key={i.id}>{i.name}</div>)}
    </div>
  );
}
```
