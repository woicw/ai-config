---
name: react-router-use-action-data
description: useActionData hook to access action return data. Use when you need to read data returned from route actions.
---

# useActionData

The `useActionData` hook provides access to data returned from route actions.

## Basic Usage

```tsx
import { useActionData, Form } from "react-router";

function Project() {
  const actionData = useActionData();
  
  return (
    <div>
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

## TypeScript

Add type inference:

```tsx
import { useActionData } from "react-router";
import type { action } from "./route";

function Component() {
  const actionData = useActionData<typeof action>();
  // actionData is typed based on action return type
}
```

## Error Handling

Use action data for validation errors:

```tsx
async function action({ request }) {
  const data = await request.formData();
  const title = data.get("title") as string;
  
  if (title.trim() === "") {
    return { ok: false, error: "Title cannot be empty" };
  }
  
  await saveTitle(title);
  return { ok: true, error: null };
}

function Component() {
  const actionData = useActionData();
  
  return (
    <Form method="post">
      <input type="text" name="title" />
      {actionData?.error && (
        <p style={{ color: "red" }}>{actionData.error}</p>
      )}
      <button type="submit">Save</button>
    </Form>
  );
}
```

## Success Messages

Display success feedback:

```tsx
function Component() {
  const actionData = useActionData();
  
  return (
    <div>
      {actionData?.success && (
        <div className="success">{actionData.message}</div>
      )}
      <Form method="post">
        {/* form fields */}
      </Form>
    </div>
  );
}
```

## Key Points

- **Only after action** - Returns `undefined` until an action is called
- **Cleared on navigation** - Action data is cleared when navigating away
- **Type safety** - Use `useActionData<typeof action>()` for TypeScript
- **Error handling** - Return error objects from actions for validation

<!--
Source references:
- https://reactrouter.com/start/data/actions#accessing-action-data
-->
