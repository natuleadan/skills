# Structured Data Reference (JSON-LD)

## Overview

Structured data provides explicit clues about the meaning of a page to search engines. JSON-LD (JavaScript Object Notation for Linked Data) is the recommended format because it keeps structured data separate from HTML content.

## Schema.org Context

Every JSON-LD snippet starts with a `@context` set to `https://schema.org` and a `@type` specifying the schema type.

```json
{
  "@context": "https://schema.org",
  "@type": "TypeName",
  "property": "value"
}
```

The `@id` property provides a globally unique identifier (usually the URL):

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "@id": "https://example.com/authors/john-doe",
  "name": "John Doe"
}
```

## Common Schema Types

### Organization

Required: `name` and either `url` or `logo`.

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://example.com/#organization",
  "name": "Example Inc.",
  "url": "https://example.com",
  "logo": {
    "@type": "ImageObject",
    "url": "https://example.com/logo.png",
    "width": 600,
    "height": 60
  },
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+1-555-555-5555",
    "contactType": "customer service",
    "areaServed": "US",
    "availableLanguage": ["English", "Spanish"]
  },
  "sameAs": [
    "https://www.facebook.com/example",
    "https://twitter.com/example",
    "https://www.linkedin.com/company/example",
    "https://www.instagram.com/example"
  ],
  "description": "Example Inc. provides high-quality widgets and services."
}
```

### WebSite (with Sitelinks Search Box)

Required: `name`, `url`. For sitelinks search box: `potentialAction`, `SearchAction`.

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "@id": "https://example.com/#website",
  "name": "Example",
  "url": "https://example.com",
  "description": "Your source for quality widgets and tools.",
  "potentialAction": {
    "@type": "SearchAction",
    "target": {
      "@type": "EntryPoint",
      "urlTemplate": "https://example.com/search?q={search_term_string}"
    },
    "query-input": "required name=search_term_string"
  }
}
```

### WebPage

Recommended: `name`, `description`, `breadcrumb`, `lastReviewed`.

```json
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "@id": "https://example.com/seo-guide#webpage",
  "name": "Technical SEO Guide",
  "description": "A comprehensive guide to technical SEO optimization.",
  "url": "https://example.com/seo-guide",
  "lastReviewed": "2026-05-25",
  "dateCreated": "2026-01-15",
  "dateModified": "2026-05-25",
  "breadcrumb": {
    "@type": "BreadcrumbList",
    "itemListElement": [
      {
        "@type": "ListItem",
        "position": 1,
        "name": "Home",
        "item": "https://example.com"
      },
      {
        "@type": "ListItem",
        "position": 2,
        "name": "Guides",
        "item": "https://example.com/guides"
      },
      {
        "@type": "ListItem",
        "position": 3,
        "name": "SEO Guide",
        "item": "https://example.com/seo-guide"
      }
    ]
  },
  "mainContentOfPage": {
    "@type": "WebPageElement",
    "name": "Main content",
    "description": "Technical SEO optimization guide content"
  }
}
```

### Article

Required for rich results: `headline`, `image`, `datePublished`.

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "@id": "https://example.com/blog/seo-guide#article",
  "headline": "Technical SEO Optimization Guide",
  "description": "A comprehensive guide to technical SEO best practices including sitemaps, robots.txt, and structured data.",
  "image": {
    "@type": "ImageObject",
    "url": "https://example.com/images/seo-guide-hero.jpg",
    "width": 1200,
    "height": 630
  },
  "author": {
    "@type": "Person",
    "@id": "https://example.com/authors/john-doe#person",
    "name": "John Doe",
    "url": "https://example.com/authors/john-doe"
  },
  "publisher": {
    "@type": "Organization",
    "@id": "https://example.com/#organization",
    "name": "Example Inc.",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png",
      "width": 600,
      "height": 60
    }
  },
  "datePublished": "2026-01-15T10:00:00Z",
  "dateModified": "2026-05-25T14:30:00Z",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://example.com/blog/seo-guide"
  },
  "wordCount": 2500,
  "articleSection": "SEO",
  "keywords": ["technical SEO", "sitemaps", "robots.txt", "structured data"]
}
```

### BreadcrumbList

