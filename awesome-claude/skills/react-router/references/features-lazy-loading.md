---
name: react-router-lazy-loading
description: Lazy loading routes to reduce initial bundle size. Use when you want to code-split route components, loaders, and actions.
---

# Lazy Loading Routes

The `lazy` property allows you to lazily import route implementations (Component, loader, action, etc.) to reduce the initial bundle size.

## Basic Lazy Loading

```tsx
createBrowserRouter([
  {
    path: "/app",
    lazy: async () => {
      const [Component, loader] = await Promise.all([
        import("./app"),
        import("./app-loader"),
      ]);
      return { Component, loader };
    },
  },
]);
```

## Lazy Component Only

```tsx
createBrowserRouter([
  {
    path: "/show/:showId",
    loader: showLoader,
    lazy: async () => {
      const { Component } = await import("./show.component.js");
      return { Component };
    },
  },
]);
```

## Lazy Loader and Action

```tsx
createBrowserRouter([
  {
    path: "/show/:showId",
    lazy: async () => {
      const [loader, action, Component] = await Promise.all([
        import("./show.loader.js").then((m) => m.loader),
        import("./show.action.js").then((m) => m.action),
        import("./show.component.js").then((m) => m.Component),
      ]);
      return { loader, action, Component };
    },
  },
]);
```

## Route Module Pattern

If using route modules, lazy load the entire module:

```tsx
createBrowserRouter([
  {
    path: "/dashboard",
    lazy: async () => {
      const module = await import("./routes/dashboard");
      return {
        Component: module.default,
        loader: module.loader,
        action: module.action,
      };
    },
  },
]);
```

## Parallel Loading

Load multiple route properties in parallel:

```tsx
createBrowserRouter([
  {
    path: "/app",
    lazy: async () => {
      const [
        { default: Component },
        { loader },
        { action },
        { ErrorBoundary },
      ] = await Promise.all([
        import("./app.component"),
        import("./app.loader"),
        import("./app.action"),
        import("./app.error"),
      ]);
      
      return {
        Component,
        loader,
        action,
        ErrorBoundary,
      };
    },
  },
]);
```

## Nested Lazy Routes

Lazy load nested routes:

```tsx
createBrowserRouter([
  {
    path: "/",
    Component: Root,
    children: [
      {
        path: "dashboard",
        lazy: async () => {
          const { default: Component } = await import("./dashboard");
          return { Component };
        },
        children: [
          {
            path: "settings",
            lazy: async () => {
              const { default: Component } = await import("./settings");
              return { Component };
            },
          },
        ],
      },
    ],
  },
]);
```

## Key Points

- **Reduce bundle size** - Only load route code when needed
- **Parallel loading** - Use `Promise.all` to load multiple properties
- **Route definitions** - Path and other route metadata should be static
- **Type safety** - Lazy functions should return properly typed route properties
- **Error handling** - Lazy loading errors are handled by error boundaries

<!--
Source references:
- https://reactrouter.com/start/data/route-object#lazy
- https://reactrouter.com/start/data/custom#3-lazy-loading
-->
