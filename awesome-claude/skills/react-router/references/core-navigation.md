---
name: react-router-navigation
description: Navigation APIs for Data Mode. Use when navigating between routes with Link, NavLink, Form, redirect, or useNavigate.
---

# Navigation

Users navigate your application with `<Link>`, `<NavLink>`, `<Form>`, `redirect`, and `useNavigate`. Navigation in Data Mode works the same as Framework Mode.

## Link

Use `<Link>` for navigation links that don't need active styling:

```tsx
import { Link } from "react-router";

export function LoggedOutMessage() {
  return (
    <p>
      You've been logged out.{" "}
      <Link to="/login">Login again</Link>
    </p>
  );
}
```

## NavLink

Use `<NavLink>` for navigation links that need active and pending states:

```tsx
import { NavLink } from "react-router";

export function MyAppNav() {
  return (
    <nav>
      <NavLink to="/" end>Home</NavLink>
      <NavLink to="/trending" end>Trending Concerts</NavLink>
      <NavLink to="/concerts">All Concerts</NavLink>
      <NavLink to="/account">Account</NavLink>
    </nav>
  );
}
```

### Active States

`NavLink` renders default class names for styling:

```css
a.active {
  color: red;
}

a.pending {
  animate: pulse 1s infinite;
}

a.transitioning {
  /* css transition is running */
}
```

### Custom Styling

Use callback props for inline styling:

```tsx
// className
<NavLink
  to="/messages"
  className={({ isActive, isPending, isTransitioning }) =>
    [
      isPending ? "pending" : "",
      isActive ? "active" : "",
      isTransitioning ? "transitioning" : "",
    ].join(" ")
}
>
  Messages
</NavLink>

// style
<NavLink
  to="/messages"
  style={({ isActive, isPending, isTransitioning }) => ({
    fontWeight: isActive ? "bold" : "",
    color: isPending ? "red" : "black",
    viewTransitionName: isTransitioning ? "slide" : "",
  })}
>
  Messages
</NavLink>

// children
<NavLink to="/tasks">
  {({ isActive, isPending, isTransitioning }) => (
    <span className={isActive ? "active" : ""}>Tasks</span>
  )}
</NavLink>
```

## Form Navigation

Use `<Form>` to navigate with URLSearchParams:

```tsx
import { Form } from "react-router";

<Form action="/search">
  <input type="text" name="q" />
</Form>
```

If the user enters "journey" and submits, navigates to `/search?q=journey`.

Forms with `method="post"` will navigate to the action but submit as FormData. For POST submissions, prefer `useFetcher()`.

## redirect

Return `redirect` from loaders or actions to navigate:

```tsx
import { redirect } from "react-router";

// In loader
export async function loader({ request }) {
  const user = await getUser(request);
  if (!user) {
    return redirect("/login");
  }
  return { userName: user.name };
}

// In action
export async function action({ request }) {
  const formData = await request.formData();
  const project = await createProject(formData);
  return redirect(`/projects/${project.id}`);
}
```

## useNavigate

Use `useNavigate` for programmatic navigation without user interaction:

```tsx
import { useNavigate } from "react-router";

export function useLogoutAfterInactivity() {
  const navigate = useNavigate();
  
  useFakeInactivityHook(() => {
    navigate("/logout");
  });
}
```

### Navigate Options

```tsx
// Navigate with state
navigate("/path", { state: { from: "home" } });

// Replace history entry
navigate("/path", { replace: true });

// Relative navigation
navigate("../parent");

// With search params
navigate("/path?key=value");
```

## Key Points

- **Link vs NavLink** - Use `Link` for simple navigation, `NavLink` for active states
- **Form navigation** - Use for GET requests with search params
- **redirect** - Return from loaders/actions for server-side redirects
- **useNavigate** - Reserve for programmatic navigation without user interaction
- **Active states** - `NavLink` provides `isActive`, `isPending`, `isTransitioning`

<!--
Source references:
- https://reactrouter.com/start/data/navigating
- https://reactrouter.com/start/framework/navigating
-->
