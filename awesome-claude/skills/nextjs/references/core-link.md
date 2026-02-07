---
name: nextjs-link
description: Next.js Link component for client-side navigation. Use when navigating between routes in the App Router.
---

# Link Component

`<Link>` is a React component that extends the HTML `<a>` element to provide [prefetching](https://nextjs.org/docs/app/getting-started/linking-and-navigating#prefetching) and client-side navigation between routes. It is the primary way to navigate between routes in Next.js.

## Basic Usage

```tsx
import Link from 'next/link'

export default function Page() {
  return <Link href="/dashboard">Dashboard</Link>
}
```

## Props

### `href` (required)

The path or URL to navigate to.

```tsx
// Navigate to /about?name=test
export default function Page() {
  return (
    <Link
      href={{
        pathname: '/about',
        query: { name: 'test' },
      }}
    >
      About
    </Link>
  )
}
```

### `replace`

**Defaults to `false`.** When `true`, `next/link` will replace the current history state instead of adding a new URL into the [browser's history](https://developer.mozilla.org/docs/Web/API/History_API) stack.

```tsx
<Link href="/dashboard" replace>
  Dashboard
</Link>
```

### `scroll`

**Defaults to `true`.** The default scrolling behavior of `<Link>` in Next.js **is to maintain scroll position**, similar to how browsers handle back and forwards navigation.

When `scroll = {false}`, Next.js will not attempt to scroll to the first Page element.

```tsx
<Link href="/dashboard" scroll={false}>
  Dashboard
</Link>
```

### `prefetch`

Prefetching happens when a `<Link />` component enters the user's viewport (initially or through scroll). Next.js prefetches and loads the linked route (denoted by the `href`) and its data in the background to improve the performance of client-side navigations.

- **`"auto"` or `null` (default)**: Prefetch behavior depends on whether the route is static or dynamic
- **`true`**: The full route will be prefetched for both static and dynamic routes
- **`false`**: Prefetching will never happen

```tsx
<Link href="/dashboard" prefetch={false}>
  Dashboard
</Link>
```

### `onNavigate`

An event handler called during client-side navigation. The handler receives an event object that includes a `preventDefault()` method, allowing you to cancel the navigation if needed.

```tsx
<Link
  href="/dashboard"
  onNavigate={(e) => {
    // Only executes during SPA navigation
    console.log('Navigating...')
    // Optionally prevent navigation
    // e.preventDefault()
  }}
>
  Dashboard
</Link>
```

## Key Points

- **Automatic prefetching** - The `<Link>` component automatically prefetches routes as they become visible in the viewport
- **Client-side navigation** - Using `<Link>` for navigation does not cause a full page reload
- **Supports all `<a>` attributes** - You can add attributes like `className`, `target="_blank"` to `<Link>`, and they will be passed to the underlying `<a>` element
- **Dynamic routes** - When linking to dynamic segments, you can use template literals and interpolation to generate a list of links

## Examples

### Linking to dynamic route segments

```tsx
import Link from 'next/link'

interface Post {
  id: number
  title: string
  slug: string
}

export default function PostList({ posts }: { posts: Post[] }) {
  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>
          <Link href={`/blog/${post.slug}`}>{post.title}</Link>
        </li>
      ))}
    </ul>
  )
}
```

### Checking active links

```tsx
'use client'
import { usePathname } from 'next/navigation'
import Link from 'next/link'

export function Links() {
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

### Scrolling to an `id`

```tsx
<Link href="/dashboard#settings">Settings</Link>
// Output
<a href="/dashboard#settings">Settings</a>
```

### Blocking navigation

```tsx
'use client'
import Link from 'next/link'
import { useNavigationBlocker } from '../contexts/navigation-blocker'

export function CustomLink({ children, ...props }) {
  const { isBlocked } = useNavigationBlocker()
  return (
    <Link
      onNavigate={(e) => {
        if (isBlocked && !window.confirm('You have unsaved changes. Leave anyway?')) {
          e.preventDefault()
        }
      }}
      {...props}
    >
      {children}
    </Link>
  )
}
```

<!--
Source references:
- https://nextjs.org/docs/app/api-reference/components/link
-->
