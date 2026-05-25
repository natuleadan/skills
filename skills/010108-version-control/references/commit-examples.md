# Commit Message Examples

Real commit message examples per type.

## MAJOR — `upgrade`

```
upgrade(env): require new encryption key for server actions

⚠️ BREAKING: All multi-pod deployments must now set
NEXT_SERVER_ACTIONS_ENCRYPTION_KEY in .env.

Without this key, cross-pod Server Actions will fail silently.
```

```
upgrade(api): remove deprecated v1 endpoints

⚠️ BREAKING: /api/v1/* routes are no longer available.
Migrate to /api/v2/* before deploying.
```

## MINOR — `feat`

```
feat(auth): add google oauth callback
```

```
feat(products): add ratings and reviews
```

```
feat(dashboard): add export to csv button
```

## PATCH — `fix`

```
fix(auth): validate token format before decoding
```

```
fix(cache): prevent stale data in multi-pod deployment
```

```
fix(api): return 404 instead of 500 for missing resource
```

## PATCH — `perf`

```
perf(api): batch redis calls to reduce round trips
```

```
perf(db): add index on orders.user_id for faster lookups
```

## PATCH — `revert`

```
revert(auth): revert "add device flow oauth"

Reverts commit abc1234. Feature caused login loop on Safari.
```

## NONE — `docs`

```
docs(readme): update local setup instructions
```

```
docs(architecture): add multi-server deployment diagram
```

## NONE — `style`

```
style(auth): fix indentation in login component
```

## NONE — `refactor`

```
refactor(cache): simplify key generation logic
```

```
refactor(auth): extract token validation to separate function
```

## NONE — `test`

```
test(auth): add login flow integration tests
```

```
test(api): add edge case tests for pagination
```

## NONE — `chore`

```
chore(deps): update eslint to v9
```

```
chore(config): add prettier configuration
```

## NONE — `ci`

```
ci(github): add semantic-release workflow
```

```
ci(github): fix node version in deploy job
```

## With issue reference (body)

```
fix(checkout): prevent duplicate order submission

Fixes #412
```

```
feat(notifications): add email digest option

Closes #318
Closes #290
```
