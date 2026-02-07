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

Define nested routes with the `children` property:

```tsx
createBrowserRouter([
  {
    path: "/",
    Component: Root,
    children: [
      {
        path: "events/:id",
        Component: Event,
        loader: eventLoader,
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
    Component: Root,
    children: [
      {
        path: "auth",
        middleware: [authMiddleware],
        loader: authLoader,
        Component: Auth,
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
- **lazy** - Function to lazily load route implementation
- **children** - Nested route objects
- **index** - Boolean indicating index route
- **errorElement** - Component to render on errors

## Key Points

- **Route objects are static** - Define routes outside React rendering
- **Nested routes** - Use `children` array for nested route structure
- **Path matching** - Routes match based on URL pathname
- **Route IDs** - Can specify `id` for route identification

<!--
Source references:
- https://reactrouter.com/start/data/route-object
-->
