---
name: react-router-loaders
description: Route loaders for data loading in Data Mode. Use when fetching data before route components render.
---

# Data Loading with Loaders

Route loaders provide data to route components before they are rendered. Loaders are called before route components render as users navigate between routes.

## Defining Loaders

Define a loader function on the route object:

```tsx
import { createBrowserRouter } from "react-router";

const router = createBrowserRouter([
  {
    path: "/",
    loader: async () => {
      // return data from here
      return {
        records: await getSomeRecords(),
      };
    },
    Component: MyRoute,
  },
]);
```

## Loader Function Signature

Loaders receive a `LoaderFunctionArgs` object:

```tsx
async function loader({ request, params, context }) {
  // request - Web Fetch Request object
  // params - Route params from URL
  // context - Custom context (if using dataStrategy)
  
  return {
    // Return any serializable data
  };
}
```

## Accessing Loader Data

Use `useLoaderData` hook in route components:

```tsx
import { useLoaderData } from "react-router";

function MyRoute() {
  const { records } = useLoaderData();
  return <div>{records.length}</div>;
}
```

## Loader Examples

### With URL Params

```tsx
createBrowserRouter([
  {
    path: "/projects/:projectId",
    loader: async ({ params }) => {
      const project = await getProject(params.projectId);
      return { project };
    },
    Component: Project,
  },
]);
```

### With Request Signal

Use `request.signal` for aborting requests:

```tsx
createBrowserRouter([
  {
    path: "/shows/:showId",
    loader: ({ request, params }) =>
      fetch(`/api/show/${params.showId}.json`, {
        signal: request.signal,
      }),
    Component: Show,
  },
]);
```

### Parallel Loading

React Router automatically runs loaders in parallel:

```tsx
createBrowserRouter([
  {
    path: "/",
    loader: rootLoader,
    Component: Root,
    children: [
      {
        path: "team",
        loader: teamLoader, // Runs in parallel with rootLoader
        Component: Team,
      },
    ],
  },
]);
```

## Return Values

Loaders can return:
- Plain objects/arrays
- `Response` objects (will be unwrapped)
- `redirect()` - Redirect to another route
- `defer()` - Stream data progressively

## Key Points

- **Loaders run before render** - Data is available when component renders
- **Parallel execution** - All matching route loaders run in parallel
- **Automatic revalidation** - Loaders revalidate after actions, navigation, etc.
- **Request signal** - Use `request.signal` for cancellation
- **Type safety** - Use TypeScript with `useLoaderData<typeof loader>()`

<!--
Source references:
- https://reactrouter.com/start/data/data-loading
- https://reactrouter.com/start/data/route-object#loader
-->
