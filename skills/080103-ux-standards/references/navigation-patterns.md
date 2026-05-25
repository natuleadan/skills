# Navigation Patterns Reference

Deep reference for navigation architecture: types, platform idioms, deep linking, state preservation, back stack, and gesture support.

---

## Navigation Types

### Bottom Tab Bar

| Platform | Guidelines |
|---|---|
| iOS | UITabBarController, always at bottom |
| Android | BottomNavigationView, Material 3 guidelines |
| Web (PWA) | Bottom nav bar, matches mobile convention |

**Rules:**
- Max 5 items (Apple HIG). 4 items is optimal.
- Each item: icon + label (both required)
- Active state: filled icon + accent color
- Do not scroll bottom tabs (they stay fixed)
- Badges: limited to notifications/counts, clear on visit

```tsx
<nav role="tablist" aria-label="Main navigation">
  <a href="/dashboard" aria-current="page" role="tab">
    <svg aria-hidden="true"><!-- dashboard icon --></svg>
    <span>Dashboard</span>
  </a>
  <a href="/products" role="tab">
    <svg aria-hidden="true"><!-- products icon --></svg>
    <span>Products</span>
  </a>
  <a href="/orders" role="tab">
    <svg aria-hidden="true"><!-- orders icon --></svg>
    <span>Orders</span>
  </a>
  <a href="/settings" role="tab">
    <svg aria-hidden="true"><!-- settings icon --></svg>
    <span>Settings</span>
  </a>
</nav>
```

### Sidebar / Drawer

**Use cases:**
- Primary navigation on desktop (sidebar)
- Secondary navigation on mobile (drawer)
- Admin panels, dashboards, content-heavy apps

**Patterns:**
```tsx
<aside role="navigation" aria-label="Sidebar">
  <div class="sidebar-header">
    <span class="app-name">App</span>
  </div>
  <ul class="nav-primary" role="list">
    <li><a href="/" aria-current="page">Home</a></li>
    <li>
      <button aria-expanded="true" aria-controls="sub-1">Projects</button>
      <ul id="sub-1" role="list">
        <li><a href="/projects/active">Active</a></li>
        <li><a href="/projects/archived">Archived</a></li>
      </ul>
    </li>
  </ul>
  <div class="nav-secondary">
    <ul role="list">
      <li><a href="/help">Help</a></li>
      <li><a href="/settings">Settings</a></li>
    </ul>
  </div>
</aside>
```

**Conventions:**
- Primary nav at top, secondary at bottom (separated visually)
- Collapsible sections for nested items
- Active item highlighted with accent color + background
- Width: 240–320px default, up to 400px for nav-heavy panels
- Drawer overlay on mobile: backdrop + tap-to-dismiss

### Tabs (Top/Content)

```html
<div role="tablist" aria-label="Report sections">
  <button role="tab" aria-selected="true" aria-controls="panel-overview" id="tab-overview">Overview</button>
  <button role="tab" aria-selected="false" aria-controls="panel-details" id="tab-details">Details</button>
  <button role="tab" aria-selected="false" aria-controls="panel-history" id="tab-history">History</button>
</div>
<div role="tabpanel" id="panel-overview" aria-labelledby="tab-overview">…</div>
<div role="tabpanel" id="panel-details" aria-labelledby="tab-details" hidden>…</div>
<div role="tabpanel" id="panel-history" aria-labelledby="tab-history" hidden>…</div>
```

- Tabs navigate within the same context (not top-level navigation)
- Scrollable tabs if more items than fit (never wrap)
- Active tab: underline + accent color

### Breadcrumbs

```html
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li aria-current="page">Wireless Headphones</li>
  </ol>
</nav>
```

- Use for 3+ levels deep
- Current page is the last item (text, not link) with `aria-current="page"`
- Separator: `/` or `›` (use CSS, not in markup)

### Search-Based Navigation
- Search bar accessible from top bar or prominent position
- Results should include category/type hints
- Recent searches pinned at top when search field is focused
- Keyboard: Arrow keys to navigate results, Enter to select, Escape to close

---

## Platform Idioms

### iOS (HIG)
- Tab bar at bottom for top-level sections only
- Navigation bar at top with title and back button
- Swipe-to-go-back: left edge swipe, system-wide
- Modal presentations: slide up from bottom, swipe down to dismiss
- Long press for context menus (Haptic Touch)

### Android (Material 3)
- Bottom navigation or Navigation Rail (tablet)
- Top app bar: title + hamburger/back + actions
- Navigation drawer for secondary navigation
- Back gesture: left or right edge swipe, system-wide
- Navigation rail on large screens: icons + labels, expandable

### Web
- Sidebar or top nav as primary navigation
- Breadcrumbs for deep hierarchies
- Back behavior: browser back button + history management
- Responsive: sidebar collapses to drawer on mobile

---

## Deep Linking

