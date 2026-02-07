---
name: react-router-use-navigation
description: useNavigation hook to access navigation state for pending UI. Use when you need to show loading states during navigation.
---

# useNavigation

The `useNavigation` hook provides access to the current navigation state, useful for showing pending UI during navigations and form submissions.

## Basic Usage

```tsx
import { useNavigation } from "react-router";

function Component() {
  const navigation = useNavigation();
  
  if (navigation.state === "loading") {
    return <div>Loading...</div>;
  }
  
  return <div>Content</div>;
}
```

## Navigation State

Access the current navigation state:

```tsx
function Component() {
  const navigation = useNavigation();
  
  const isNavigating = navigation.state !== "idle";
  const isSubmitting = navigation.state === "submitting";
  const isLoading = navigation.state === "loading";
  
  return (
    <div>
      {isNavigating && <div>Processing...</div>}
      {/* content */}
    </div>
  );
}
```

Navigation states:
- `idle` - No active navigation
- `submitting` - Form submission in progress
- `loading` - Loader execution in progress

## Form Method

Check which form method is being used:

```tsx
function Component() {
  const navigation = useNavigation();
  
  const isPosting = navigation.formMethod === "post";
  const isDeleting = navigation.formMethod === "delete";
  
  return (
    <div>
      {isPosting && <div>Creating...</div>}
      {isDeleting && <div>Deleting...</div>}
    </div>
  );
}
```

## Form Action

Check which route action is being called:

```tsx
function Component() {
  const navigation = useNavigation();
  
  const isUpdating = navigation.formAction === "/projects/123";
  
  return (
    <div>
      {isUpdating && <div>Updating project...</div>}
    </div>
  );
}
```

## Location

Access the location being navigated to:

```tsx
function Component() {
  const navigation = useNavigation();
  
  const isGoingToProjects = navigation.location?.pathname === "/projects";
  
  return (
    <div>
      {isGoingToProjects && <div>Navigating to projects...</div>}
    </div>
  );
}
```

## Pending UI Pattern

Common pattern for showing pending UI:

```tsx
function Component() {
  const navigation = useNavigation();
  const data = useLoaderData();
  
  const isPending = navigation.state === "loading";
  
  return (
    <div>
      {isPending ? (
        <div>Loading...</div>
      ) : (
        <div>{data.content}</div>
      )}
    </div>
  );
}
```

## Form Submission Pattern

Show different UI for form submissions:

```tsx
function Component() {
  const navigation = useNavigation();
  
  const isSubmitting = navigation.state === "submitting";
  
  return (
    <Form method="post">
      <input type="text" name="title" disabled={isSubmitting} />
      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? "Saving..." : "Save"}
      </button>
    </Form>
  );
}
```

## Navigation Properties

- `state` - Current state: "idle" | "submitting" | "loading"
- `location` - Location being navigated to (null when idle)
- `formMethod` - HTTP method if submitting: "get" | "post" | "put" | "patch" | "delete"
- `formAction` - Action URL if submitting
- `formData` - FormData if submitting

## Key Points

- **Pending UI** - Use for showing loading states during navigation
- **Form submissions** - Check `formMethod` and `formAction` for form-specific UI
- **Location** - Access target location during navigation
- **State management** - Track navigation progress for better UX

<!--
Source references:
- https://reactrouter.com/start/data/pending-ui
-->
