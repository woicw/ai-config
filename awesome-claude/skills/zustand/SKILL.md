---
name: zustand
description: Zustand is a small, fast, scalable state management library for React. Use when creating stores, managing state/actions, using middleware (persist, devtools, immer), or implementing state patterns in React apps.
metadata:
  author: woic
  version: "2026.2.5"
  source: Generated from https://zustand.docs.pmnd.rs
---

# Zustand

Zustand is a small, fast, and scalable state-management solution for React. It offers a simple hook-based API without boilerplate, with first-class TypeScript support and excellent devtools integration.

> The skill is based on Zustand v5.x, generated at 2026-02-05.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Stores | Creating stores, state, actions, selectors, TypeScript patterns | [core-stores](references/core-stores.md) |

## Middleware

| Topic | Description | Reference |
|-------|-------------|-----------|
| Persist | Persisting store data to localStorage/sessionStorage | [middleware-persist](references/middleware-persist.md) |
| Devtools | Redux DevTools integration for debugging | [middleware-devtools](references/middleware-devtools.md) |
| Immer | Write immutable updates with mutable syntax | [middleware-immer](references/middleware-immer.md) |
| SubscribeWithSelector | Subscribe to specific state slices | [middleware-subscribe-with-selector](references/middleware-subscribe-with-selector.md) |

## Patterns

| Topic | Description | Reference |
|-------|-------------|-----------|
| Slices Pattern | Modular store organization for large apps | [patterns-slices](references/patterns-slices.md) |
| Auto Selectors | Auto-generating selectors for cleaner code | [patterns-auto-selectors](references/patterns-auto-selectors.md) |

## Best Practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| Testing | Unit testing stores with Jest/Vitest, mocking, resetting | [best-practices-testing](references/best-practices-testing.md) |
| Prevent Rerenders | Using useShallow and equality functions | [best-practices-prevent-rerenders](references/best-practices-prevent-rerenders.md) |

## Framework Integration

| Topic | Description | Reference |
|-------|-------------|-----------|
| Next.js | Next.js integration, SSR, hydration, context provider | [integration-nextjs](references/integration-nextjs.md) |

## Key Recommendations

- **Use curried form with TypeScript** - `create<State>()(...)` for proper type inference
- **Use selectors** to subscribe to specific state slices and prevent unnecessary rerenders
- **Wrap selectors with `useShallow`** when returning objects/arrays to use shallow comparison
- **Actions don't need `this`** - access state via `get()` parameter
- **Store is a hook** - call it directly in components without providers
- **Use `getState()` outside React** - access store state in non-React code
- **Combine middleware carefully** - order matters: `devtools(persist(immer(...)))`
- **Reset stores in tests** - use mock pattern to reset all stores after each test
