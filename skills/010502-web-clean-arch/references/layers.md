# Clean Architecture Layers Reference

## Layer Definitions

### Domain Layer

Pure business entities and business rules. No framework imports, no I/O.

```typescript
// domain/entities/product.ts
export interface Product {
  id: string
  name: string
  price: number
  category: string
}

export function applyDiscount(product: Product, percent: number): Product {
  return { ...product, price: product.price * (1 - percent / 100) }
}
```

### Application Layer

Use cases orchestrate domain entities and call infrastructure ports.

```typescript
// application/services/cart-service.ts
import type { ProductRepository } from "@/domain/ports/product-repository"

export async function addToCart(
  repo: ProductRepository,
  userId: string,
  productId: string,
  quantity: number
) {
  const product = await repo.findById(productId)
  if (!product) throw new Error("Product not found")
  if (product.stock < quantity) throw new Error("Insufficient stock")
  // ... add to cart logic
}
```

### Infrastructure Layer

Concrete implementations of domain ports.

```typescript
// infrastructure/repositories/product-repository.ts
import type { ProductRepository } from "@/domain/ports/product-repository"
import { db } from "@/infrastructure/database/client"

export const createProductRepo = (): ProductRepository => ({
  async findById(id: string) {
    const row = await db.query("SELECT * FROM products WHERE id = $1", [id])
    return row ? mapToProduct(row) : null
  },
})
```

### Actions Layer

Entry points — thin wrappers that validate auth and delegate.

```typescript
// actions/products/add-to-cart.ts
"use server"
import { addToCart } from "@/application/services/cart-service"
import { createProductRepo } from "@/infrastructure/repositories/product-repository"

export async function addToCartAction(formData: FormData) {
  const productId = formData.get("productId") as string
  const quantity = Number(formData.get("quantity"))
  return addToCart(createProductRepo(), "current-user", productId, quantity)
}
```

## Data Flow Example

```
Component (form submit)
  → Action (validate auth, call service)
    → Application/Service (orchestrate business logic)
      → Infrastructure/Repository (query DB)
        → Domain/Entity (pure business rules)
      ← Result
    ← Response
  ← UI update
```

## Common Anti-Patterns

| Anti-pattern | Problem | Fix |
|---|---|---|
| Service calls service | Circular dependencies | Extract shared logic to domain |
| Action calls repository directly | Bypasses business rules | Route through application service |
| Domain import from infrastructure | Dependency inversion broken | Define port interface in domain |
| UI imports from infrastructure | Tight coupling | Use actions as mediator |
| Fat controller/action | Business logic in entry point | Extract to application layer |
