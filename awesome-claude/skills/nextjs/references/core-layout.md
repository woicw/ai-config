---
name: nextjs-layout
description: Next.js layout.js file convention for shared UI across routes. Use when creating layouts that wrap multiple pages.
---

# layout.js

The `layout` file is used to define a layout in your Next.js application.

```tsx
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return <section>{children}</section>
}
```

A **root layout** is the top-most layout in the root `app` directory. It is used to define the `<html>` and `<body>` tags and other globally shared UI.

```tsx
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
```

## Props

### `children` (required)

Layout components should accept and use a `children` prop. During rendering, `children` will be populated with the route segments the layout is wrapping.

### `params` (optional)

A promise that resolves to an object containing the [dynamic route parameters](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes) object from the root segment down to that layout.

```tsx
export default async function Layout({
  children,
  params,
}: {
  children: React.ReactNode
  params: Promise<{ team: string }>
}) {
  const { team } = await params
  return (
    <section>
      <header>Welcome to {team}'s Dashboard</header>
      <main>{children}</main>
    </section>
  )
}
```

## TypeScript

You can type layouts with `LayoutProps` to get a strongly typed `params` and named slots inferred from your directory structure. `LayoutProps` is a globally available helper.

```tsx
export default function Layout(props: LayoutProps<'/dashboard'>) {
  return <section>{props.children}</section>
}
```

## Caveats

### Request Object

Layouts are cached in the client during navigation to avoid unnecessary server requests. [Layouts](https://nextjs.org/docs/app/api-reference/file-conventions/layout) do not rerender. They can be cached and reused to avoid unnecessary computation when navigating between pages.

To access the request object, you can use [`headers`](https://nextjs.org/docs/app/api-reference/functions/headers) and [`cookies`](https://nextjs.org/docs/app/api-reference/functions/cookies) APIs in [Server Components](https://nextjs.org/docs/app/getting-started/server-and-client-components) and Functions.

```tsx
import { cookies } from 'next/headers'

export default async function Layout({ children }) {
  const cookieStore = await cookies()
  const theme = cookieStore.get('theme')
  return '...'
}
```

### Query params

Layouts do not rerender on navigation, so they cannot access search params which would otherwise become stale.

To access updated query parameters, you can use the Page [`searchParams`](https://nextjs.org/docs/app/api-reference/file-conventions/page#searchparams-optional) prop, or read them inside a Client Component using the [`useSearchParams`](https://nextjs.org/docs/app/api-reference/functions/use-search-params) hook.

### Pathname

Layouts do not re-render on navigation, so they do not access pathname which would otherwise become stale.

To access the current pathname, you can read it inside a Client Component using the [`usePathname`](https://nextjs.org/docs/app/api-reference/functions/use-pathname) hook.

### Fetching Data

Layouts cannot pass data to their `children`. However, you can fetch the same data in a route more than once, and use React [`cache`](https://react.dev/reference/react/cache) to dedupe the requests without affecting performance.

## Key Points

- **Layouts are shared** - Layouts are cached in the client during navigation and do not rerender
- **Must include children** - Layout components should accept and use a `children` prop
- **Root layout required** - The `app` directory **must** include a **root layout**
- **Multiple root layouts** - You can create **multiple root layouts** using route groups
- **Cross root layout navigation** - Navigating **across multiple root layouts** will cause a **full page load**

## Examples

### Metadata

```tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Next.js',
}

export default function Layout({ children }: { children: React.ReactNode }) {
  return '...'
}
```

### Active Nav Links

```tsx
'use client'
import { usePathname } from 'next/navigation'
import Link from 'next/link'

export function NavLinks() {
  const pathname = usePathname()
  return (
    <nav>
      <Link
        className={`link ${pathname === '/' ? 'active' : ''}`}
        href="/"
      >
        Home
      </Link>
      <Link
        className={`link ${pathname === '/about' ? 'active' : ''}`}
        href="/about"
      >
        About
      </Link>
    </nav>
  )
}
```

### Displaying content based on `params`

```tsx
export default async function DashboardLayout({
  children,
  params,
}: {
  children: React.ReactNode
  params: Promise<{ team: string }>
}) {
  const { team } = await params
  return (
    <section>
      <header>
        <h1>Welcome to {team}'s Dashboard</h1>
      </header>
      <main>{children}</main>
    </section>
  )
}
```

<!--
Source references:
- https://nextjs.org/docs/app/api-reference/file-conventions/layout
-->
