---
name: nextjs-page
description: Next.js page.js file convention for defining route UI. Use when creating pages in the App Router.
---

# page.js

The `page` file allows you to define UI that is **unique** to a route. You can create a page by default exporting a component from the file.

## Basic Usage

```tsx
export default function Page({
  params,
  searchParams,
}: {
  params: Promise<{ slug: string }>
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>
}) {
  return <h1>My Page</h1>
}
```

## Props

### `params` (optional)

A promise that resolves to an object containing the [dynamic route parameters](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes) from the root segment down to that page.

```tsx
export default async function Page({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
  return <h1>Blog Post: {slug}</h1>
}
```

- Since the `params` prop is a promise, you must use `async/await` or React's [`use`](https://react.dev/reference/react/use) function to access the values
- In version 14 and earlier, `params` was a synchronous prop. To help with backwards compatibility, you can still access it synchronously in Next.js 15, but this behavior will be deprecated in the future

### `searchParams` (optional)

A promise that resolves to an object containing the [search parameters](https://developer.mozilla.org/docs/Learn/Common_questions/What_is_a_URL#parameters) of the current URL.

```tsx
export default async function Page({
  searchParams,
}: {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>
}) {
  const { filters } = await searchParams
  return <div>Filters: {filters}</div>
}
```

- `searchParams` is a **[Dynamic API](https://nextjs.org/docs/app/guides/caching#dynamic-rendering)** whose values cannot be known ahead of time. Using it will opt the page into **[dynamic rendering](https://nextjs.org/docs/app/guides/caching#dynamic-rendering)** at request time
- Client Component **pages** can also access `searchParams` using React's [`use`](https://react.dev/reference/react/use) hook

## TypeScript

You can type pages with `PageProps` to get strongly typed `params` and `searchParams` from the route literal. `PageProps` is a globally available helper.

```tsx
export default async function Page(props: PageProps<'/blog/[slug]'>) {
  const { slug } = await props.params
  const query = await props.searchParams
  return <h1>Blog Post: {slug}</h1>
}
```

## Key Points

- **A page is always the leaf** - A page is always the **leaf** of the route subtree
- **A page file is required** - A `page` file is required to make a route segment **publicly accessible**
- **Pages are Server Components by default** - Pages are [Server Components](https://react.dev/reference/rsc/server-components) by default, but can be set to a [Client Component](https://react.dev/reference/rsc/use-client)
- **File extensions** - The `.js`, `.jsx`, or `.tsx` file extensions can be used for `page`

## Examples

### Displaying content based on `params`

```tsx
export default async function Page({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
  return <h1>Blog Post: {slug}</h1>
}
```

### Handling filtering with `searchParams`

```tsx
export default async function Page({
  searchParams,
}: {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>
}) {
  const { page = '1', sort = 'asc', query = '' } = await searchParams
  return (
    <div>
      <h1>Product Listing</h1>
      <p>Search query: {query}</p>
      <p>Current page: {page}</p>
      <p>Sort order: {sort}</p>
    </div>
  )
}
```

### Reading `searchParams` and `params` in Client Components

To use `searchParams` and `params` in a Client Component (which cannot be `async`), you can use React's [`use`](https://react.dev/reference/react/use) function to read the promise:

```tsx
'use client'
import { use } from 'react'

export default function Page({
  params,
  searchParams,
}: {
  params: Promise<{ slug: string }>
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>
}) {
  const { slug } = use(params)
  const { query } = use(searchParams)
  return <div>{slug} - {query}</div>
}
```

<!--
Source references:
- https://nextjs.org/docs/app/api-reference/file-conventions/page
-->
