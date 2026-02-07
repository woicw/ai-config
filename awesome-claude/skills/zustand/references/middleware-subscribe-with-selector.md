---
name: subscribeWithSelector
description: Subscribe to specific state slices for granular updates
---

# SubscribeWithSelector Middleware

The `subscribeWithSelector` middleware allows subscribing to specific state slices outside of React components.

## Basic Usage

```ts
import { createStore } from 'zustand/vanilla'
import { subscribeWithSelector } from 'zustand/middleware'

interface PositionState {
  position: { x: number; y: number }
  setPosition: (position: { x: number; y: number }) => void
}

const store = createStore<PositionState>()(
  subscribeWithSelector((set) => ({
    position: { x: 0, y: 0 },
    setPosition: (position) => set({ position }),
  })),
)
```

## Subscribing to State Slices

### Basic Selector

```ts
// Subscribe to position changes only
store.subscribe(
  (state) => state.position,
  (position) => {
    console.log('Position changed:', position)
  },
)
```

### Deep Property Selector

```ts
// Subscribe to x coordinate only
store.subscribe(
  (state) => state.position.x,
  (x) => {
    console.log('X changed:', x)
  },
)
```

### With Equality Function

```ts
import { shallow } from 'zustand/shallow'

// Use shallow comparison
store.subscribe(
  (state) => state.position,
  (position) => console.log(position),
  { equalityFn: shallow },
)
```

### Fire Immediately

```ts
// Fire callback immediately with current state
store.subscribe(
  (state) => state.position,
  (position) => console.log(position),
  { fireImmediately: true },
)
```

---

## Use Cases

### DOM Updates (Vanilla JS)

```ts
const $dot = document.getElementById('dot')

store.subscribe(
  (state) => state.position,
  (position) => {
    $dot.style.transform = `translate(${position.x}px, ${position.y}px)`
  },
)
```

### Logging State Changes

```ts
store.subscribe(
  (state) => state,
  (state, prevState) => {
    console.log('State changed from', prevState, 'to', state)
  },
)
```

### Side Effects

```ts
store.subscribe(
  (state) => state.isLoggedIn,
  (isLoggedIn) => {
    if (isLoggedIn) {
      analytics.track('user_logged_in')
    }
  },
)
```

---

## With React Store

Also works with `create`:

```ts
import { create } from 'zustand'
import { subscribeWithSelector } from 'zustand/middleware'

const useBearStore = create<BearState>()(
  subscribeWithSelector((set) => ({
    bears: 0,
    increase: () => set((state) => ({ bears: state.bears + 1 })),
  })),
)

// Now you can use selective subscriptions
useBearStore.subscribe(
  (state) => state.bears,
  (bears) => console.log('Bears:', bears),
)
```

---

## Combining with Other Middleware

```ts
import { create } from 'zustand'
import { devtools, subscribeWithSelector } from 'zustand/middleware'

const useBearStore = create<BearState>()(
  devtools(
    subscribeWithSelector((set) => ({
      bears: 0,
      increase: () => set((state) => ({ bears: state.bears + 1 })),
    })),
    { name: 'BearStore' },
  ),
)
```

---

## TypeScript

### Full Type Safety

```ts
import { createStore } from 'zustand/vanilla'
import { subscribeWithSelector } from 'zustand/middleware'

interface State {
  count: number
  name: string
}

interface Actions {
  increment: () => void
}

const store = createStore<State & Actions>()(
  subscribeWithSelector((set) => ({
    count: 0,
    name: 'Zustand',
    increment: () => set((state) => ({ count: state.count + 1 })),
  })),
)

// Selector return type is inferred
store.subscribe(
  (state) => state.count, // selector returns number
  (count) => console.log(count), // count is typed as number
)
```

<!--
Source references:
- https://zustand.docs.pmnd.rs/middlewares/subscribe-with-selector
-->
