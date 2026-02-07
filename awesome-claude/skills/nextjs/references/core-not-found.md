---
name: nextjs-not-found
description: Next.js not-found.js file convention for 404 pages. Use when handling not found cases in routes.
---

# not-found.js

Next.js provides two conventions to handle not found cases:

- **`not-found.js`**: Used when you call the [`notFound`](https://nextjs.org/docs/app/api-reference/functions/not-found) function in a route segment
- **`global-not-found.js`**: Used to define a global 404 page for unmatched routes across your entire app (experimental)

## `not-found.js`

The **not-found** file is used to render UI when the [`notFound`](https://nextjs.org/docs/app/api-reference/functions/not-found) function is thrown within a route segment. Along with serving a custom UI, Next.js will return a `200` HTTP status code for streamed responses, and `404` for non-streamed responses.

```tsx
import Link from 'next/link'

export default function NotFound() {
  return (
    <div>
      <h2>Not Found</h2>
      <p>Could not find requested resource</p>
      <Link href="/">Return Home</Link>
    </div>
  )
}
```

## `global-not-found.js` (experimental)

The `global-not-found.js` file lets you define a 404 page for your entire application. Unlike `not-found.js`, which works at the route level, this is used when a requested URL doesn't match any route at all. Next.js **skips rendering** and directly returns this global page.

To enable it, add the `globalNotFound` flag in `next.config.ts`:

```tsx
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  experimental: {
    globalNotFound: true,
  },
}

export default nextConfig
```

Then, create a file in the root of the `app` directory: `app/global-not-found.js`:

```tsx
// Import global styles and fonts
import './globals.css'
import { Inter } from 'next/font/google'
import type { Metadata } from 'next'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: '404 - Page Not Found',
  description: 'The page you are looking for does not exist.',
}

export default function GlobalNotFound() {
  return (
    <html lang="en" className={inter.className}>
      <body>
        <h1>404 - Page Not Found</h1>
        <p>This page does not exist.</p>
      </body>
    </html>
  )
}
```

Unlike `not-found.js`, this file must return a full HTML document, including `<html>` and `<body>` tags.

## Props

`not-found.js` or `global-not-found.js` components do not accept any props.

## Key Points

- **Root not-found.js** - The root `app/not-found.js` and `app/global-not-found.js` files handle any unmatched URLs for your whole application
- **By default, `not-found` is a Server Component** - You can mark it as `async` to fetch and display data
- **Metadata support** - For `global-not-found.js`, you can export a `metadata` object or a [`generateMetadata`](https://nextjs.org/docs/app/api-reference/functions/generate-metadata) function

## Examples

### Data Fetching

```tsx
import Link from 'next/link'
import { headers } from 'next/headers'

export default async function NotFound() {
  const headersList = await headers()
  const domain = headersList.get('host')
  const data = await getSiteData(domain)

  return (
    <div>
      <h2>Not Found: {data.name}</h2>
      <p>Could not find requested resource</p>
      <p>
        View <Link href="/blog">all posts</Link>
      </p>
    </div>
  )
}
```

### Metadata

```tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Not Found',
  description: 'The page you are looking for does not exist.',
}

export default function GlobalNotFound() {
  return (
    <html lang="en">
      <body>
        <div>
          <h1>Not Found</h1>
          <p>The page you are looking for does not exist.</p>
        </div>
      </body>
    </html>
  )
}
```

<!--
Source references:
- https://nextjs.org/docs/app/api-reference/file-conventions/not-found
-->
