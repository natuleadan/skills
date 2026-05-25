# TypeBox Models

Define reusable schemas with Elysia's TypeBox integration:

```typescript
import { t } from "elysia"

export const ProductSchema = t.Object({
  id: t.Number(),
  name: t.String(),
  price: t.Number(),
})
```

Use schemas in route definitions for validation and OpenAPI generation.
