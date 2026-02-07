---
name: react-router-fetchers
description: Using fetchers for complex data interactions without navigation. Use when building search, optimistic updates, or concurrent data operations.
---

# Using Fetchers

Fetchers are useful for creating complex, dynamic user interfaces that require multiple, concurrent data interactions without causing a navigation. They track their own independent state and can be used to load data, mutate data, submit forms, and interact with loaders and actions.

## Calling Actions with Fetchers

### Basic Pattern

```tsx
import { useFetcher, useLoaderData } from "react-router";

export default function Component() {
  const data = useLoaderData();
  const fetcher = useFetcher();
  
  return (
    <div>
      <h1>{data.title}</h1>
      <fetcher.Form method="post">
        <input type="text" name="title" />
        <button type="submit">Save</button>
      </fetcher.Form>
    </div>
  );
}
```

### With Pending State

```tsx
export default function Component() {
  const data = useLoaderData();
  const fetcher = useFetcher();
  
  return (
    <div>
      <h1>{data.title}</h1>
      <fetcher.Form method="post">
        <input type="text" name="title" />
        {fetcher.state !== "idle" && <p>Saving...</p>}
      </fetcher.Form>
    </div>
  );
}
```

### Optimistic UI

Use `fetcher.formData` for immediate feedback:

```tsx
export default function Component() {
  const data = useLoaderData();
  const fetcher = useFetcher();
  
  // Use formData if submitting, otherwise use loaded data
  const title = fetcher.formData?.get("title") || data.title;
  
  return (
    <div>
      <h1>{title}</h1>
      <fetcher.Form method="post">
        <input type="text" name="title" />
        {fetcher.state !== "idle" && <p>Saving...</p>}
      </fetcher.Form>
    </div>
  );
}
```

### Error Handling

```tsx
export default function Component() {
  const data = useLoaderData();
  const fetcher = useFetcher();
  const title = fetcher.formData?.get("title") || data.title;
  
  return (
    <div>
      <h1>{title}</h1>
      <fetcher.Form method="post">
        <input type="text" name="title" />
        {fetcher.state !== "idle" && <p>Saving...</p>}
        {fetcher.data?.error && (
          <p style={{ color: "red" }}>{fetcher.data.error}</p>
        )}
      </fetcher.Form>
    </div>
  );
}
```

## Loading Data with Fetchers

### Search Route

Create a route with a loader:

```tsx
// Route: /search-users
const users = [
  { id: 1, name: "Ryan" },
  { id: 2, name: "Michael" },
];

export async function loader({ request }) {
  await new Promise((res) => setTimeout(res, 300));
  const url = new URL(request.url);
  const query = url.searchParams.get("q");
  return users.filter((user) =>
    user.name.toLowerCase().includes(query.toLowerCase())
  );
}
```

### Combobox Component

```tsx
import { useFetcher } from "react-router";
import type { loader } from "./search-users";

export function UserSearchCombobox() {
  const fetcher = useFetcher<typeof loader>();
  
  return (
    <div>
      <fetcher.Form method="get" action="/search-users">
        <input
          type="text"
          name="q"
          onChange={(event) => {
            fetcher.submit(event.currentTarget.form);
          }}
        />
      </fetcher.Form>
      {fetcher.data && (
        <ul style={{ opacity: fetcher.state === "idle" ? 1 : 0.25 }}>
          {fetcher.data.map((user) => (
            <li key={user.id}>{user.name}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

## Key Patterns

### Multiple Concurrent Fetchers

```tsx
function Component() {
  const saveFetcher = useFetcher();
  const deleteFetcher = useFetcher();
  
  return (
    <div>
      <saveFetcher.Form method="post" action="/save">
        {/* save form */}
      </saveFetcher.Form>
      <deleteFetcher.Form method="post" action="/delete">
        {/* delete form */}
      </deleteFetcher.Form>
    </div>
  );
}
```

### Programmatic Submission

```tsx
function Component() {
  const fetcher = useFetcher();
  
  const handleSave = () => {
    fetcher.submit(
      { title: "New Title" },
      { action: "/update-task/123", method: "post" }
    );
  };
  
  return <button onClick={handleSave}>Save</button>;
}
```

## Key Points

- **No navigation** - Fetchers don't cause navigation or history entries
- **Independent state** - Each fetcher tracks its own state separately
- **Revalidation** - Actions still trigger loader revalidation
- **Optimistic UI** - Use `fetcher.formData` for immediate feedback
- **Concurrent operations** - Multiple fetchers can run simultaneously
- **Type safety** - Use `useFetcher<typeof loader>()` for TypeScript

<!--
Source references:
- https://reactrouter.com/how-to/fetchers
-->