Displayed as breadcrumb trails in SERPs. Required: `position`, `name`, `item` for each item.

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "@id": "https://example.com/seo-guide#breadcrumb",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://example.com"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Guides",
      "item": "https://example.com/guides"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "SEO Guide",
      "item": "https://example.com/seo-guide"
    }
  ]
}
```

### Product

Required for Google Shopping: `name`, `offers` with `price`, `priceCurrency`, `availability`.

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "@id": "https://example.com/products/widget#product",
  "name": "Premium Widget",
  "description": "A high-quality widget designed for maximum durability and performance.",
  "sku": "WGT-001",
  "mpn": "EXAMPLE-WGT-001",
  "brand": {
    "@type": "Brand",
    "name": "Example"
  },
  "image": [
    "https://example.com/images/widget-main.jpg",
    "https://example.com/images/widget-side.jpg"
  ],
  "offers": [
    {
      "@type": "Offer",
      "@id": "https://example.com/products/widget#offer",
      "price": "29.99",
      "priceCurrency": "USD",
      "priceValidUntil": "2027-12-31",
      "availability": "https://schema.org/InStock",
      "itemCondition": "https://schema.org/NewCondition",
      "url": "https://example.com/products/widget",
      "shippingDetails": {
        "@type": "OfferShippingDetails",
        "shippingRate": {
          "@type": "MonetaryAmount",
          "value": "5.99",
          "currency": "USD"
        },
        "deliveryTime": {
          "@type": "ShippingDeliveryTime",
          "handlingTime": {
            "@type": "QuantitativeValue",
            "minValue": 1,
            "maxValue": 2,
            "unitCode": "DAY"
          },
          "transitTime": {
            "@type": "QuantitativeValue",
            "minValue": 3,
            "maxValue": 5,
            "unitCode": "DAY"
          }
        }
      }
    }
  ],
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.5",
    "reviewCount": 128,
    "bestRating": "5"
  },
  "review": [
    {
      "@type": "Review",
      "author": {
        "@type": "Person",
        "name": "Jane Smith"
      },
      "datePublished": "2026-05-20",
      "reviewBody": "Great widget! Exceeded my expectations.",
      "reviewRating": {
        "@type": "Rating",
        "ratingValue": "5"
      }
    }
  ]
}
```

### LocalBusiness

Required: `name`, `address`.

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "@id": "https://example.com/cafe#business",
  "name": "Example Cafe",
  "description": "A cozy cafe serving artisan coffee and fresh pastries.",
  "url": "https://example.com/cafe",
  "image": "https://example.com/images/cafe.jpg",
  "telephone": "+1-555-555-5555",
  "email": "hello@example.com",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main Street",
    "addressLocality": "Anytown",
    "addressRegion": "CA",
    "postalCode": "12345",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 40.7128,
    "longitude": -74.006
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "07:00",
      "closes": "18:00"
    },
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Saturday", "Sunday"],
      "opens": "08:00",
      "closes": "15:00"
    }
  ],
  "servesCuisine": ["Coffee", "Pastries", "Sandwiches"],
  "priceRange": "$$",
  "paymentAccepted": ["Cash", "Credit Card", "Mobile Pay"],
  "sameAs": [
    "https://www.facebook.com/examplecafe",
    "https://www.instagram.com/examplecafe"
  ]
}
```

### FAQPage

Enables rich FAQ results in SERPs. Required: `mainEntity` with `Question`/`Answer` pairs.

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "@id": "https://example.com/faq#faqpage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is technical SEO?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Technical SEO refers to website and server optimizations that help search engines crawl, index, and render your pages effectively. It includes sitemaps, robots.txt, site speed, structured data, and more."
      }
    },
    {
      "@type": "Question",
      "name": "How does a sitemap help SEO?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "A sitemap lists all URLs on your site that you want search engines to index. It helps discover pages that might not be found through normal crawling, especially new or deeply nested content."
      }
    },
    {
      "@type": "Question",
      "name": "What is JSON-LD?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "JSON-LD (JavaScript Object Notation for Linked Data) is a format for encoding structured data. Google recommends JSON-LD because it keeps data separate from HTML and is easier to implement than Microdata or RDFa."
      }
    }
  ]
}
```

### Review

