# Dual Auth (API Key + Session)

## requireApiKeyOrSession

```typescript
export async function requireApiKeyOrSession(
  headers: Headers,
  permissions: Record<string, string[]>
): Promise<PermissionCheck> {
  const authHeader = headers.get("authorization")
  if (authHeader?.startsWith("Bearer ")) {
    const result = await auth.api.verifyApiKey({ body: { key, permissions } })
    if (result.valid) return { ok: true }
    return { ok: false, error: { status: 401, message: "Invalid API key" } }
  }
  return requirePermission(headers, permissions)
}
```

## requirePermission (session-based)

```typescript
export async function requirePermission(headers, permissions) {
  const sesResult = await authApi.getSession(headers)
  if (!sesResult.ok) return { ok: false, error: { status: 401 } }
  if (sesResult.data.user.role === "admin") return { ok: true }
  const roleObj = roles[sesResult.data.user.role]
  if (!roleObj) return { ok: false, error: { status: 403 } }
  const result = roleObj.authorize(permissions)
  if (!result.success) return { ok: false, error: { status: 403 } }
  return { ok: true }
}
```
