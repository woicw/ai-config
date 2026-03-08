---
name: react-router
description: React Router Data Mode with browser router. Use when building React applications with createBrowserRouter, RouterProvider, route.lazy, and route-level code splitting for loaders, actions, and route components.
metadata:
  author: woic
  version: "2026.2.6"
  source: Generated from https://reactrouter.com
---

# React Router (Data Mode)

React Router Data Mode enables data loading, actions, pending states, and more by moving route configuration outside of React rendering. It uses `createBrowserRouter` and `RouterProvider` to provide a powerful data layer for React applications.

> The skill is based on React Router v7.13.0, generated at 2026-02-06. Focuses on Data Mode with browser router only.

## Core References

| Topic | Description | Reference |
| ----- | ----------- | --------- |
| Router Setup | createBrowserRouter, RouterProvider, basic configuration | [core-router-setup](references/core-router-setup.md) |
| Route Objects | Route configuration, Component, path, children | [core-route-object](references/core-route-object.md) |
| Navigation | Link, NavLink, Form, redirect, useNavigate | [core-navigation](references/core-navigation.md) |
| Data Loading | Loaders, useLoaderData, data fetching patterns | [core-loaders](references/core-loaders.md) |
| Data Mutations | Actions, useActionData, form submissions | [core-actions](references/core-actions.md) |

## Hooks

| Topic | Description | Reference |
| ----- | ----------- | --------- |
| useParams | Access dynamic route parameters from URL | [hooks-use-params](references/hooks-use-params.md) |
| useSearchParams | Read and update URL search parameters | [hooks-use-search-params](references/hooks-use-search-params.md) |
| useLocation | Access current location (pathname, search, state, key) | [hooks-use-location](references/hooks-use-location.md) |
| useLoaderData | Access loader data in route components | [hooks-use-loader-data](references/hooks-use-loader-data.md) |
| useActionData | Access action return data | [hooks-use-action-data](references/hooks-use-action-data.md) |
| useFetcher | Non-navigational data loading and mutations | [hooks-use-fetcher](references/hooks-use-fetcher.md) |
| useNavigation | Navigation state, pending UI | [hooks-use-navigation](references/hooks-use-navigation.md) |

## Features

| Topic | Description | Reference |
| ----- | ----------- | --------- |
| Fetchers | Loading data and calling actions without navigation | [features-fetchers](references/features-fetchers.md) |
| Lazy Loading | Route-level code splitting with `route.lazy` object API | [features-lazy-loading](references/features-lazy-loading.md) |
| Revalidation | Control when loader data refreshes | [features-revalidation](references/features-revalidation.md) |
| Data Strategy | Advanced control over loader/action execution | [features-data-strategy](references/features-data-strategy.md) |

## Preferred Route Definition Pattern

Prefer static route matching and lazy route implementation:

```tsx
const router = createBrowserRouter([
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

Keep route-matching fields static in the route tree:

- `path`
- `index`
- `children`
- `caseSensitive`

Lazy load non-matching implementation fields with `route.lazy`:

- `Component`
- `loader`
- `action`
- `ErrorBoundary`
- Other non-matching route behavior

## Key Recommendations

- **Use createBrowserRouter** - recommended router for all React Router web projects
- **Define routes statically** - create router outside React tree with static route definitions
- **Keep matching keys static** - never lazy load `path`, `index`, or `children`
- **Use loaders for data** - load data before components render
- **Use actions for mutations** - actions automatically revalidate loader data
- **Use fetchers for non-navigational interactions** - search, optimistic updates, etc.
- **Prefer route.lazy object API** - split `Component`, `loader`, `action`, and `ErrorBoundary` at the route level
- **Code split by route boundary** - keep common layouts eager, lazy load leaf or heavy child routes
- **Handle pending states** - use `useNavigation` and fetcher state for loading UI
