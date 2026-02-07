---
name: react-router-data-strategy
description: Advanced control over loader/action execution with dataStrategy. Use when you need custom middleware, sequential loading, or custom handler execution.
---

# Data Strategy

The `dataStrategy` option gives you full control over how your loader and action functions are executed. This is a low-level API for advanced use-cases like middleware, context, and caching layers.

## Basic Usage

```tsx
let router = createBrowserRouter(routes, {
  async dataStrategy({ matches, request, runClientMiddleware }) {
    // Determine which matches should execute handlers
    const matchesToLoad = matches.filter((m) => m.shouldCallHandler());
    
    // Execute handlers and store results
    const results: Record<string, DataStrategyResult> = {};
    
    await runClientMiddleware(() =>
      Promise.all(
        matchesToLoad.map(async (match) => {
          console.log(`Processing ${match.route.id}`);
          results[match.route.id] = await match.resolve();
        })
      )
    );
    
    return results;
  },
});
```

## Function Arguments

The `dataStrategy` function receives:

```tsx
async function dataStrategy({
  matches,           // Array of matched routes
  request,           // Web Fetch Request
  params,            // Route params
  context,           // Custom context (if provided)
  runClientMiddleware, // Helper to run middleware
  fetcherKey,        // Fetcher key or null
}) {
  // ...
}
```

## Match Properties

Each match in the `matches` array has:

- `shouldCallHandler()` - Function indicating if handler should be called
- `shouldRevalidateArgs` - Arguments for `shouldRevalidate`
- `resolve()` - Function to execute the route handler
- `route` - The route object

## Adding Logging

Simple example with logging:

```tsx
let router = createBrowserRouter(routes, {
  async dataStrategy({ matches, runClientMiddleware }) {
    const matchesToLoad = matches.filter((m) => m.shouldCallHandler());
    
    const results: Record<string, DataStrategyResult> = {};
    
    await runClientMiddleware(() =>
      Promise.all(
        matchesToLoad.map(async (match) => {
          console.log(`Processing ${match.route.id}`);
          results[match.route.id] = await match.resolve();
        })
      )
    );
    
    return results;
  },
});
```

## Custom Middleware

Run middleware sequentially before loaders:

```tsx
const routes = [
  {
    id: "parent",
    path: "/parent",
    loader({ request }, context) {
      // Use context from middleware
    },
    handle: {
      async middleware({ request }, context) {
        context.parent = "PARENT MIDDLEWARE";
      },
    },
    children: [
      {
        id: "child",
        path: "child",
        loader({ request }, context) {
          // Use context from middleware
        },
        handle: {
          async middleware({ request }, context) {
            context.child = "CHILD MIDDLEWARE";
          },
        },
      },
    ],
  },
];

let router = createBrowserRouter(routes, {
  async dataStrategy({ matches, request, params, runClientMiddleware }) {
    // Run middleware sequentially
    let context = {};
    for (const match of matches) {
      if (match.route.handle?.middleware) {
        await match.route.handle.middleware({ request, params }, context);
      }
    }
    
    // Run loaders in parallel with context
    const matchesToLoad = matches.filter((m) => m.shouldCallHandler());
    const results = await runClientMiddleware(() =>
      Promise.all(
        matchesToLoad.map((match) =>
          match.resolve((handler) => {
            // Pass context as second parameter to loader
            return handler(context);
          })
        )
      )
    );
    
    return results.reduce(
      (acc, result, i) =>
        Object.assign(acc, {
          [matchesToLoad[i].route.id]: result,
        }),
      {}
    );
  },
});
```

## Custom Handler Execution

Override handler execution completely:

```tsx
const routes = [
  {
    id: "parent",
    path: "/parent",
    loader: true, // Mark as having loader
    handle: {
      gql: gql`fragment Parent on Whatever { parentField }`,
    },
    children: [
      {
        id: "child",
        path: "child",
        loader: true,
        handle: {
          gql: gql`fragment Child on Whatever { childField }`,
        },
      },
    ],
  },
];

let router = createBrowserRouter(routes, {
  async dataStrategy({ matches, request, params }) {
    const matchesToLoad = matches.filter((m) => m.shouldCallHandler());
    
    // Compose fragments into single GQL payload
    const gql = getFragmentsFromRouteHandles(matchesToLoad);
    const data = await fetchGql(gql);
    
    // Parse results back into route-level DataStrategyResult's
    const results = parseResultsFromGql(matchesToLoad, data);
    return results;
  },
});
```

## Custom Revalidation

Alter revalidation behavior:

```tsx
let router = createBrowserRouter(routes, {
  async dataStrategy({ matches }) {
    const matchesToLoad = matches.filter((match) => {
      const defaultShouldRevalidate = customShouldRevalidate(
        match.shouldRevalidateArgs
      );
      return match.shouldCallHandler(defaultShouldRevalidate);
    });
    
    // Execute handlers...
  },
});
```

## Key Points

- **Low-level API** - Advanced use-case only, use with caution
- **Full control** - Override React Router's default parallel execution
- **Middleware support** - Use `runClientMiddleware` helper
- **Custom handlers** - Can completely replace route handler execution
- **Context passing** - Pass custom context to loaders/actions
- **Sequential execution** - Run middleware sequentially, loaders in parallel

<!--
Source references:
- https://reactrouter.com/how-to/data-strategy
- https://reactrouter.com/v6/routers/create-browser-router#optsdatastrategy
-->
