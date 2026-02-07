---
name: prevent-rerenders
description: Preventing unnecessary rerenders with selectors and equality functions
---

# Preventing Rerenders

Zustand uses strict equality (`===`) by default to detect changes. Understanding this helps prevent unnecessary rerenders.

## The Problem

### Object/Array Selectors Cause Rerenders

```tsx
// ❌ Creates new object every render - always triggers rerender
const { bears, food } = useBearStore((state) => ({
  bears: state.bears,
  food: state.food,
}))
```

Even if `bears` and `food` haven't changed, a new object is created on each render, failing the strict equality check.

---

## Solutions

### 1. Use Individual Selectors (Recommended)

```tsx
// ✅ Each selector returns a primitive - optimal rerenders
const bears = useBearStore((state) => state.bears)
const food = useBearStore((state) => state.food)
```

### 2. Use `useShallow`

```tsx
import { useShallow } from 'zustand/react/shallow'

// ✅ Shallow comparison prevents unnecessary rerenders
const { bears, food } = useBearStore(
  useShallow((state) => ({ bears: state.bears, food: state.food })),
)
```

### 3. Use Array Destructuring with `useShallow`

```tsx
import { useShallow } from 'zustand/react/shallow'

// ✅ Works with arrays too
const [bears, food] = useBearStore(
  useShallow((state) => [state.bears, state.food]),
)
```

---

## When to Use `useShallow`

### Object Returns

```tsx
// When selecting multiple properties as an object
const { count, name, age } = useStore(
  useShallow((state) => ({
    count: state.count,
    name: state.name,
    age: state.age,
  })),
)
```

### Array Returns

```tsx
// When selecting as array
const [count, name] = useStore(
  useShallow((state) => [state.count, state.name]),
)
```

### Computed Arrays

```tsx
// When returning computed arrays
const names = useMeals(
  useShallow((state) => Object.keys(state)),
)
```

---

## Custom Equality Functions

### Using `useStoreWithEqualityFn`

For more control, use `useStoreWithEqualityFn`:

```tsx
import { useStoreWithEqualityFn } from 'zustand/traditional'
import { shallow } from 'zustand/shallow'

// With React store
const position = useStoreWithEqualityFn(
  usePositionStore,
  (state) => state.position,
  shallow,
)
```

### With Vanilla Store

```tsx
import { createStore } from 'zustand/vanilla'
import { useStoreWithEqualityFn } from 'zustand/traditional'
import { shallow } from 'zustand/shallow'

const store = createStore<PositionState>()((set) => ({
  position: { x: 0, y: 0 },
  setPosition: (position) => set({ position }),
}))

function Component() {
  const position = useStoreWithEqualityFn(
    store,
    (state) => state.position,
    shallow,
  )
  return <div>{position.x}, {position.y}</div>
}
```

---

## Deep Equality (Rare)

For deeply nested objects, use a deep equality function:

```tsx
import { useStoreWithEqualityFn } from 'zustand/traditional'
import isEqual from 'lodash/isEqual'

const deepNested = useStoreWithEqualityFn(
  useStore,
  (state) => state.deeply.nested.data,
  isEqual, // Deep comparison
)
```

**Note:** Deep equality is expensive. Prefer restructuring state to avoid deep nesting.

---

## Selector Stability

### Memoize Complex Selectors

```tsx
import { useMemo } from 'react'

function Component() {
  // ❌ Creates new function every render
  const data = useStore((state) => state.items.filter((i) => i.active))

  // ✅ Stable selector with useMemo
  const activeItems = useStore(
    useMemo(() => (state) => state.items.filter((i) => i.active), []),
  )
}
```

### Alternatively: Compute in Render

```tsx
function Component() {
  const items = useStore((state) => state.items)
  
  // Compute outside selector - items must change for rerender
  const activeItems = items.filter((i) => i.active)
  
  return <List items={activeItems} />
}
```

---

## Debugging Rerenders

### Track Rerenders

```tsx
function Component() {
  const bears = useBearStore((state) => state.bears)
  
  // Debug: log when component renders
  console.log('Component rendered, bears:', bears)
  
  return <div>{bears}</div>
}
```

### Use React DevTools

React DevTools Profiler can identify unnecessary rerenders and their causes.

<!--
Source references:
- https://zustand.docs.pmnd.rs/guides/prevent-rerenders-with-use-shallow
- https://zustand.docs.pmnd.rs/hooks/use-store-with-equality-fn
-->
