---
name: react-router-use-loader-data
description: useLoaderData hook to access loader data in route components. Use when you need to read data loaded by route loaders.
---

# useLoaderData

The `useLoaderData` hook provides access to data returned from route loaders.

## Basic Usage

```tsx
import { useLoaderData } from "react-router";

function MyRoute() {
  const data = useLoaderData();
  return <div>{data.message}</div>;
}
```

## TypeScript

Add type inference for better type safety:

```tsx
import { useLoaderData } from "react-router";
import type { loader } from "./route";

function MyRoute() {
  const data = useLoaderData<typeof loader>();
  // data is typed based on loader return type
  return <div>{data.message}</div>;
}
```

## Destructuring

Destructure the returned data:

```tsx
function MyRoute() {
  const { records } = useLoaderData();
  return (
    <div>
      {records.map((record) => (
        <div key={record.id}>{record.name}</div>
      ))}
    </div>
  );
}
```

## With Route Loader

```tsx
// Route definition
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

// Component
function Project() {
  const { project } = useLoaderData();
  return <h1>{project.name}</h1>;
}
```

## Nested Routes

Each route level can access its own loader data:

```tsx
createBrowserRouter([
  {
    path: "/",
    loader: rootLoader,
    Component: Root,
    children: [
      {
        path: "team",
        loader: teamLoader,
        Component: Team,
      },
    ],
  },
]);

function Root() {
  const rootData = useLoaderData(); // From rootLoader
  return (
    <div>
      <h1>{rootData.title}</h1>
      <Outlet /> {/* Team component renders here */}
    </div>
  );
}

function Team() {
  const teamData = useLoaderData(); // From teamLoader
  return <div>{teamData.members.length} members</div>;
}
```

## Key Points

- **Only in route components** - Must be used in components rendered by routes
- **Type safety** - Use `useLoaderData<typeof loader>()` for TypeScript
- **Reactive** - Data updates automatically when loaders revalidate
- **Nested access** - Each route level accesses its own loader data

<!--
Source references:
- https://reactrouter.com/start/data/data-loading
-->
