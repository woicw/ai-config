---
name: nextjs
description: Next.js App Router for building full-stack React applications. Use when building web applications with server components, routing, data fetching, and API routes.
metadata:
  author: woic
  version: "2026.2.7"
  source: Generated from https://nextjs.org/docs
---

# Next.js (App Router)

Next.js is a React framework for building full-stack web applications. You use React Components to build user interfaces, and Next.js provides additional features and optimizations.

> The skill is based on Next.js v16.1.6, generated at 2026-02-07. Focuses on App Router only.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Page | Define unique UI for a route | [core-page](references/core-page.md) |
| Layout | Shared UI across routes | [core-layout](references/core-layout.md) |
| Route Handler | Create API endpoints and custom request handlers | [core-route](references/core-route.md) |
| Loading | Show loading UI with React Suspense | [core-loading](references/core-loading.md) |
| Error | Handle runtime errors with error boundaries | [core-error](references/core-error.md) |
| Not Found | Handle 404 cases | [core-not-found](references/core-not-found.md) |

## Components

| Topic | Description | Reference |
|-------|-------------|-----------|
| Link | Client-side navigation between routes | [core-link](references/core-link.md) |
| Image | Optimized image component | [core-image](references/core-image.md) |

## Functions & Hooks

| Topic | Description | Reference |
|-------|-------------|-----------|
| useRouter | Programmatic navigation in Client Components | [core-use-router](references/core-use-router.md) |

## Routing

| Topic | Description | Reference |
|-------|-------------|-----------|
| Dynamic Routes | Create routes from dynamic data | [core-dynamic-routes](references/core-dynamic-routes.md) |
| generateStaticParams | Pre-render dynamic routes at build time | [core-generate-static-params](references/core-generate-static-params.md) |
| generateMetadata | Dynamic metadata generation | [core-generate-metadata](references/core-generate-metadata.md) |

## Key Recommendations

- **Use App Router** - App Router is the recommended router for new Next.js projects
- **Server Components by default** - Pages and layouts are Server Components by default
- **File-based routing** - Use file system conventions for routing
- **Use Link for navigation** - Prefer `<Link>` component over `useRouter` for navigation
- **Optimize images** - Use `next/image` for automatic image optimization
- **Static generation** - Use `generateStaticParams` to pre-render dynamic routes at build time
- **Metadata API** - Use `metadata` object or `generateMetadata` function for SEO
