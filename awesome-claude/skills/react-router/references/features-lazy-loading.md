---
name: react-router-lazy-loading
description: Lazy loading routes to reduce initial bundle size. Use when you want to code-split route components, loaders, and actions.
---

# Lazy Loading Routes

Use `route.lazy` to code-split non-matching route implementation details such as `Component`, `loader`, `action`, and `ErrorBoundary`.

Prefer route-level code splitting in Data Mode apps built with `createBrowserRouter`.

## Recommended Pattern

```tsx
createBrowserRouter([
  {
    path: "/",
    Component: RootLayout,
    children: [
      {
        index: true,
        Component: HomePage,
      },
      {
        path: "projects/:projectId",
        lazy: {
          loader: async () =>
            (await import("./routes/project-detail.loader")).loader,
          action: async () =>
            (await import("./routes/project-detail.action")).action,
          Component: async () =>
            (await import("./routes/project-detail.page")).ProjectDetailPage,
          ErrorBoundary: async () =>
            (await import("./routes/project-detail.error")).ProjectDetailErrorBoundary,
        },
      },
    ],
  },
]);
```

## What Must Stay Static

Keep all route-matching fields in the static route tree:

- `path`
- `index`
- `children`
- `caseSensitive`

Do not attempt to lazy load route matching.

## What Should Be Lazy

Lazy load non-matching route implementation:

- `Component`
- `loader`
- `action`
- `ErrorBoundary`
- Other non-matching route behavior

## Why Prefer Object API

Prefer the object form of `route.lazy` in library/data mode because it makes route-level code splitting explicit in the route definition:

- Split component and data logic independently
- Keep route config readable and static
- Align with official `createBrowserRouter` examples
- Make heavy leaf routes load on demand

## Shared Chunk Pattern

When several child routes should ship in one chunk, point multiple lazy properties at the same imported file:

```tsx
createBrowserRouter([
  {
    path: "dashboard",
    children: [
      {
        index: true,
        lazy: {
          Component: async () =>
            (await import("./routes/dashboard.chunk")).DashboardIndex,
        },
      },
      {
        path: "messages",
        lazy: {
          loader: async () =>
            (await import("./routes/dashboard.chunk")).messagesLoader,
          Component: async () =>
            (await import("./routes/dashboard.chunk")).DashboardMessages,
        },
      },
    ],
  },
]);
```

## Keep Critical Routes Eager

Keep the first screen or tiny layout routes in the critical bundle when that improves first render. Lazy load heavier child pages, admin areas, dashboards, reports, and detail views.

## Key Points

- **Use Data Routers only** - `route.lazy` is for `createBrowserRouter` and other data routers
- **Split by route boundary** - make pages the main chunk boundary, not arbitrary component trees
- **Keep matching static** - route matching must be known before lazy resolution
- **Load implementation on demand** - fetch route code just before navigation/fetching
- **Prefer object API** - make route-level code splitting explicit and easy to maintain

<!--
Source references:
- https://reactrouter.com/start/data/route-object#lazy
- https://reactrouter.com/start/data/custom#3-lazy-loading
- https://reactrouter.com/changelog
-->
