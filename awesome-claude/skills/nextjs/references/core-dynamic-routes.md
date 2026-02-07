---
name: nextjs-dynamic-routes
description: Next.js dynamic route segments for creating routes from dynamic data. Use when routes depend on runtime or build-time data.
---

# Dynamic Route Segments

When you don't know the exact route segment names ahead of time and want to create routes from dynamic data, you can use Dynamic Segments that are filled in at request time or prerendered at build time.

## Convention

A Dynamic Segment can be created by wrapping a folder's name in square brackets: `[folderName]`.

```tsx
// app/blog/[slug]/page.tsx
export default async function Page({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
  return <div>My Post: {slug}</div>
}
```

Dynamic Segments are passed as the `params` prop to [`layout`](https://nextjs.org/docs/app/api-reference/file-conventions/layout), [`page`](https://nextjs.org/docs/app/api-reference/file-conventions/page), [`route`](https://nextjs.org/docs/app/api-reference/file-conventions/route), and [`generateMetadata`](https://nextjs.org/docs/app/api-reference/functions/generate-metadata) functions.

| Route | Example URL | `params` |
|-------|-------------|----------|
| `app/blog/[slug]/page.js` | `/blog/a` | `{ slug: 'a' }` |
| `app/blog/[slug]/page.js` | `/blog/b` | `{ slug: 'b' }` |
| `app/shop/[tag]/[item]/page.js` | `/shop/1/2` | `{ tag: '1', item: '2' }` |

## Catch-all Segments

Dynamic Segments can be extended to **catch-all** subsequent segments by adding an ellipsis inside the brackets `[...folderName]`.

```tsx
// app/shop/[...slug]/page.js
export default async function Page({
  params,
}: {
  params: Promise<{ slug: string[] }>
}) {
  const { slug } = await params
  return <div>Shop: {slug.join('/')}</div>
}
```

| Route | Example URL | `params` |
|-------|-------------|----------|
| `app/shop/[...slug]/page.js` | `/shop/a` | `{ slug: ['a'] }` |
| `app/shop/[...slug]/page.js` | `/shop/a/b` | `{ slug: ['a', 'b'] }` |
| `app/shop/[...slug]/page.js` | `/shop/a/b/c` | `{ slug: ['a', 'b', 'c'] }` |

## Optional Catch-all Segments

Catch-all Segments can be made **optional** by including the parameter in double square brackets: `[[...folderName]]`.

```tsx
// app/shop/[[...slug]]/page.js
export default async function Page({
  params,
}: {
  params: Promise<{ slug?: string[] }>
}) {
  const { slug } = await params
  return <div>Shop: {slug?.join('/') || 'home'}</div>
}
```

| Route | Example URL | `params` |
|-------|-------------|----------|
| `app/shop/[[...slug]]/page.js` | `/shop` | `{ slug: undefined }` |
| `app/shop/[[...slug]]/page.js` | `/shop/a` | `{ slug: ['a'] }` |
| `app/shop/[[...slug]]/page.js` | `/shop/a/b` | `{ slug: ['a', 'b'] }` |

## TypeScript

When using TypeScript, you can add types for `params` depending on your configured route segment — use [`PageProps<'/route'>`](https://nextjs.org/docs/app/api-reference/file-conventions/page#page-props-helper), [`LayoutProps<'/route'>`](https://nextjs.org/docs/app/api-reference/file-conventions/layout#layout-props-helper), or [`RouteContext<'/route'>`](https://nextjs.org/docs/app/api-reference/file-conventions/route#route-context-helper) to type `params` in `page`, `layout`, and `route` respectively.

```tsx
export default async function Page(props: PageProps<'/blog/[slug]'>) {
  const { slug } = await props.params
  return <div>{slug}</div>
}
```

## Behavior

- Since the `params` prop is a promise, you must use `async/await` or React's `use` function to access the values
- In version 14 and earlier, `params` was a synchronous prop. To help with backwards compatibility, you can still access it synchronously in Next.js 15, but this behavior will be deprecated in the future

## With generateStaticParams

### Without `generateStaticParams`

All params are runtime data. Param access must be wrapped by Suspense fallback UI.

```tsx
import { Suspense } from 'react'

export default function Page({ params }: PageProps<'/blog/[slug]'>) {
  return (
    <div>
      <h1>Blog Post</h1>
      <Suspense fallback={<div>Loading...</div>}>
        {params.then(({ slug }) => (
          <Content slug={slug} />
        ))}
      </Suspense>
    </div>
  )
}
```

### With `generateStaticParams`

Provide params ahead of time to prerender pages at build time.

```tsx
export async function generateStaticParams() {
  return [{ slug: '1' }, { slug: '2' }, { slug: '3' }]
}

export default async function Page({ params }: PageProps<'/blog/[slug]'>) {
  const { slug } = await params
  return (
    <div>
      <h1>Blog Post</h1>
      <Content slug={slug} />
    </div>
  )
}
```

## Key Points

- **Dynamic data** - Dynamic segments allow creating routes from runtime or build-time data
- **Type safety** - Use TypeScript helper types to get strongly typed params
- **Static generation** - Combine with `generateStaticParams` to prerender routes at build time
- **Runtime rendering** - Without `generateStaticParams`, routes render at request time

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
  return <div>Product {id}</div>
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

export default async function Page({
  params,
}: {
  params: Promise<{ category: string; product: string }>
}) {
  const { category, product } = await params
  return <div>Category: {category}, Product: {product}</div>
}
```

<!--
Source references:
- https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes
-->