```json
{
  "@context": "https://schema.org",
  "@type": "Review",
  "@id": "https://example.com/reviews/widget#review-1",
  "itemReviewed": {
    "@type": "Product",
    "@id": "https://example.com/products/widget#product",
    "name": "Premium Widget"
  },
  "reviewRating": {
    "@type": "Rating",
    "ratingValue": "5",
    "bestRating": "5",
    "worstRating": "1"
  },
  "author": {
    "@type": "Person",
    "name": "Jane Smith"
  },
  "datePublished": "2026-05-20",
  "reviewBody": "I've been using the Premium Widget for three months and it's fantastic. Build quality is outstanding and it performs exactly as described."
  }
}
```

### Event

```json
{
  "@context": "https://schema.org",
  "@type": "Event",
  "@id": "https://example.com/events/seo-conference#event",
  "name": "SEO Conference 2026",
  "description": "The premier conference for SEO professionals featuring workshops, keynotes, and networking.",
  "startDate": "2026-09-15T09:00:00-05:00",
  "endDate": "2026-09-17T18:00:00-05:00",
  "eventStatus": "https://schema.org/EventScheduled",
  "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
  "location": {
    "@type": "Place",
    "name": "Grand Convention Center",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "789 Convention Drive",
      "addressLocality": "Metropolis",
      "addressRegion": "NY",
      "postalCode": "10001",
      "addressCountry": "US"
    }
  },
  "image": "https://example.com/images/conference-hero.jpg",
  "offers": [
    {
      "@type": "Offer",
      "name": "Early Bird Ticket",
      "price": "299.00",
      "priceCurrency": "USD",
      "availability": "https://schema.org/InStock",
      "validFrom": "2026-06-01T00:00:00Z",
      "url": "https://example.com/events/seo-conference/register"
    },
    {
      "@type": "Offer",
      "name": "Standard Ticket",
      "price": "499.00",
      "priceCurrency": "USD",
      "availability": "https://schema.org/InStock",
      "url": "https://example.com/events/seo-conference/register"
    }
  ],
  "performer": [
    {
      "@type": "Person",
      "name": "Jane Smith",
      "jobTitle": "SEO Specialist"
    },
    {
      "@type": "Organization",
      "name": "Example Inc."
    }
  ],
  "organizer": {
    "@type": "Organization",
    "name": "Example Events",
    "url": "https://example.com"
  }
}
```

## Multiple Entities on One Page

Use `@graph` to include multiple schema types on a single page:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://example.com/#organization",
      "name": "Example Inc.",
      "url": "https://example.com",
      "logo": "https://example.com/logo.png"
    },
    {
      "@type": "WebSite",
      "@id": "https://example.com/#website",
      "name": "Example",
      "url": "https://example.com",
      "potentialAction": {
        "@type": "SearchAction",
        "target": "https://example.com/search?q={search_term_string}",
        "query-input": "required name=search_term_string"
      }
    },
    {
      "@type": "BreadcrumbList",
      "@id": "https://example.com/products#breadcrumb",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://example.com" },
        { "@type": "ListItem", "position": 2, "name": "Products", "item": "https://example.com/products" }
      ]
    },
    {
      "@type": "WebPage",
      "@id": "https://example.com/products#webpage",
      "name": "Products - Example",
      "description": "Browse our range of high-quality products.",
      "breadcrumb": { "@id": "https://example.com/products#breadcrumb" }
    }
  ]
}
```

## Implementation in Next.js

### Component Pattern for Dynamic Structured Data

```typescript
// components/structured-data/product-jsonld.tsx
interface ProductJsonLdProps {
  product: {
    name: string
    description: string
    image: string
    price: number
    currency: string
    inStock: boolean
    sku: string
    slug: string
  }
}

export function ProductJsonLd({ product }: ProductJsonLdProps) {
  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "Product",
    "@id": `https://example.com/products/${product.slug}#product`,
    name: product.name,
    description: product.description,
    image: product.image,
    sku: product.sku,
    offers: {
      "@type": "Offer",
      price: product.price.toFixed(2),
      priceCurrency: product.currency,
      availability: product.inStock
        ? "https://schema.org/InStock"
        : "https://schema.org/OutOfStock",
      url: `https://example.com/products/${product.slug}`,
    },
  }

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
    />
  )
}
```

### Page-Level Integration

```typescript
// app/products/[slug]/page.tsx
import { ProductJsonLd } from "@/components/structured-data/product-jsonld"
import { OrganizationJsonLd } from "@/components/structured-data/organization-jsonld"
import { BreadcrumbJsonLd } from "@/components/structured-data/breadcrumb-jsonld"

