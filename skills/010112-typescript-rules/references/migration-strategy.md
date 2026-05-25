# Migration Strategy Lesson

Converting JavaScript to TypeScript incrementally.

## Incremental Approach

Don't convert entire codebase at once.

1. **Set up TypeScript** — `npm install typescript`
2. **Configure tsconfig.json** — start with lenient settings
3. **Rename first file** — `.js` → `.ts`
4. **Add annotations gradually** — most critical first
5. **Enable strict options** — one at a time
6. **Test thoroughly** — each stage

## Initial tsconfig.json (Lenient)

```json
{
  "compilerOptions": {
    "target": "ES2024",
    "module": "ESNext",
    "strict": false,
    "allowJs": true,
    "checkJs": false,
    "skipLibCheck": true
  }
}
```

Then gradually:
- Change `strict: false` → `strict: true`
- Enable `noImplicitAny: true`
- Enable `strictNullChecks: true`
- Enable `noUncheckedIndexedAccess: true`

## JSDoc for Gradual Typing

Use JSDoc in `.js` files before full migration:

```javascript
/**
 * @param {string} name
 * @param {number} age
 * @returns {{ name: string, age: number }}
 */
function createUser(name, age) {
  return { name, age }
}
```

## Library Types

- **Typed npm packages** — prefer packages with built-in `@types` or `.d.ts`
- **DefinitelyTyped** — `npm install --save-dev @types/package-name`
- **Check package.json** — look for `types` or `typings` field

## Common Migration Issues

- **Missing types** — install @types/* packages
- **Circular dependencies** — refactor imports
- **Dynamic requires** — use static imports where possible
- **Global variables** — declare in `.d.ts` files

## Rules

- [ ] **Incremental** — don't migrate all at once
- [ ] **Start lenient** — enable strict options gradually
- [ ] **Test each stage** — verify nothing breaks
- [ ] **Use JSDoc** — for gradual typing in .js files
- [ ] **Install @types** — for third-party libraries
- [ ] **Fix root causes** — don't ignore errors with @ts-ignore
