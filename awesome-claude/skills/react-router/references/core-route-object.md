---
name: react-router-route-object
description: Route object configuration for Data Mode. Use when defining routes with loaders, actions, components, and route properties.
---

# Route Object

Route objects are the foundation of React Router's Data Mode. They define data loading, actions, revalidation, error boundaries, and more.

## Basic Structure

```tsx
createBrowserRouter([
  {
    path: "/",
    Component: App,
  },
]);
```

## Component

The `Component` property defines the component that renders when the route matches:

```tsx
createBrowserRouter([
  {
    path: "/",
    Component: MyRouteComponent,
  },
]);

function MyRouteComponent() {
  return (
    <div>
      <h1>Look ma!</h1>
      <p>I'm still using React Router after like 10 years.</p>
    </div>
  );
}
```

## Path and Children

Define nested routes with the `children` property. Prefer a lightweight eager layout route with lazy-loaded child pages:

```tsx
createBrowserRouter([
  {
    path: "/",
    Component: RootLayout,
    children: [
      {
        path: "events/:id",
        lazy: {
          loader: async () => (await import("./routes/event.loader")).loader,
          Component: async () => (await import("./routes/event.page")).EventPage,
          ErrorBoundary: async () =>
            (await import("./routes/event.error")).EventErrorBoundary,
        },
      },
    ],
  },
]);
```

## Preferred Pattern

Keep route-matching fields static and route implementation lazy when the child route is substantial:

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
        path: "reports",
        lazy: {
          loader: async () => (await import("./routes/reports.loader")).loader,
          Component: async () => (await import("./routes/reports.page")).ReportsPage,
        },
      },
    ],
  },
]);
```

## Middleware

Route middleware runs sequentially before and after navigations:

```tsx
createBrowserRouter([
  {
    path: "/",
    middleware: [loggingMiddleware],
    loader: rootLoader,
    Component: RootLayout,
    children: [
      {
        path: "auth",
        middleware: [authMiddleware],
        lazy: {
          loader: async () => (await import("./routes/auth.loader")).authLoader,
          Component: async () => (await import("./routes/auth.page")).AuthPage,
        },
      },
    ],
  },
]);

async function loggingMiddleware({ request }, next) {
  const url = new URL(request.url);
  console.log(`Starting navigation: ${url.pathname}`);
  const start = performance.now();
  await next();
  const duration = performance.now() - start;
  console.log(`Navigation completed in ${duration}ms`);
}
```

## Route Properties

- **path** - URL path pattern (supports params like `:id` and splats like `*`)
- **Component** - Component to render when route matches
- **loader** - Function to load data before component renders
- **action** - Function to handle form submissions and mutations
- **middleware** - Array of middleware functions
- **shouldRevalidate** - Function to control when loader revalidates
- **lazy** - Object or function to lazily load non-matching route implementation
- **children** - Nested route objects
- **index** - Boolean indicating index route
- **errorElement** - Component to render on errors

## Key Points

- **Route objects are static** - Define routes outside React rendering
- **Keep matching keys static** - Define `path`, `index`, and `children` eagerly in the route tree
- **Lazy load heavy route implementation** - Prefer `route.lazy` for large child pages, loaders, and error boundaries
- **Nested routes** - Use `children` array for nested route structure
- **Path matching** - Routes match based on URL pathname
- **Route IDs** - Can specify `id` for route identification

<!--
Source references:
- https://reactrouter.com/start/data/route-object
-->
