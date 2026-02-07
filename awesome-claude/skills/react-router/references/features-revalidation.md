---
name: react-router-revalidation
description: Control when loader data revalidates with shouldRevalidate. Use when you need custom control over data freshness.
---

# Revalidation Control

Loader data is automatically revalidated after certain events. The `shouldRevalidate` function enables you to opt in or out of the default revalidation behavior.

## Default Revalidation Behavior

By default, a route loader is revalidated when:
- Its own route params change
- Any change to URL search params
- After an action is called and returns a non-error status code

## Basic Usage

```tsx
import type { ShouldRevalidateFunctionArgs } from "react-router";

function shouldRevalidate(arg: ShouldRevalidateFunctionArgs) {
  return true; // or false
}

createBrowserRouter([
  {
    path: "/",
    shouldRevalidate: shouldRevalidate,
    Component: MyRoute,
  },
]);
```

## Function Arguments

The `shouldRevalidate` function receives arguments:

```tsx
function shouldRevalidate({
  currentUrl,
  currentParams,
  nextUrl,
  nextParams,
  formMethod,
  formAction,
  formData,
  actionResult,
  defaultShouldRevalidate,
}) {
  // Return true to revalidate, false to skip
  return true;
}
```

## Conditional Revalidation

Only revalidate under specific conditions:

```tsx
function shouldRevalidate({ formMethod, formAction }) {
  // Only revalidate on POST to /update
  if (formMethod === "post" && formAction === "/update") {
    return true;
  }
  return false;
}
```

## Skip Revalidation

Prevent revalidation in certain cases:

```tsx
function shouldRevalidate({ formMethod }) {
  // Skip revalidation for GET requests
  if (formMethod === "get") {
    return false;
  }
  return true;
}
```

## Based on Action Result

Check action result before revalidating:

```tsx
function shouldRevalidate({ actionResult }) {
  // Only revalidate if action succeeded
  if (actionResult?.ok) {
    return true;
  }
  return false;
}
```

## URL-Based Logic

Compare current and next URLs:

```tsx
function shouldRevalidate({ currentUrl, nextUrl }) {
  // Only revalidate if pathname changed
  if (currentUrl.pathname !== nextUrl.pathname) {
    return true;
  }
  return false;
}
```

## Default Behavior

Use `defaultShouldRevalidate` to extend default behavior:

```tsx
function shouldRevalidate({ defaultShouldRevalidate, formMethod }) {
  // Use default behavior, but skip for GET
  if (formMethod === "get") {
    return false;
  }
  return defaultShouldRevalidate;
}
```

## Key Points

- **Opt-out behavior** - Defining `shouldRevalidate` opts out of default behavior completely
- **Full control** - You have complete control over when loaders revalidate
- **Action-based** - Check `formMethod`, `formAction`, `actionResult` for action-triggered revalidation
- **URL-based** - Compare `currentUrl` and `nextUrl` for navigation-based revalidation
- **Default helper** - Use `defaultShouldRevalidate` to extend rather than replace default behavior

<!--
Source references:
- https://reactrouter.com/start/data/route-object#shouldrevalidate
-->
