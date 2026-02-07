---
name: react-router-use-fetcher
description: useFetcher hook for non-navigational data loading and mutations. Use when you need to load data or call actions without causing navigation.
---

# useFetcher

The `useFetcher` hook allows you to interact with loaders and actions without causing a navigation. Fetchers track their own independent state and are useful for complex, dynamic UIs.

## Basic Usage

```tsx
import { useFetcher } from "react-router";

function Component() {
  const fetcher = useFetcher();
  
  return (
    <fetcher.Form method="post" action="/update-task/123">
      <input type="text" name="title" />
      <button type="submit">Save</button>
    </fetcher.Form>
  );
}
```

## Fetcher State

Access fetcher state for pending UI:

```tsx
function Component() {
  const fetcher = useFetcher();
  const busy = fetcher.state !== "idle";
  
  return (
    <fetcher.Form method="post">
      <input type="text" name="title" />
      <button type="submit" disabled={busy}>
        {busy ? "Saving..." : "Save"}
      </button>
    </fetcher.Form>
  );
}
```

Fetcher states:
- `idle` - No active request
- `submitting` - Form submission in progress
- `loading` - Loader call in progress

## Fetcher Data

Access data returned from actions or loaders:

```tsx
function Component() {
  const fetcher = useFetcher();
  
  return (
    <div>
      {fetcher.data?.error && (
        <p style={{ color: "red" }}>{fetcher.data.error}</p>
      )}
      <fetcher.Form method="post">
        {/* form */}
      </fetcher.Form>
    </div>
  );
}
```

## Imperative Submission

Submit programmatically with `fetcher.submit`:

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

## Loading Data

Use fetchers to load data without navigation:

```tsx
function SearchCombobox() {
  const fetcher = useFetcher();
  
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
        <ul>
          {fetcher.data.map((user) => (
            <li key={user.id}>{user.name}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

## Optimistic UI

Use `fetcher.formData` for optimistic updates:

```tsx
function Component() {
  const fetcher = useFetcher();
  const data = useLoaderData();
  
  // Use formData if submitting, otherwise use loaded data
  const title = fetcher.formData?.get("title") || data.title;
  
  return (
    <div>
      <h1>{title}</h1>
      <fetcher.Form method="post">
        <input type="text" name="title" />
        <button type="submit">Save</button>
      </fetcher.Form>
    </div>
  );
}
```

## TypeScript

Add type inference:

```tsx
import { useFetcher } from "react-router";
import type { loader } from "./search-users";

function Component() {
  const fetcher = useFetcher<typeof loader>();
  // fetcher.data is typed based on loader return type
}
```

## Fetcher Properties

- `state` - Current state: "idle" | "submitting" | "loading"
- `data` - Data returned from loader/action
- `formData` - FormData from current submission
- `formMethod` - HTTP method: "get" | "post" | "put" | "patch" | "delete"
- `formAction` - Action URL
- `submit()` - Imperative submit method
- `load()` - Load data from a route

## Key Points

- **No navigation** - Fetchers don't cause navigation or history entries
- **Independent state** - Each fetcher tracks its own state
- **Revalidation** - Actions called via fetchers still revalidate route loaders
- **Optimistic UI** - Use `fetcher.formData` for immediate feedback
- **Type safety** - Use `useFetcher<typeof loader>()` for TypeScript

<!--
Source references:
- https://reactrouter.com/how-to/fetchers
- https://reactrouter.com/start/data/actions#calling-actions-with-a-fetcher
-->
