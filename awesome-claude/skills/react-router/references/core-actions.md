---
name: react-router-actions
description: Route actions for data mutations in Data Mode. Use when handling form submissions and data mutations.
---

# Data Mutations with Actions

Route actions handle data mutations. When an action completes, all loader data on the page is automatically revalidated to keep your UI in sync.

## Defining Actions

Define an action function on the route object:

```tsx
import { createBrowserRouter } from "react-router";
import { someApi } from "./api";

const router = createBrowserRouter([
  {
    path: "/projects/:projectId",
    Component: Project,
    action: async ({ request }) => {
      const formData = await request.formData();
      const title = formData.get("title");
      const project = await someApi.updateProject({ title });
      return project;
    },
  },
]);
```

## Action Function Signature

Actions receive a `ActionFunctionArgs` object:

```tsx
async function action({ request, params, context }) {
  // request - Web Fetch Request object with formData
  // params - Route params from URL
  // context - Custom context (if using dataStrategy)
  
  return {
    // Return any serializable data
  };
}
```

## Calling Actions

### With Form Component

Use `<Form>` component for declarative submissions:

```tsx
import { Form } from "react-router";

function SomeComponent() {
  return (
    <Form action="/projects/123" method="post">
      <input type="text" name="title" />
      <button type="submit">Submit</button>
    </Form>
  );
}
```

This causes a navigation and adds a new entry to browser history.

### With useSubmit Hook

Submit imperatively with `useSubmit`:

```tsx
import { useSubmit } from "react-router";

function useQuizTimer() {
  const submit = useSubmit();
  
  const cb = useCallback(() => {
    submit(
      { quizTimedOut: true },
      { action: "/end-quiz", method: "post" }
    );
  }, []);
  
  useFakeTimer(10 * 60 * 1000, cb);
}
```

### With Fetcher

Use `useFetcher` for non-navigational submissions:

```tsx
import { useFetcher } from "react-router";

function Task() {
  const fetcher = useFetcher();
  const busy = fetcher.state !== "idle";
  
  return (
    <fetcher.Form method="post" action="/update-task/123">
      <input type="text" name="title" />
      <button type="submit">
        {busy ? "Saving..." : "Save"}
      </button>
    </fetcher.Form>
  );
}
```

Or imperatively:

```tsx
fetcher.submit(
  { title: "New Title" },
  { action: "/update-task/123", method: "post" }
);
```

## Accessing Action Data

Use `useActionData` in route components:

```tsx
import { useActionData, Form } from "react-router";

function Project() {
  const actionData = useActionData();
  
  return (
    <div>
      <h1>Project</h1>
      <Form method="post">
        <input type="text" name="title" />
        <button type="submit">Submit</button>
      </Form>
      {actionData && (
        <p>{actionData.title} updated</p>
      )}
    </div>
  );
}
```

With fetchers, use `fetcher.data`:

```tsx
function Component() {
  const fetcher = useFetcher();
  
  return (
    <div>
      {fetcher.data?.error && (
        <p style={{ color: "red" }}>{fetcher.data.error}</p>
      )}
    </div>
  );
}
```

## Action Examples

### Form Data Handling

```tsx
async function action({ request }) {
  const data = await request.formData();
  const title = data.get("title");
  const todo = await fakeDb.addItem({ title });
  return { ok: true };
}
```

### Validation

```tsx
async function action({ request }) {
  const data = await request.formData();
  const title = data.get("title") as string;
  
  if (title.trim() === "") {
    return { ok: false, error: "Title cannot be empty" };
  }
  
  await fakeDb.addItem({ title });
  return { ok: true, error: null };
}
```

### Redirects

```tsx
import { redirect } from "react-router";

async function action({ request }) {
  const data = await request.formData();
  await createProject(data);
  return redirect("/projects");
}
```

## Key Points

- **Automatic revalidation** - All loaders revalidate after action completes
- **Form data** - Access via `request.formData()`
- **Return data** - Available via `useActionData()` or `fetcher.data`
- **Error handling** - Return error objects, throw errors, or return redirects
- **Non-navigational** - Use fetchers to avoid navigation

<!--
Source references:
- https://reactrouter.com/start/data/actions
- https://reactrouter.com/start/data/route-object#action
-->
