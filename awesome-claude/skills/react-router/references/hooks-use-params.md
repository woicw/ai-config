---
name: react-router-use-params
description: useParams hook to access dynamic route parameters. Use when you need to read URL parameters from route path segments.
---

# useParams

The `useParams` hook returns an object of key/value pairs of the dynamic params from the current URL that were matched by the routes. Child routes inherit all params from their parent routes.

## Basic Usage

```tsx
import { useParams } from "react-router";

// Given a route like:
// createBrowserRouter([{ path: "/posts/:postId", Component: Post }])

function Post() {
  const params = useParams();
  return <h1>Post: {params.postId}</h1>;
}
```

## TypeScript

Add type safety with TypeScript:

```tsx
function Post() {
  const params = useParams<{ postId: string }>();
  return <h1>Post: {params.postId}</h1>;
}
```

## Multiple Params

Patterns can have multiple params:

```tsx
// Route: "/posts/:postId/comments/:commentId"

function Comment() {
  const params = useParams();
  return (
    <h1>
      Post: {params.postId}, Comment: {params.commentId}
    </h1>
  );
}
```

## Destructuring

Destructure params for cleaner code:

```tsx
function Post() {
  const { postId } = useParams();
  return <h1>Post: {postId}</h1>;
}
```

## Catchall Params

Catchall params are defined with `*`:

```tsx
// Route: "/files/*"

function File() {
  const params = useParams();
  const catchall = params["*"];
  // ...
}
```

Or destructure the catchall param:

```tsx
function File() {
  const { "*": catchall } = useParams();
  console.log(catchall);
}
```

## Nested Routes

Child routes inherit all params from parent routes:

```tsx
createBrowserRouter([
  {
    path: "/posts/:postId",
    Component: PostLayout,
    children: [
      {
        path: "comments/:commentId",
        Component: Comment,
      },
    ],
  },
]);

function Comment() {
  const params = useParams();
  // params.postId is available from parent route
  // params.commentId is from current route
  return (
    <div>
      Post {params.postId}, Comment {params.commentId}
    </div>
  );
}
```

## Using in Loaders

Params are also available in loaders:

```tsx
createBrowserRouter([
  {
    path: "/posts/:postId",
    loader: ({ params }) => {
      // params.postId available here
      return getPost(params.postId);
    },
    Component: Post,
  },
]);
```

## Key Points

- **Dynamic segments** - Access values from `:paramName` route segments
- **Inheritance** - Child routes inherit parent route params
- **String values** - All params are strings, convert if needed
- **Type safety** - Use TypeScript generics for type checking
- **Catchall** - Use `params["*"]` for catchall routes

<!--
Source references:
- https://reactrouter.com/api/hooks/useParams
- https://reactrouter.com/start/declarative/url-values#route-params
-->
