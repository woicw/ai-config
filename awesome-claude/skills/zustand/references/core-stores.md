---
name: stores
description: Creating stores, state, actions, and selectors in Zustand
---

# Zustand Stores

Stores are created using `create()` function. Each store contains **state** and **actions** in a single object.

## Creating Stores

### Basic Store

```ts
import { create } from 'zustand'

const useBearStore = create((set) => ({
  bears: 0,
  increasePopulation: () => set((state) => ({ bears: state.bears + 1 })),
  removeAllBears: () => set({ bears: 0 }),
}))
```

### With TypeScript (Recommended)

Use the curried form `create<State>()((set) => ...)` for proper type inference:

```ts
import { create } from 'zustand'

interface BearState {
  bears: number
  food: string
  increase: (by: number) => void
  reset: () => void
}

const useBearStore = create<BearState>()((set) => ({
  bears: 0,
  food: 'honey',
  increase: (by) => set((state) => ({ bears: state.bears + by })),
  reset: () => set({ bears: 0, food: 'honey' }),
}))
```

### Using `get` for State Access in Actions

```ts
const useBearStore = create<BearState>()((set, get) => ({
  bears: 0,
  doublePopulation: () => {
    const currentBears = get().bears
    set({ bears: currentBears * 2 })
  },
}))
```

---

## Using Stores in Components

### Basic Usage

```tsx
function BearCounter() {
  const bears = useBearStore((state) => state.bears)
  return <h1>{bears} bears around here</h1>
}

function Controls() {
  const increase = useBearStore((state) => state.increase)
  return <button onClick={() => increase(1)}>Add bear</button>
}
```

### Selecting Multiple Values

```tsx
// ❌ Creates new object on every render - causes rerenders
const { bears, food } = useBearStore((state) => ({ bears: state.bears, food: state.food }))

// ✅ Use useShallow for object/array selectors
import { useShallow } from 'zustand/react/shallow'

const { bears, food } = useBearStore(
  useShallow((state) => ({ bears: state.bears, food: state.food }))
)

// ✅ Or select individually
const bears = useBearStore((state) => state.bears)
const food = useBearStore((state) => state.food)
```

### Derived/Computed Values

Calculate derived values in selectors (no caching, computed on each render):

```tsx
function TotalFood() {
  const totalFood = useBearStore((state) => state.bears * state.foodPerBear)
  return <div>Need {totalFood} jars of honey</div>
}
```

---

## State Updates

### Direct Updates

```ts
set({ bears: 10 })
```

### Functional Updates

```ts
set((state) => ({ bears: state.bears + 1 }))
```

### Replace vs Merge

By default, `set` merges state. To replace entirely:

```ts
// Merge (default)
set({ bears: 10 }) // { bears: 10, food: 'honey' }

// Replace entire state
set({ bears: 10 }, true) // { bears: 10 }
```

---

## Resetting State

### Pattern: Store Initial State

```ts
const initialState = { bears: 0, food: 'honey' }

type BearState = typeof initialState & {
  increase: (by: number) => void
  reset: () => void
}

const useBearStore = create<BearState>()((set) => ({
  ...initialState,
  increase: (by) => set((state) => ({ bears: state.bears + by })),
  reset: () => set(initialState),
}))
```

---

## Async Actions

Actions can be async - no special syntax needed:

```ts
const useFishStore = create<FishState>()((set) => ({
  fishes: [],
  loading: false,
  error: null,
  
  fetchFishes: async () => {
    set({ loading: true, error: null })
    try {
      const response = await fetch('/api/fishes')
      const fishes = await response.json()
      set({ fishes, loading: false })
    } catch (error) {
      set({ error: error.message, loading: false })
    }
  },
}))
```

---

## Subscriptions

### Subscribe to State Changes

```ts
// Subscribe to all changes
const unsub = useBearStore.subscribe((state, prevState) => {
  console.log('State changed:', state)
})

// Unsubscribe
unsub()
```

### With subscribeWithSelector Middleware

See [middleware-subscribe-with-selector](middleware-subscribe-with-selector.md) for selective subscriptions.

---

## Accessing Store Outside React

### Using `getState()` and `setState()`

```ts
// Get current state
const bears = useBearStore.getState().bears

// Update state
useBearStore.setState({ bears: 10 })

// Get initial state
const initial = useBearStore.getInitialState()
```

### In Event Handlers, Utilities, etc.

```ts
// api.ts
import { useBearStore } from './stores/bear'

export async function fetchAndUpdateBears() {
  const response = await fetch('/api/bears')
  const data = await response.json()
  useBearStore.setState({ bears: data.count })
}
```

---

## Vanilla Store (Non-React)

Use `createStore` for vanilla JavaScript or when you need the store API:

```ts
import { createStore } from 'zustand/vanilla'

const store = createStore<BearState>()((set) => ({
  bears: 0,
  increase: (by) => set((state) => ({ bears: state.bears + by })),
}))

// Use the API
const { getState, setState, subscribe, getInitialState } = store

// Access state
console.log(getState().bears)

// Subscribe
subscribe((state) => console.log('Bears:', state.bears))
```

### Using Vanilla Store in React

```ts
import { useStore } from 'zustand'
import { store } from './vanilla-store'

function Component() {
  const bears = useStore(store, (state) => state.bears)
  return <div>{bears}</div>
}
```

<!--
Source references:
- https://zustand.docs.pmnd.rs/getting-started/introduction
- https://zustand.docs.pmnd.rs/apis/create
- https://zustand.docs.pmnd.rs/guides/beginner-typescript
- https://zustand.docs.pmnd.rs/guides/advanced-typescript
-->
