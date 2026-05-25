# Code Examples

## Async Page with Metadata

```tsx
// app/products/[id]/page.tsx
import type { Metadata } from 'next'
import { notFound } from 'next/navigation'

export async function generateMetadata(props): Promise<Metadata> {
  const params = await props.params
  const product = await getProduct(params.id)

  if (!product) return { title: 'Not Found' }

  return {
    title: product.name,
    description: product.description,
    openGraph: {
      title: product.name,
      images: [{ url: product.image }]
    }
  }
}

export default async function ProductPage(props) {
  const params = await props.params
  const product = await getProduct(params.id)

  if (!product) notFound()

  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <ProductDetails product={product} />
    </div>
  )
}

// Client Component for interactivity
'use client'
function ProductDetails({ product }) {
  const [quantity, setQuantity] = useState(1)

  return (
    <div>
      <input
        type="number"
        value={quantity}
        onChange={e => setQuantity(Number(e.target.value))}
      />
    </div>
  )
}
```

## Cached Async Function

```tsx
// lib/products/queries.ts
import { cacheTag, cacheLife } from 'next/cache'

export async function getProducts() {
  'use cache'
  cacheLife('hours')
  cacheTag('products')

  const products = await db.products.findAll()
  return products
}

export async function getProductById(id: string) {
  'use cache'
  cacheLife('hours')
  cacheTag(`product:${id}`, 'products')

  const product = await db.products.findById(id)
  return product
}
```

## Server Action with Revalidation

```tsx
// app/products/actions.ts
'use server'

import { updateTag, revalidateTag } from 'next/cache'

export async function updateProduct(id: string, data: FormData) {
  const name = data.get('name')

  await db.products.update(id, { name })

  // Immediate refresh
  updateTag(`product:${id}`)

  // Or soft revalidate
  revalidateTag('products')
}
```

## Parallel Routes

```tsx
// app/layout.tsx
export default function Layout({ children, modal, sidebar }) {
  return (
    <div>
      <aside>{sidebar}</aside>
      <main>{children}</main>
      {modal}
    </div>
  )
}

// app/@modal/default.tsx
export default function ModalDefault() {
  return null
}

// app/@modal/[id]/page.tsx
export default async function ModalPage(props) {
  const params = await props.params
  return <Dialog id={params.id} />
}
```

## Dynamic OG Image

```tsx
// app/products/[id]/opengraph-image.tsx
import { ImageResponse } from 'next/og'

export const alt = 'Product OG Image'
export const size = { width: 1200, height: 630 }
export const contentType = 'image/png'

export default async function Image(props) {
  const params = await props.params
  const product = await getProduct(params.id)

  return (
    <ImageResponse>
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          width: '100%',
          height: '100%',
          backgroundColor: '#000',
          color: '#fff'
        }}
      >
        <h1 style={{ fontSize: 64 }}>{product.name}</h1>
        <p style={{ fontSize: 32 }}>${product.price}</p>
      </div>
    </ImageResponse>
  )
}
```

## Proxy.ts (Request Interception)

```tsx
// src/proxy.ts
import { next } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Check auth
  const token = request.cookies.get('auth-token')
  if (!token && request.nextUrl.pathname.startsWith('/admin')) {
    return new Response('Unauthorized', { status: 401 })
  }

  // Add header
  const response = next(request)
  response.headers.set('x-custom-header', 'value')

  return response
}

export const config = {
  matcher: ['/((?!_next|api|static).*)']
}
```

## Structured Data (JSON-LD)

```tsx
// app/products/[id]/page.tsx
export default async function ProductPage(props) {
  const params = await props.params
  const product = await getProduct(params.id)

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: product.name,
    description: product.description,
    image: product.image,
    offers: {
      '@type': 'Offer',
      price: product.price,
      priceCurrency: 'USD'
    }
  }

  return (
    <>
      <script type="application/ld+json">
        {JSON.stringify(jsonLd)}
      </script>
      <h1>{product.name}</h1>
    </>
  )
}
```
