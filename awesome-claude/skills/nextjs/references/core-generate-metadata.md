---
name: nextjs-generate-metadata
description: Next.js generateMetadata function for dynamic metadata. Use when metadata depends on dynamic information like route params or external data.
---

# generateMetadata

You can use the `metadata` object or the `generateMetadata` function to define metadata.

## The `metadata` object

To define static metadata, export a [`Metadata` object](#metadata-fields) from a `layout.js` or `page.js` file.

```tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Next.js',
  description: 'The React Framework for the Web',
}

export default function Page() {}
```

## `generateMetadata` function

Dynamic metadata depends on **dynamic information**, such as the current route parameters, external data, or `metadata` in parent segments, can be set by exporting a `generateMetadata` function that returns a [`Metadata` object](#metadata-fields).

```tsx
import type { Metadata, ResolvingMetadata } from 'next'

type Props = {
  params: Promise<{ id: string }>
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>
}

export async function generateMetadata(
  { params, searchParams }: Props,
  parent: ResolvingMetadata
): Promise<Metadata> {
  // read route params
  const { id } = await params

  // fetch data
  const product = await fetch(`https://.../${id}`).then((res) => res.json())

  // optionally access and extend (rather than replace) parent metadata
  const previousImages = (await parent).openGraph?.images || []

  return {
    title: product.title,
    openGraph: {
      images: ['/some-specific-page-image.jpg', ...previousImages],
    },
  }
}

export default function Page({ params, searchParams }: Props) {}
```

## Parameters

### `props`

An object containing the parameters of the current route:

- `params` - An object containing the [dynamic route parameters](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes) object from the root segment down to the segment `generateMetadata` is called from
- `searchParams` - An object containing the current URL's [search params](https://developer.mozilla.org/docs/Learn/Common_questions/What_is_a_URL#parameters) (only available in `page.js` segments)

### `parent`

A promise of the resolved metadata from parent route segments.

## Returns

`generateMetadata` should return a [`Metadata` object](#metadata-fields) containing one or more metadata fields.

## Key Points

- **Only supported in Server Components** - The `metadata` object and `generateMetadata` function exports are **only supported in Server Components**
- **Cannot export both** - You cannot export both the `metadata` object and `generateMetadata` function from the same route segment
- **Automatic memoization** - `fetch` requests inside `generateMetadata` are automatically [memoized](https://nextjs.org/docs/app/guides/caching#request-memoization)
- **Streaming metadata** - Metadata can be streamed from `generateMetadata` (Next.js 15.2+)

## Common Fields

### `title`

```tsx
export const metadata: Metadata = {
  title: 'Next.js',
  // or use template
  title: {
    template: '%s | Acme',
    default: 'Acme',
  },
}
```

### `description`

```tsx
export const metadata: Metadata = {
  description: 'The React Framework for the Web',
}
```

### `openGraph`

```tsx
export const metadata: Metadata = {
  openGraph: {
    title: 'Next.js',
    description: 'The React Framework for the Web',
    url: 'https://nextjs.org',
    siteName: 'Next.js',
    images: [
      {
        url: 'https://nextjs.org/og.png',
        width: 800,
        height: 600,
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
}
```

### `robots`

```tsx
export const metadata: Metadata = {
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
}
```

### `metadataBase`

A convenience option to set a base URL prefix for `metadata` fields that require a fully qualified URL.

```tsx
export const metadata: Metadata = {
  metadataBase: new URL('https://acme.com'),
  openGraph: {
    images: '/og-image.png', // resolves to https://acme.com/og-image.png
  },
}
```

## Examples

### Dynamic metadata based on route params

```tsx
export async function generateMetadata({
  params,
}: {
  params: Promise<{ id: string }>
}): Promise<Metadata> {
  const { id } = await params
  const product = await fetch(`https://api.example.com/products/${id}`).then(
    (res) => res.json()
  )

  return {
    title: product.title,
    description: product.description,
  }
}
```

### Inheriting parent metadata

```tsx
export async function generateMetadata(
  { params }: { params: Promise<{ id: string }> },
  parent: ResolvingMetadata
): Promise<Metadata> {
  const { id } = await params
  const product = await fetch(`https://api.example.com/products/${id}`).then(
    (res) => res.json()
  )

  const previousImages = (await parent).openGraph?.images || []

  return {
    title: product.title,
    openGraph: {
      images: [`/products/${id}/og.png`, ...previousImages],
    },
  }
}
```

<!--
Source references:
- https://nextjs.org/docs/app/api-reference/functions/generate-metadata
-->
