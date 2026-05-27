# Testing Lesson

Write tests to verify behavior, catch regressions, and document expected outcomes.

## Unit Tests

Test individual functions in isolation:

```typescript
import { describe, it, expect } from 'vitest';
import { getTotal, filterPositive } from './math';

describe('getTotal', () => {
  it('should sum positive and negative numbers', () => {
    expect(getTotal([1, -2, 3])).toBe(2);
  });

  it('should return 0 for empty array', () => {
    expect(getTotal([])).toBe(0);
  });

  it('should handle decimals', () => {
    expect(getTotal([1.5, 2.5])).toBe(4);
  });
});

describe('filterPositive', () => {
  it('should keep only positive numbers', () => {
    expect(filterPositive([1, -2, 3, 0])).toEqual([1, 3]);
  });
});
```

## Integration Tests

Test components and features end-to-end:

```typescript
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { LoginForm } from './login-form';

describe('LoginForm', () => {
  it('should display error on invalid email', async () => {
    render(<LoginForm />);

    const input = screen.getByPlaceholderText('Email');
    await userEvent.type(input, 'invalid-email');

    const button = screen.getByRole('button', { name: /submit/i });
    await userEvent.click(button);

    expect(screen.getByText('Invalid email')).toBeInTheDocument();
  });

  it('should submit form with valid data', async () => {
    const mockSubmit = vi.fn();
    render(<LoginForm onSubmit={mockSubmit} />);

    await userEvent.type(screen.getByPlaceholderText('Email'), 'user@example.com');
    await userEvent.type(screen.getByPlaceholderText('Password'), 'password');
    await userEvent.click(screen.getByRole('button', { name: /submit/i }));

    await waitFor(() => {
      expect(mockSubmit).toHaveBeenCalledWith({
        email: 'user@example.com',
        password: 'password'
      });
    });
  });
});
```

## Assertions

Use clear, descriptive assertions:

```typescript
// ✅ GOOD: Clear assertions
expect(user.name).toBe('John');
expect(users).toHaveLength(3);
expect(response).toContainEqual({ id: 1 });
expect(element).toBeInTheDocument();
expect(element).toHaveAttribute('aria-label', 'Close');

// ✅ GOOD: Grouped assertions
expect(result).toMatchObject({
  id: 1,
  name: 'John',
  email: 'john@example.com'
});

// ❌ BAD: Vague assertions
expect(user).toBeTruthy(); // What property?
expect(response).toBe(true); // What did we test?
```

## Test Structure (AAA Pattern)

```typescript
it('should update user profile', async () => {
  // ARRANGE: Set up test data
  const user = { id: 1, name: 'John', email: 'old@example.com' };
  const mockDb = { update: vi.fn() };

  // ACT: Execute the function
  await updateUser(user.id, { email: 'new@example.com' }, mockDb);

  // ASSERT: Verify results
  expect(mockDb.update).toHaveBeenCalledWith(1, { email: 'new@example.com' });
});
```

## Mocking

Mock external dependencies; test logic:

```typescript
// ✅ GOOD: Mock API calls
vi.mock('../api', () => ({
  fetchUser: vi.fn(() => Promise.resolve({ id: 1, name: 'John' }))
}));

it('should load user on mount', async () => {
  render(<UserProfile userId={1} />);
  await waitFor(() => {
    expect(screen.getByText('John')).toBeInTheDocument();
  });
});

// ❌ BAD: Test actual API
it('should load user on mount', async () => {
  render(<UserProfile userId={1} />);
  // This makes real HTTP request - slow, fragile!
  await waitFor(() => {
    expect(screen.getByText('John')).toBeInTheDocument();
  });
});
```

## Avoid These

| ❌ WRONG | ✅ RIGHT |
|---------|---------|
| Focused tests (`.only`) | Remove `.only` before commit |
| Skipped tests (`.skip`) | Delete or fix test |
| Testing implementation | Test behavior/output |
| No meaningful messages | Clear assertion descriptions |
| Testing random data | Fixed test data |
| No cleanup | Clean up after tests |

## Test Coverage Goals

- **Lines:** 80%+ coverage
- **Functions:** 100% (all code paths)
- **Branches:** 80%+ (if/else conditions)
- **Critical paths:** 100% (auth, payments, etc.)

Check with: `vitest run --coverage`

## Integration Tests for HTTP Endpoints

Test authenticated HTTP endpoints against a running server:

```typescript
import { beforeAll, describe, expect, test } from "bun:test"

const HOST = "http://localhost:3400"
let cookie = ""

// Helper: reusable request function
async function api(method: string, path: string, body?: unknown) {
  const opts: RequestInit = { method, headers: { "content-type": "application/json", cookie } }
  if (body) opts.body = JSON.stringify(body)
  const res = await fetch(`${HOST}${path}`, opts)
  return { status: res.status, data: await res.json() }
}

describe("Organizations", () => {
  beforeAll(async () => {
    // Create test user + get session cookie
    const { cookie: c } = await getAuthHeaders("admin")
    cookie = c
  })

  test("create org returns valid response", async () => {
    const { status, data } = await api("POST", "/v1/organizations", {
      name: "test-org",
      slug: "test-org",
    })
    expect(status).toBe(200)
    expect(data.code).toBe(1)
    expect(data.data.name).toBe("test-org")
  })
})
```

**Pattern:**
- Use `describeIf(!IS_PROD)` to skip tests in CI production
- Clean test data in `setup.ts` (DELETE with `test-` prefix)
- `getAuthHeaders(role)` creates user + returns cookie
- `toBeOneOf([200, 403])` for multiple valid status codes

## Testing Checklist

- ✅ Unit tests for utilities/services
- ✅ Integration tests for HTTP endpoints (against real server)
- ✅ E2E tests for critical flows
- ✅ Mock external APIs
- ✅ Use AAA pattern (Arrange, Act, Assert)
- ✅ Clear test names
- ✅ Clean test data before each suite
- ✅ 80%+ coverage