export default async function ProductPage({ params }: { params: { slug: string } }) {
  const product = await getProduct(params.slug)

  return (
    <>
      <OrganizationJsonLd />
      <BreadcrumbJsonLd
        items={[
          { name: "Home", url: "/" },
          { name: "Products", url: "/products" },
          { name: product.name, url: `/products/${product.slug}` },
        ]}
      />
      <ProductJsonLd product={product} />

      <article>
        {/* Page content */}
      </article>
    </>
  )
}
```

### Layout-Level Structured Data (Site-wide)

```typescript
// app/layout.tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  const organizationLd = {
    "@context": "https://schema.org",
    "@type": "Organization",
    name: "Example Inc.",
    url: "https://example.com",
    logo: "https://example.com/logo.png",
  }

  const websiteLd = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    name: "Example",
    url: "https://example.com",
    potentialAction: {
      "@type": "SearchAction",
      target: "https://example.com/search?q={search_term_string}",
      "query-input": "required name=search_term_string",
    },
  }

  return (
    <html lang="en">
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(organizationLd) }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(websiteLd) }}
        />
      </head>
      <body>{children}</body>
    </html>
  )
}
```

## Required vs Recommended Properties

| Rich Result | Required Properties | Recommended Properties |
|---|---|---|
| **Article** | `headline`, `image`, `datePublished` | `author`, `dateModified`, `description`, `publisher`, `mainEntityOfPage` |
| **BreadcrumbList** | `itemListElement[].position`, `itemListElement[].name`, `itemListElement[].item` | — |
| **Product** | `name`, `offers.price`, `offers.priceCurrency`, `offers.availability` | `description`, `image`, `brand`, `aggregateRating`, `review`, `sku`, `mpn` |
| **FAQPage** | `mainEntity[].name`, `mainEntity[].acceptedAnswer.text` | — |
| **LocalBusiness** | `name`, `address` | `telephone`, `geo`, `openingHours`, `image`, `url`, `priceRange`, `sameAs` |
| **Event** | `name`, `startDate`, `location` | `endDate`, `description`, `image`, `offers`, `performer`, `organizer`, `eventStatus` |
| **Review** | `itemReviewed`, `reviewRating`, `author` | `datePublished`, `reviewBody`, `publisher` |
| **Organization** | `name`, `url` or `logo` | `contactPoint`, `sameAs`, `description`, `address` |
| **WebSite** | `name`, `url` | `description`, `potentialAction` (for sitelinks search box) |

## Testing Tools

| Tool | URL | Purpose |
|---|---|---|
| Google Rich Results Test | `https://search.google.com/test/rich-results` | Test URL or code snippet for valid rich results |
| Schema Markup Validator | `https://validator.schema.org/` | Validate schema.org markup syntax |
| Google Search Console | Dashboard → Enhancements | Monitor live structured data issues on indexed pages |
| Bing Webmaster Tools | Dashboard → SEO → Structured Data | Monitor structured data in Bing index |

## Google-Specific Requirements

### Logo for Knowledge Panel

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Example Inc.",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png"
}
```

Requirements for Knowledge Panel eligibility:
- Logo must be 112×112px minimum
- Logo must be hosted on the same domain as the Organization URL
- URL and name must match the verified Google Search Console property

### Site Name in Search Results

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Example",
  "url": "https://example.com"
}
```

Google may use this to display the site name in search results instead of the domain.

## Common Pitfalls

- **Missing @id references**: Not linking entities together with `@id` when they reference each other
- **Wrong price format**: Prices must be strings, not numbers (to avoid floating point issues)
- **Mismatched availability values**: Use the Schema.org URL values, not plain text
- **Missing publisher in articles**: Required for Google News and Top Stories
- **Too many FAQ entries**: Google limits FAQ rich results to roughly 10 questions
- **FAQ content not visible**: Questions and answers must be directly visible on the page
- **Review without actual review content**: The review text must match what users see on the page
