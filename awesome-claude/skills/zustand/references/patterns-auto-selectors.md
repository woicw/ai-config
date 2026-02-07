---
name: auto-selectors
description: Auto-generating selectors for cleaner store access
---

# Auto-generating Selectors

Auto-generating selectors simplifies store access by creating individual hooks for each state property and action.

## For React Stores

### createSelectors Utility

```ts
import { StoreApi, UseBoundStore } from 'zustand'

type WithSelectors<S> = S extends { getState: () => infer T }
  ? S & { use: { [K in keyof T]: () => T[K] } }
  : never

const createSelectors = <S extends UseBoundStore<StoreApi<object>>>(
  _store: S,
) => {
  const store = _store as WithSelectors<typeof _store>
  store.use = {}
  for (const k of Object.keys(store.getState())) {
    ;(store.use as any)[k] = () => store((s) => s[k as keyof typeof s])
  }
  return store
}
```

### Usage

```ts
import { create } from 'zustand'

interface BearState {
  bears: number
  increase: (by: number) => void
  increment: () => void
}

const useBearStoreBase = create<BearState>()((set) => ({
  bears: 0,
  increase: (by) => set((state) => ({ bears: state.bears + by })),
  increment: () => set((state) => ({ bears: state.bears + 1 })),
}))

// Wrap with createSelectors
export const useBearStore = createSelectors(useBearStoreBase)
```

### In Components

```tsx
function BearCounter() {
  // Auto-generated selectors via .use
  const bears = useBearStore.use.bears()
  const increment = useBearStore.use.increment()

  return (
    <div>
      <span>{bears}</span>
      <button onClick={increment}>+1</button>
    </div>
  )
}
```

---

## For Vanilla Stores

### createSelectors for Vanilla

```ts
import { StoreApi, useStore, createStore } from 'zustand'

type WithSelectors<S> = S extends { getState: () => infer T }
  ? S & { use: { [K in keyof T]: () => T[K] } }
  : never

const createSelectors = <S extends StoreApi<object>>(_store: S) => {
  const store = _store as WithSelectors<typeof _store>
  store.use = {}
  for (const k of Object.keys(store.getState())) {
    ;(store.use as any)[k] = () =>
      useStore(_store, (s) => s[k as keyof typeof s])
  }
  return store
}
```

### Usage with Vanilla Store

```ts
import { createStore } from 'zustand/vanilla'

interface BearState {
  bears: number
  increase: (by: number) => void
}

const store = createStore<BearState>()((set) => ({
  bears: 0,
  increase: (by) => set((state) => ({ bears: state.bears + by })),
}))

export const useBearStore = createSelectors(store)
```

---

## Benefits

### Without Auto Selectors

```tsx
// Manual selectors - repetitive
const bears = useBearStore((state) => state.bears)
const increase = useBearStore((state) => state.increase)
const increment = useBearStore((state) => state.increment)
```

### With Auto Selectors

```tsx
// Clean and concise
const bears = useBearStore.use.bears()
const increase = useBearStore.use.increase()
const increment = useBearStore.use.increment()
```

---

## TypeScript Support

The utility is fully typed:

```tsx
// Type-safe: bears is number
const bears = useBearStore.use.bears()

// Type-safe: increase expects (by: number) => void
const increase = useBearStore.use.increase()

// TypeScript error if property doesn't exist
const invalid = useBearStore.use.nonExistent() // ❌ Error
```

---

## Caveats

### Reactivity

Each `.use.property()` call creates a separate subscription. This is usually desired for preventing unnecessary rerenders.

### Adding New Properties

If state shape changes dynamically, selectors won't auto-update. The utility generates selectors based on initial state.

### Middleware Compatibility

Works with all middleware - just apply `createSelectors` after creating the store:

```ts
import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'

const useBearStoreBase = create<BearState>()(
  devtools(
    persist(
      (set) => ({
        bears: 0,
        increase: (by) => set((state) => ({ bears: state.bears + by })),
      }),
      { name: 'bear-storage' },
    ),
  ),
)

export const useBearStore = createSelectors(useBearStoreBase)
```

<!--
Source references:
- https://zustand.docs.pmnd.rs/guides/auto-generating-selectors
-->
