---
name: nextjs-generate-static-params
description: Next.js generateStaticParams function for static generation. Use when pre-rendering dynamic routes at build time.
---

# generateStaticParams

The `generateStaticParams` function can be used in combination with [dynamic route segments](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes) to [**statically generate**](https://nextjs.org/docs/app/guides/caching#static-rendering) routes at build time instead of on-demand at request time.

`generateStaticParams` can be used with:
- [Pages](https://nextjs.org/docs/app/api-reference/file-conventions/page) (`page.tsx`/`page.js`)
- [Layouts](https://nextjs.org/docs/app/api-reference/file-conventions/layout) (`layout.tsx`/`layout.js`)
- [Route Handlers](https://nextjs.org/docs/app/api-reference/file-conventions/route) (`route.ts`/`route.js`)

## Basic Usage

```tsx
// Return a list of `params` to populate the [slug] dynamic segment
export async function generateStaticParams() {
  const posts = await fetch('https://.../posts').then((res) => res.json())
  return posts.map((post) => ({
    slug: post.slug,
  }))
}

// Multiple versions of this page will be statically generated
// using the `params` returned by `generateStaticParams`
export default async function Page({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
  // ...
}
```

## Parameters

### `options.params` (optional)

If multiple dynamic segments in a route use `generateStaticParams`, the child `generateStaticParams` function is executed once for each set of `params` the parent generates.

The `params` object contains the populated `params` from the parent `generateStaticParams`, which can be used to [generate the `params` in a child segment](#multiple-dynamic-segments-in-a-route).

## Returns

`generateStaticParams` should return an array of objects where each object represents the populated dynamic segments of a single route.

| Example Route | `generateStaticParams` Return Type |
|---------------|-----------------------------------|
| `/product/[id]` | `{ id: string }[]` |
| `/products/[category]/[product]` | `{ category: string, product: string }[]` |
| `/products/[...slug]` | `{ slug: string[] }[]` |

## Key Points

- **During `next build`** - `generateStaticParams` runs before the corresponding Layouts or Pages are generated
- **During `next dev`** - `generateStaticParams` will be called when you navigate to a route
- **Replaces `getStaticPaths`** - `generateStaticParams` replaces the [`getStaticPaths`](https://nextjs.org/docs/pages/api-reference/functions/get-static-paths) function in the Pages Router
- **Automatic memoization** - `fetch` requests inside `generateStaticParams` are automatically [memoized](https://nextjs.org/docs/app/guides/caching#request-memoization)

## Examples

### Single Dynamic Segment

```tsx
// app/product/[id]/page.tsx
export function generateStaticParams() {
  return [{ id: '1' }, { id: '2' }, { id: '3' }]
}

// Three versions of this page will be statically generated
// using the `params` returned by `generateStaticParams`
// - /product/1
// - /product/2
// - /product/3
export default async function Page({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params
  // ...
}
```

### Multiple Dynamic Segments

```tsx
// app/products/[category]/[product]/page.tsx
export function generateStaticParams() {
  return [
    { category: 'a', product: '1' },
    { category: 'b', product: '2' },
    { category: 'c', product: '3' },
  ]
}

// Three versions of this page will be statically generated
// using the `params` returned by `generateStaticParams`
// - /products/a/1
// - /products/b/2
// - /products/c/3
export default async function Page({
  params,
}: {
  params: Promise<{ category: string; product: string }>
}) {
  const { category, product } = await params
  // ...
}
```

### All paths at build time

```tsx
export async function generateStaticParams() {
  const posts = await fetch('https://.../posts').then((res) => res.json())
  return posts.map((post) => ({
    slug: post.slug,
  }))
}
```

### Subset of paths at build time

```tsx
export async function generateStaticParams() {
  const posts = await fetch('https://.../posts').then((res) => res.json())
  // Render the first 10 posts at build time
  return posts.slice(0, 10).map((post) => ({
    slug: post.slug,
  }))
}
```

### All paths at runtime

```tsx
// Return empty array (no paths will be rendered at build time)
export async function generateStaticParams() {
  return []
}
```

Or use:

```tsx
export const dynamic = 'force-static'
```

### Multiple Dynamic Segments in a Route

#### Generate params from the bottom up

Generate multiple dynamic segments from the child route segment.

```tsx
// app/products/[category]/[product]/page.tsx
// Generate segments for both [category] and [product]
export async function generateStaticParams() {
  const products = await fetch('https://.../products').then((res) =>
    res.json()
  )
  return products.map((product) => ({
    category: product.category.slug,
    product: product.id,
  }))
}
```

#### Generate params from the top down

Generate the parent segments first and use the result to generate the child segments.

```tsx
// app/products/[category]/layout.tsx
// Generate segments for [category]
export async function generateStaticParams() {
  const products = await fetch('https://.../products').then((res) =>
    res.json()
  )
  return products.map((product) => ({
    category: product.category.slug,
  }))
}
```

```tsx
// app/products/[category]/[product]/page.tsx
// Generate segments for [product] using the `params` passed from
// the parent segment's `generateStaticParams` function
export async function generateStaticParams({
  params: { category },
}: {
  params: { category: string }
}) {
  const products = await fetch(
    `https://.../products?category=${category}`
  ).then((res) => res.json())
  return products.map((product) => ({
    product: product.id,
  }))
}
```

### With Route Handlers

```tsx
// app/api/posts/[id]/route.ts
export async function generateStaticParams() {
  return [{ id: '1' }, { id: '2' }, { id: '3' }]
}

export async function GET(
  request: Request,
  { params }: RouteContext<'/api/posts/[id]'>
) {
  const { id } = await params
  // This will be statically generated for IDs 1, 2, and 3
  return Response.json({ id, title: `Post ${id}` })
}
```

<!--
Source references:
- https://nextjs.org/docs/app/api-reference/functions/generate-static-params
-->
