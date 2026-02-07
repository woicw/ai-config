---
name: nextjs-route
description: Next.js route.js file convention for creating API route handlers. Use when building API endpoints or custom request handlers.
---

# route.js

Route Handlers allow you to create custom request handlers for a given route using the Web [Request](https://developer.mozilla.org/docs/Web/API/Request) and [Response](https://developer.mozilla.org/docs/Web/API/Response) APIs.

## Basic Usage

```tsx
export async function GET() {
  return Response.json({ message: 'Hello World' })
}
```

## HTTP Methods

A **route** file allows you to create custom request handlers for a given route. The following [HTTP methods](https://developer.mozilla.org/docs/Web/HTTP/Methods) are supported: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD`, and `OPTIONS`.

```tsx
export async function GET(request: Request) {}
export async function HEAD(request: Request) {}
export async function POST(request: Request) {}
export async function PUT(request: Request) {}
export async function DELETE(request: Request) {}
export async function PATCH(request: Request) {}
export async function OPTIONS(request: Request) {}
```

## Parameters

### `request` (optional)

The `request` object is a [NextRequest](https://nextjs.org/docs/app/api-reference/functions/next-request) object, which is an extension of the Web [Request](https://developer.mozilla.org/docs/Web/API/Request) API.

```tsx
import type { NextRequest } from 'next/server'

export async function GET(request: NextRequest) {
  const url = request.nextUrl
  return Response.json({ url: url.pathname })
}
```

### `context` (optional)

- **`params`**: a promise that resolves to an object containing the [dynamic route parameters](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes) for the current route.

```tsx
export async function GET(
  request: Request,
  { params }: { params: Promise<{ team: string }> }
) {
  const { team } = await params
  return Response.json({ team })
}
```

## TypeScript

You can type the Route Handler context using `RouteContext` to get strongly typed `params` from a route literal. `RouteContext` is a globally available helper.

```tsx
import type { NextRequest } from 'next/server'

export async function GET(
  _req: NextRequest,
  ctx: RouteContext<'/users/[id]'>
) {
  const { id } = await ctx.params
  return Response.json({ id })
}
```

## Common Operations

### Cookies

```tsx
import { cookies } from 'next/headers'

export async function GET(request: NextRequest) {
  const cookieStore = await cookies()
  const token = cookieStore.get('token')
  return Response.json({ token: token?.value })
}
```

### Headers

```tsx
import { headers } from 'next/headers'

export async function GET(request: NextRequest) {
  const headersList = await headers()
  const referer = headersList.get('referer')
  return Response.json({ referer })
}
```

### Request Body

```tsx
export async function POST(request: Request) {
  const res = await request.json()
  return Response.json({ res })
}
```

### FormData

```tsx
export async function POST(request: Request) {
  const formData = await request.formData()
  const name = formData.get('name')
  const email = formData.get('email')
  return Response.json({ name, email })
}
```

### URL Query Parameters

```tsx
import type { NextRequest } from 'next/server'

export function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams
  const query = searchParams.get('query')
  return Response.json({ query })
}
```

### Redirects

```tsx
import { redirect } from 'next/navigation'

export async function GET(request: Request) {
  redirect('https://nextjs.org/')
}
```

### CORS

```tsx
export async function GET(request: Request) {
  return new Response('Hello, Next.js!', {
    status: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  })
}
```

### Streaming

```tsx
export async function GET() {
  const encoder = new TextEncoder()
  
  async function* makeIterator() {
    yield encoder.encode('<p>One</p>')
    await sleep(200)
    yield encoder.encode('<p>Two</p>')
    await sleep(200)
    yield encoder.encode('<p>Three</p>')
  }
  
  const iterator = makeIterator()
  const stream = iteratorToStream(iterator)
  return new Response(stream)
}
```

## Dynamic Route Segments

Route Handlers can use [Dynamic Segments](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes) to create request handlers from dynamic data.

```tsx
export async function GET(
  request: Request,
  { params }: { params: Promise<{ slug: string }> }
) {
  const { slug } = await params
  return Response.json({ slug })
}
```

## Route Segment Config Options

Route Handlers use the same [route segment configuration](https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config) as pages and layouts.

```tsx
export const dynamic = 'auto'
export const dynamicParams = true
export const revalidate = false
export const fetchCache = 'auto'
export const runtime = 'nodejs'
export const preferredRegion = 'auto'
```

## Key Points

- **Default caching** - The default caching for `GET` handlers was changed from static to dynamic (Next.js 15+)
- **params is Promise** - In Next.js 15+, `context.params` is now a promise
- **Web API compatible** - Uses standard Web Request and Response APIs
- **Supports streaming** - Can return streaming responses, useful for AI-generated content

## Examples

### Webhooks

```tsx
export async function POST(request: Request) {
  try {
    const text = await request.text()
    // Process the webhook payload
  } catch (error) {
    return new Response(`Webhook error: ${error.message}`, {
      status: 400,
    })
  }
  return new Response('Success!', { status: 200 })
}
```

### Non-UI Responses

```tsx
export async function GET() {
  return new Response(
    `<?xml version="1.0" encoding="UTF-8" ?>
    <rss version="2.0">
      <channel>
        <title>Next.js Documentation</title>
        <link>https://nextjs.org/docs</link>
        <description>The React Framework for the Web</description>
      </channel>
    </rss>`,
    {
      headers: {
        'Content-Type': 'text/xml',
      },
    }
  )
}
```

<!--
Source references:
- https://nextjs.org/docs/app/api-reference/file-conventions/route
-->
