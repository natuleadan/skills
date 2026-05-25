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
  if (condition) useEffect(() => {}, []); // React Error!
  return <input />;
}

// ❌ BAD: Hook inside loop
for (let i = 0; i < 5; i++) {
  useState(i); // React can't track state!
}
```

## Keys in Lists

Always use stable, unique keys (not array indexes):

```tsx
// ✅ GOOD: Stable key (item.id)
{items.map(item => (
  <li key={item.id}>{item.name}</li>
))}

// ❌ BAD: Array index (breaks if list reorders)
{items.map((item, i) => (
  <li key={i}>{item.name}</li>
))}

// ❌ BAD: No key
{items.map(item => (
  <li>{item.name}</li>
))}
```

## Composition & Prop Drilling

Pass data as props; avoid excessive nesting:

```tsx
// ✅ GOOD: Direct props
<Header user={user} />
<Main user={user} />
<Footer user={user} />

// ✅ GOOD: Context for deeply nested (if needed)
const UserContext = createContext(null);

function App() {
  return (
    <UserContext.Provider value={user}>
      <Header />
      <Main />
    </UserContext.Provider>
  );
}

function DeepComponent() {
  const user = useContext(UserContext);
  return <div>{user.name}</div>;
}

// ❌ BAD: Too much prop drilling
<Header user={user} theme={theme} lang={lang} />
<Main user={user} theme={theme} lang={lang} />
<Footer user={user} theme={theme} lang={lang} />
```

## Dependencies in Hooks

Specify all dependencies; don't ignore warnings:

```tsx
// ✅ GOOD: Dependencies listed
const userId = props.userId;
useEffect(() => {
  fetch(`/api/users/${userId}`).then(setUser);
}, [userId]); // userId is a dependency

// ❌ BAD: Missing dependency
useEffect(() => {
  fetch(`/api/users/${userId}`).then(setUser);
}, []); // userId isn't listed! Stale closure.
```

## Client Component Best Practices

Push Client Components to leaf level:

```tsx
// ✅ GOOD: Client Component is leaf
export function App() {
  const data = await fetchData();
  return <ClientCounter data={data} />;
}

'use client';
function ClientCounter({ data }) {
  const [count, setCount] = useState(0);
  return <div>{data} - {count}</div>;
}

// ❌ BAD: Client Component wraps everything
'use client';
export async function App() {
  const data = await fetchData(); // Can't use await in Client Component!
  return <ClientCounter />;
}
```

## Anti-Patterns

| ❌ WRONG | ✅ RIGHT |
|---------|---------|
| Client Component for data fetching | Server Component or Route Handler |
| Array index as key | Stable unique ID |
| Missing dependencies | List all dependencies |
| Hook inside condition | Top-level hook calls |
| Prop drilling 5+ levels | Context or composition |
| useEffect for sync logic | Regular functions |

## Composition Pattern (Server + Client)

```tsx
// app/layout.tsx (Server)
export default async function Layout({ children }) {
  const user = await getUser();
  return (
    <html>
      <body>
        <Header user={user} />
        {children}
      </body>
    </html>
  );
}

// app/page.tsx (Server)
export default async function Page() {
  const data = await fetchData();
  return <Main data={data} />;
}

// components/main.tsx (Client)
'use client';
import { useState } from 'react';

export function Main({ data }) {
  const [tab, setTab] = useState('overview');
  return (
    <div>
      <button onClick={() => setTab('details')}>Details</button>
      {tab === 'overview' && <div>{data.overview}</div>}
    </div>
  );
}
```
