---
name: immer
description: Write immutable updates with mutable syntax using Immer
---

# Immer Middleware

The `immer` middleware lets you write state updates using mutable syntax, which Immer converts to immutable updates.

## Basic Usage

```ts
import { create } from 'zustand'
import { immer } from 'zustand/middleware/immer'

interface State {
  count: number
  nested: { value: number }
}

interface Actions {
  increment: () => void
  updateNested: (value: number) => void
}

const useStore = create<State & Actions>()(
  immer((set) => ({
    count: 0,
    nested: { value: 0 },
    increment: () =>
      set((state) => {
        state.count += 1 // Mutate directly
      }),
    updateNested: (value) =>
      set((state) => {
        state.nested.value = value // Deep updates are easy
      }),
  })),
)
```

## Benefits

### Simplified Nested Updates

Without Immer:

```ts
// ❌ Verbose immutable updates
set((state) => ({
  deeply: {
    ...state.deeply,
    nested: {
      ...state.deeply.nested,
      object: {
        ...state.deeply.nested.object,
        value: 'updated',
      },
    },
  },
}))
```

With Immer:

```ts
// ✅ Simple mutable syntax
set((state) => {
  state.deeply.nested.object.value = 'updated'
})
```

### Array Operations

```ts
const useTodoStore = create<TodoState>()(
  immer((set) => ({
    todos: [],
    
    addTodo: (text) =>
      set((state) => {
        state.todos.push({ id: Date.now(), text, done: false })
      }),
    
    toggleTodo: (id) =>
      set((state) => {
        const todo = state.todos.find((t) => t.id === id)
        if (todo) todo.done = !todo.done
      }),
    
    removeTodo: (id) =>
      set((state) => {
        const index = state.todos.findIndex((t) => t.id === id)
        if (index !== -1) state.todos.splice(index, 1)
      }),
  })),
)
```

---

## TypeScript

### With Type Annotations

```ts
import { create } from 'zustand'
import { immer } from 'zustand/middleware/immer'

type State = {
  count: number
}

type Actions = {
  increment: (qty: number) => void
  decrement: (qty: number) => void
}

const useCountStore = create<State & Actions>()(
  immer((set) => ({
    count: 0,
    increment: (qty) =>
      set((state) => {
        state.count += qty
      }),
    decrement: (qty) =>
      set((state) => {
        state.count -= qty
      }),
  })),
)
```

---

## Combining with Other Middleware

immer should be the innermost middleware:

```ts
import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'
import { immer } from 'zustand/middleware/immer'

const useBearStore = create<BearState>()(
  devtools(
    persist(
      immer((set) => ({
        bears: 0,
        increase: (by) =>
          set((state) => {
            state.bears += by
          }),
      })),
      { name: 'bear-storage' },
    ),
    { name: 'BearStore' },
  ),
)
```

---

## Caveats

### Return Value

When using immer, you can either mutate state OR return new state, not both:

```ts
// ✅ Mutate state
set((state) => {
  state.count += 1
})

// ✅ Return new state (ignores mutations)
set((state) => ({ count: state.count + 1 }))

// ❌ Don't do both
set((state) => {
  state.count += 1
  return { count: 10 } // Mutations are ignored!
})
```

### Primitives

Don't reassign the draft directly:

```ts
// ❌ Wrong - reassigning draft
set((state) => {
  state = { count: 0 } // This doesn't work
})

// ✅ Correct - mutate properties
set((state) => {
  state.count = 0
})
```

<!--
Source references:
- https://zustand.docs.pmnd.rs/integrations/immer-middleware
-->
