---
name: nextjs-loading
description: Next.js loading.js file convention for showing loading UI. Use when creating loading states with React Suspense.
---

# loading.js

The special file `loading.js` helps you create meaningful Loading UI with [React Suspense](https://react.dev/reference/react/Suspense). With this convention, you can show an [instant loading state](#instant-loading-states) from the server while the content of a route segment streams in.

## Basic Usage

```tsx
export default function Loading() {
  return <p>Loading...</p>
}
```

## Behavior

### Navigation

- **The Fallback UI is prefetched** - making navigation immediate unless prefetching hasn't completed
- **Navigation is interruptible** - meaning changing routes does not need to wait for the content of the route to fully load before navigating to another route
- **Shared layouts remain interactive** - while new route segments load

### Instant Loading States

An instant loading state is fallback UI that is shown immediately upon navigation. You can pre-render loading indicators such as skeletons and spinners, or a small but meaningful part of future screens such as a cover photo, title, etc.

```tsx
export default function Loading() {
  return <LoadingSkeleton />
}
```

In the same folder, `loading.js` will be nested inside `layout.js`. It will automatically wrap the `page.js` file and any children below in a `<Suspense>` boundary.

## SEO

- For bots that only scrape static HTML, and cannot execute JavaScript like a full browser, such as Twitterbot, Next.js resolves [`generateMetadata`](https://nextjs.org/docs/app/api-reference/functions/generate-metadata) before streaming UI, and metadata is placed in the `<head>` of the initial HTML
- Otherwise, [streaming metadata](https://nextjs.org/docs/app/api-reference/functions/generate-metadata#streaming-metadata) may be used. Next.js automatically detects user agents to choose between blocking and streaming behavior
- Since streaming is server-rendered, it does not impact SEO

## Status Codes

When streaming, a `200` status code will be returned to signal that the request was successful.

The server can still communicate errors or issues to the client within the streamed content itself, for example, when using [`redirect`](https://nextjs.org/docs/app/api-reference/functions/redirect) or [`notFound`](https://nextjs.org/docs/app/api-reference/functions/not-found). Because the response headers have already been sent to the client, the status code of the response cannot be updated.

## Platform Support

| Deployment Option | Supported |
|-------------------|-----------|
| Node.js server | Yes |
| Docker container | Yes |
| Static export | No |
| Adapters | Platform-specific |

## Examples

### Streaming with Suspense

In addition to `loading.js`, you can also manually create Suspense Boundaries for your own UI components:

```tsx
import { Suspense } from 'react'
import { PostFeed, Weather } from './Components'

export default function Posts() {
  return (
    <section>
      <Suspense fallback={<p>Loading feed...</p>}>
        <PostFeed />
      </Suspense>
      <Suspense fallback={<p>Loading weather...</p>}>
        <Weather />
      </Suspense>
    </section>
  )
}
```

By using Suspense, you get the benefits of:

1. **Streaming Server Rendering** - Progressively rendering HTML from the server to the client
2. **Selective Hydration** - React prioritizes what components to make interactive first based on user interaction

## Key Points

- **By default, this file is a Server Component** - but can also be used as a Client Component through the `"use client"` directive
- **Loading UI components do not accept any parameters**
- **Automatic wrapping** - `loading.js` automatically wraps `page.js` and children in a `<Suspense>` boundary
- **Browser limits** - [Some browsers](https://bugs.webkit.org/show_bug.cgi?id=252413) buffer a streaming response. You may not see the streamed response until the response exceeds 1024 bytes

<!--
Source references:
- https://nextjs.org/docs/app/api-reference/file-conventions/loading
-->