### Requirements
- Every key screen is directly reachable via a URL
- Structure: `/resource` → `/resource/:id` → `/resource/:id/section`
- Query parameters for filters, sort, page, search

```ts
// Good: predictable, hierarchical
/products
/products/wireless-headphones
/products/wireless-headphones/reviews

// Good: search and filter state via query params
/products?category=audio&sort=price&page=2

// Bad: opaque IDs without readable context
/product/a3f7b2
```

### Deep Linking in App
- Push notifications must link to the relevant content
- External links (emails, SMS) must resolve to the right screen in-app
- Handle unauthenticated users: redirect to login, then deep link after auth

---

## State Preservation

### Scroll Position
```ts
// Save before navigating away
function saveScroll(key: string) {
  sessionStorage.setItem(`scroll:${key}`, String(window.scrollY));
}

// Restore on mount
function restoreScroll(key: string) {
  const y = sessionStorage.getItem(`scroll:${key}`);
  if (y) requestAnimationFrame(() => window.scrollTo(0, parseInt(y, 10)));
}
```

### Filter & Search State
```ts
// Sync filter state to URL query params (for deep link + back support)
function useFilterState(defaults: Record<string, string>) {
  const [searchParams, setSearchParams] = useSearchParams();

  const filters = useMemo(() => ({
    search: searchParams.get('q') ?? defaults.search,
    category: searchParams.get('category') ?? defaults.category,
    page: parseInt(searchParams.get('page') ?? '1', 10),
    sort: searchParams.get('sort') ?? defaults.sort,
  }), [searchParams]);

  const setFilter = (key: string, value: string | number) => {
    setSearchParams(prev => {
      const next = new URLSearchParams(prev);
      if (value) next.set(key, String(value));
      else next.delete(key);
      return next;
    }, { replace: true });
  };

  return { filters, setFilter };
}
```

### Input State
- Form draft autosave (see form-ux.md)
- On back navigation, preserve form input values
- Use `sessionStorage` for temporary state, `localStorage` for draft forms

---

## Back Stack

### Web
- `history.pushState` / `replaceState` for client-side nav
- Do NOT silently replace the current history entry unless it's a redirect
- When opening a modal from a page, consider `replaceState` to keep modal as current history entry
- When dismissing modal, `history.back()` (or `popstate` handler)

```ts
// Open modal — push state
history.pushState({ modal: true }, '', window.location.href);

// Close modal — go back
function dismissModal() {
  if (window.history.state?.modal) {
    history.back();
  }
}

// Listen for popstate to close modal on OS back
window.addEventListener('popstate', (e) => {
  if (e.state?.modal) {
    closeModalUI();
  }
});
```

### Mobile (iOS/Android)
- Navigation stack: push screen → back = pop screen
- Deep link → push onto navigation stack, system back returns to previous app
- Do not manipulate back stack unless necessary (e.g., after login, clear login screen from stack)
- Tab switching should preserve each tab's navigation stack

---

## Adaptive Navigation

### Screen Size Breakpoints

| Breakpoint | Navigation | Layout |
|---|---|---|
| < 600px (phone) | Bottom tab bar + top app bar | Single column |
| 600–1024px (tablet portrait) | Bottom tab bar or navigation rail | Two column |
| 1024+ (desktop) | Sidebar + top bar | Multi column |

```tsx
function AppNavigation() {
  const isMobile = useMediaQuery('(max-width: 599px)');
  const isTablet = useMediaQuery('(min-width: 600px) and (max-width: 1023px)');
  const isDesktop = useMediaQuery('(min-width: 1024px)');

  if (isDesktop) return <Sidebar />;
  if (isTablet) return <NavigationRail />;
  return <BottomTabBar />;
}
```

### Navigation Rail (Material 3)

A compact sidebar for mid-size screens — wider than bottom nav but narrower than full sidebar. Icons initially, labels on expansion.

---

## Common Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Tab bar + sidebar in same view | Conflicting navigation paradigms | Pick one based on platform |
| Tab bar items that drill deep | Violates "top-level only" rule | Use push navigation within tab |
| No active state on nav items | User doesn't know where they are | Always highlight current |
| Overloaded nav items (10+ on bottom) | Cognitive load, touch target cramming | Overflow + "More" menu |
| Gesture conflicts (swipe nav on main content) | Unintended navigation | `touch-action: pan-y` |
| Back button resets form | Loss of user input | Preserve state or confirm discard |
| Deep links only work when authenticated | Broken flow after login | Implement post-auth redirect |

---

## Navigation Accessibility

- Landmarks: `<nav>` with `aria-label` to distinguish multiple navs
- Active state: `aria-current="page"` or `aria-current="true"`
- Tabs: `role="tablist"`, `role="tab"`, `aria-selected`, `role="tabpanel"`
- Skip link as first focusable element
- Focus on route change: move to `<h1>` or main container
- Keyboard: Tab between nav items, Arrow keys within tablist/menu
- Expand/collapse: `aria-expanded` and `aria-controls` on buttons
