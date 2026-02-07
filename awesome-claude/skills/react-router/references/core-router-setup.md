---
name: react-router-router-setup
description: Setup createBrowserRouter and RouterProvider for Data Mode. Use when initializing React Router with data loading capabilities.
---

# Router Setup

`createBrowserRouter` is the recommended router for all React Router web projects. It uses the DOM History API to update the URL and manage the history stack, and enables Data Mode APIs like loaders, actions, and fetchers.

## Basic Setup

Create the router outside of the React tree with a statically defined set of routes:

```tsx
import { createBrowserRouter, RouterProvider } from "react-router";
import { createRoot } from "react-dom/client";

const router = createBrowserRouter([
  {
    path: "/",
    Component: Root,
    loader: rootLoader,
    children: [
      {
        path: "team",
        Component: Team,
        loader: teamLoader,
      },
    ],
  },
]);

createRoot(document.getElementById("root")).render(
  <RouterProvider router={router} />
);
```

## Router Options

### basename

The basename of the app for situations where you can't deploy to the root of the domain:

```tsx
const router = createBrowserRouter(routes, {
  basename: "/app",
});
```

The trailing slash will be respected when linking to the root.

### future

Enable future flags to ease migration to v7:

```tsx
const router = createBrowserRouter(routes, {
  future: {
    v7_normalizeFormMethod: true,
  },
});
```

Available flags:
- `v7_fetcherPersist` - Delay active fetcher cleanup until they return to idle
- `v7_normalizeFormMethod` - Normalize `useNavigation().formMethod` to uppercase
- `v7_partialHydration` - Support partial hydration for SSR apps
- `v7_prependBasename` - Prepend router basename to navigate/fetch paths
- `v7_relativeSplatPath` - Fix relative path resolution in splat routes
- `v7_skipActionErrorRevalidation` - Don't revalidate by default if action returns 4xx/5xx

### hydrationData

When server-rendering, pass hydration data from your server-render:

```tsx
const router = createBrowserRouter(routes, {
  hydrationData: {
    loaderData: {
      // [routeId]: serverLoaderData
    },
    // may also include `errors` and/or `actionData`
  },
});
```

## Key Points

- **Create router outside React tree** - Router should be created statically, not inside component render
- **Use RouterProvider** - Wrap your app with `<RouterProvider router={router} />`
- **Static route definitions** - Define all routes upfront for optimal matching and data loading
- **DOM History API** - Uses browser's native history API for URL management

<!--
Source references:
- https://reactrouter.com/v6/routers/create-browser-router
- https://reactrouter.com/start/data/custom
-->
