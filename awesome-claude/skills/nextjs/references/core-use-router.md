---
name: nextjs-use-router
description: Next.js useRouter hook for programmatic navigation. Use when navigating programmatically in Client Components.
---

# useRouter

The `useRouter` hook allows you to programmatically change routes inside [Client Components](https://nextjs.org/docs/app/getting-started/server-and-client-components).

> **Recommendation**: Use the [`<Link>` component](https://nextjs.org/docs/app/api-reference/components/link) for navigation unless you have a specific requirement for using `useRouter`.

## Basic Usage

```tsx
'use client'
import { useRouter } from 'next/navigation'

export default function Page() {
  const router = useRouter()
  return (
    <button type="button" onClick={() => router.push('/dashboard')}>
      Dashboard
    </button>
  )
}
```

## API

### `router.push(href: string, { scroll: boolean })`

Perform a client-side navigation to the provided route. Adds a new entry into the [browser's history stack](https://developer.mozilla.org/docs/Web/API/History_API).

```tsx
router.push('/dashboard')
router.push('/dashboard', { scroll: false })
```

### `router.replace(href: string, { scroll: boolean })`

Perform a client-side navigation to the provided route without adding a new entry into the browser's history stack.

```tsx
router.replace('/dashboard')
router.replace('/dashboard', { scroll: false })
```

### `router.refresh()`

Refresh the current route. Making a new request to the server, re-fetching data requests, and re-rendering Server Components. The client will merge the updated React Server Component payload without losing unaffected client-side React (e.g. `useState`) or browser state (e.g. scroll position).

```tsx
router.refresh()
```

### `router.prefetch(href: string, options?: { onInvalidate?: () => void })`

[Prefetch](https://nextjs.org/docs/app/getting-started/linking-and-navigating#prefetching) the provided route for faster client-side transitions. The optional `onInvalidate` callback is called when the [prefetched data becomes stale](https://nextjs.org/docs/app/guides/prefetching#extending-or-ejecting-link).

```tsx
router.prefetch('/dashboard')
router.prefetch('/dashboard', {
  onInvalidate: () => {
    console.log('Prefetched data is stale')
  },
})
```

### `router.back()`

Navigate back to the previous route in the browser's history stack.

```tsx
router.back()
```

### `router.forward()`

Navigate forwards to the next page in the browser's history stack.

```tsx
router.forward()
```

## Key Points

- **Must import from `next/navigation`** - The `useRouter` hook should be imported from `next/navigation` and not `next/router` when using the App Router
- **Client Components only** - `useRouter` can only be used in Client Components
- **Do not send untrusted URLs** - You must not send untrusted or unsanitized URLs to `router.push` or `router.replace`, as this can open your site to cross-site scripting (XSS) vulnerabilities
- **Automatic prefetching** - The `<Link>` component automatically prefetch routes as they become visible in the viewport

## Migrating from `next/router`

- The `useRouter` hook should be imported from `next/navigation` and not `next/router` when using the App Router
- The `pathname` string has been removed and is replaced by [`usePathname()`](https://nextjs.org/docs/app/api-reference/functions/use-pathname)
- The `query` object has been removed and is replaced by [`useSearchParams()`](https://nextjs.org/docs/app/api-reference/functions/use-search-params)
- `router.events` has been replaced. You can listen for page changes by composing other Client Component hooks like `usePathname` and `useSearchParams`

## Examples

### Disabling scroll to top

```tsx
'use client'
import { useRouter } from 'next/navigation'

export default function Page() {
  const router = useRouter()
  return (
    <button
      type="button"
      onClick={() => router.push('/dashboard', { scroll: false })}
    >
      Dashboard
    </button>
  )
}
```

### Router events

You can listen for page changes by composing other Client Component hooks like `usePathname` and `useSearchParams`:

```tsx
'use client'
import { useEffect } from 'react'
import { usePathname, useSearchParams } from 'next/navigation'

export function NavigationEvents() {
  const pathname = usePathname()
  const searchParams = useSearchParams()

  useEffect(() => {
    const url = `${pathname}?${searchParams}`
    console.log(url)
    // You can now use the current URL
    // ...
  }, [pathname, searchParams])

  return null
}
```

Which can be imported into a layout:

```tsx
import { Suspense } from 'react'
import { NavigationEvents } from './components/navigation-events'

export default function Layout({ children }) {
  return (
    <html lang="en">
      <body>
        {children}
        <Suspense fallback={null}>
          <NavigationEvents />
        </Suspense>
      </body>
    </html>
  )
}
```

<!--
Source references:
- https://nextjs.org/docs/app/api-reference/functions/use-router
-->
