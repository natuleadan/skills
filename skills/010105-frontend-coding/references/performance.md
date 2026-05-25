# Performance Lesson

Optimize for fast load times, smooth interactions, and efficient resource usage.

## Avoid N+1 Queries

Fetch all data in one query; don't loop and fetch:

```typescript
// ✅ GOOD: Batch query
const users = await db.users.findMany({
  where: { status: 'active' },
  include: { posts: true } // Join in one query
});

// ✅ GOOD: Query multiple IDs at once
const users = await db.users.findMany({
  where: { id: { in: [1, 2, 3] } }
});

// ❌ BAD: N+1 (1 query + N more queries)
const users = await db.users.find();
for (const user of users) {
  user.posts = await db.posts.find({ userId: user.id }); // N queries!
}

// ❌ BAD: Loop + query
for (const id of ids) {
  const user = await db.users.findOne(id); // Queries serially!
}
```

## Lazy Loading

Load components/code only when needed:

```tsx
// ✅ GOOD: Dynamic import (code splitting)
import dynamic from 'next/dynamic';

const HeavyChart = dynamic(() => import('./chart'), {
  loading: () => <div>Loading...</div>,
  ssr: false // Load only in browser
});

export function Dashboard() {
  return (
    <>
      <Summary />
      <HeavyChart /> {/* Loads on demand */}
    </>
  );
}

// ✅ GOOD: Lazy load images
<img src="image.jpg" loading="lazy" />

// ❌ BAD: Load everything upfront
import HeavyChart from './chart';
export function Dashboard() {
  return <HeavyChart />; // Heavy JS loaded immediately
}
```

## Memoization

Cache expensive calculations:

```typescript
// ✅ GOOD: Memoize expensive function
import { useMemo } from 'react';

function ExpensiveComponent({ items }) {
  const sorted = useMemo(() => {
    return items.sort((a, b) => a.value - b.value); // Only re-sort on items change
  }, [items]);

  return <div>{sorted.map(i => <div key={i.id}>{i.name}</div>)}</div>;
}

// ✅ GOOD: Cache API responses
const cache = new Map();

async function fetchUser(id) {
  if (cache.has(id)) return cache.get(id);
  const user = await api.getUser(id);
  cache.set(id, user);
  return user;
}

// ❌ BAD: Recalculate every render
function BadComponent({ items }) {
  const sorted = items.sort((a, b) => a.value - b.value); // Re-sorts on every render!
  return <div>{sorted.map(i => <div key={i.id}>{i.name}</div>)}</div>;
}
```

## Infinite Lists

Paginate or virtualize large lists:

```tsx
// ✅ GOOD: Pagination
function UserList() {
  const [page, setPage] = useState(1);
  const { data: users } = useFetch(`/api/users?page=${page}&limit=20`);

  return (
    <>
      {users.map(u => <UserItem key={u.id} user={u} />)}
      <button onClick={() => setPage(p => p + 1)}>Load more</button>
    </>
  );
}

// ✅ GOOD: Virtualization (only render visible rows)
import { FixedSizeList } from 'react-window';

function VirtualList({ items }) {
  return (
    <FixedSizeList
      height={600}
      itemCount={items.length}
      itemSize={50}
    >
      {({ index, style }) => (
        <div style={style}>{items[index].name}</div>
      )}
    </FixedSizeList>
  );
}

// ❌ BAD: Render all 10,000 items at once
{users.map(u => <UserItem key={u.id} user={u} />)}
```

## Bundle Size

Tree-shake unused code; use production builds:

```typescript
// ✅ GOOD: Import only what you use
import { format } from 'date-fns';
const date = format(new Date(), 'yyyy-MM-dd');

// ✅ GOOD: Use smaller alternatives
import dayjs from 'dayjs'; // 2kb vs date-fns 13kb

// ✅ GOOD: Code splitting
const Modal = dynamic(() => import('./modal'));

// ❌ BAD: Import entire library
import * as dateFns from 'date-fns';
const date = dateFns.format(new Date(), 'yyyy-MM-dd'); // Bundles all!

// ❌ BAD: No code splitting
import { HeavyChart } from './charts';
// 500kb chart JS loaded on home page!
```

## Images & Media

Optimize images; use modern formats:

```tsx
// ✅ GOOD: next/image (auto-optimization)
import Image from 'next/image';

<Image
  src="/photo.jpg"
  alt="Photo"
  width={640}
  height={480}
  quality={75}
  priority={false} // Lazy load
/>

// ✅ GOOD: WebP with fallback
<picture>
  <source srcSet="image.webp" type="image/webp" />
  <source srcSet="image.jpg" type="image/jpeg" />
  <img src="image.jpg" alt="" />
</picture>

// ❌ BAD: Large unoptimized image
<img src="/full-resolution-4mb.jpg" />

// ❌ BAD: No alt text (accessibility + SEO)
<img src="photo.jpg" />
```

## Caching Strategy

Cache HTTP responses; revalidate strategically:

```typescript
// ✅ GOOD: Cache with revalidation
export const revalidate = 3600; // Cache 1 hour

async function getProducts() {
  const res = await fetch('https://api.example.com/products', {
    next: { revalidate: 3600 } // ISR: revalidate after 1 hour
  });
  return res.json();
}

// ✅ GOOD: Cache + tags for manual invalidation
const products = await fetch(url, {
  next: { tags: ['products'] }
});

// Later, invalidate:
revalidateTag('products');

// ❌ BAD: No caching (fetch every request)
async function getProducts() {
  const res = await fetch('https://api.example.com/products');
  return res.json(); // no-store by default
}
```

## Performance Checklist

- ✅ No N+1 queries
- ✅ Lazy load components
- ✅ Memoize expensive functions
- ✅ Paginate/virtualize large lists
- ✅ Optimize images (WebP, sizing)
- ✅ Code split large features
- ✅ Cache API responses
- ✅ Use production builds
