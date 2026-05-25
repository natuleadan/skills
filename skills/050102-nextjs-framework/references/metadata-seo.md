# Metadata & SEO

Use Metadata API in Server Components exclusively.

## generateMetadata

Async function in layout.tsx or page.tsx:

```tsx
import type { Metadata } from 'next'

export async function generateMetadata(props): Promise<Metadata> {
  const params = await props.params
  const product = await db.products.findById(params.id)

  return {
    title: product.name,
    description: product.description,
    openGraph: {
      title: product.name,
      description: product.description,
      url: `https://example.com/products/${params.id}`,
      images: [{ url: product.image }]
    }
  }
}

export default async function ProductPage(props) {
  const params = await props.params
  const product = await db.products.findById(params.id)

  return <div>{product.name}</div>
}
```

## Dynamic OG Images

File-based: `opengraph-image.tsx` (or `.jsx`):

```tsx
import { ImageResponse } from 'next/og'

export const alt = 'Product'
export const size = { width: 1200, height: 630 }

export default async function Image(props) {
  const params = await props.params
  const product = await db.products.findById(params.id)

  return (
    <ImageResponse>
      <div style={{ fontSize: 64 }}>{product.name}</div>
    </ImageResponse>
  )
}
```

## Structured Data (JSON-LD)

Use in Server Component `<head>`:

```tsx
export default async function Page(props) {
  const params = await props.params
  const product = await db.products.findById(params.id)

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: product.name,
    description: product.description,
    image: product.image,
    price: product.price
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

## Rules

- [ ] **generateMetadata is async** — can fetch data
- [ ] **Await params and searchParams** — in metadata and page
- [ ] **Dynamic OG images** — via opengraph-image.tsx
- [ ] **JSON-LD in script tags** — use JSON.stringify
- [ ] **Never in Client Components** — Metadata API is server-only
