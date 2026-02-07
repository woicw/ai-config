---
name: devtools
description: Redux DevTools integration for debugging Zustand stores
---

# Devtools Middleware

The `devtools` middleware connects Zustand stores to Redux DevTools for debugging.

## Basic Usage

```ts
import { create } from 'zustand'
import { devtools } from 'zustand/middleware'

const useBearStore = create<BearState>()(
  devtools(
    (set) => ({
      bears: 0,
      increase: (by) => set((state) => ({ bears: state.bears + by })),
    }),
  ),
)
```

## Configuration Options

### Store Name

```ts
devtools(
  (set) => ({ /* ... */ }),
  { name: 'BearStore' }, // appears in DevTools
)
```

### Action Names

Name actions for better debugging:

```ts
const useBearStore = create<BearState>()(
  devtools(
    (set) => ({
      bears: 0,
      increase: (by) =>
        set(
          (state) => ({ bears: state.bears + by }),
          false, // replace = false (default)
          'bears/increase', // action name
        ),
    }),
  ),
)
```

### Enable/Disable

```ts
devtools(
  (set) => ({ /* ... */ }),
  {
    name: 'BearStore',
    enabled: process.env.NODE_ENV === 'development',
  },
)
```

### Anonymous Actions

Disable warnings for unnamed actions:

```ts
devtools(
  (set) => ({ /* ... */ }),
  {
    name: 'BearStore',
    anonymousActionType: 'anonymous', // default action name
  },
)
```

---

## With TypeScript

### Complete Example

```ts
import { create } from 'zustand'
import { devtools } from 'zustand/middleware'

interface BearState {
  bears: number
  increase: (by: number) => void
  reset: () => void
}

const useBearStore = create<BearState>()(
  devtools(
    (set) => ({
      bears: 0,
      increase: (by) =>
        set(
          (state) => ({ bears: state.bears + by }),
          false,
          'bears/increase',
        ),
      reset: () =>
        set({ bears: 0 }, false, 'bears/reset'),
    }),
    { name: 'BearStore' },
  ),
)
```

---

## With Slices Pattern

Name actions with slice prefix for organization:

```ts
import { create, StateCreator } from 'zustand'
import { devtools } from 'zustand/middleware'

interface BearSlice {
  bears: number
  addBear: () => void
}

interface FishSlice {
  fishes: number
  addFish: () => void
}

const createBearSlice: StateCreator<
  BearSlice & FishSlice,
  [['zustand/devtools', never]],
  [],
  BearSlice
> = (set) => ({
  bears: 0,
  addBear: () =>
    set((state) => ({ bears: state.bears + 1 }), false, 'bear/addBear'),
})

const createFishSlice: StateCreator<
  BearSlice & FishSlice,
  [['zustand/devtools', never]],
  [],
  FishSlice
> = (set) => ({
  fishes: 0,
  addFish: () =>
    set((state) => ({ fishes: state.fishes + 1 }), false, 'fish/addFish'),
})

const useBoundStore = create<BearSlice & FishSlice>()(
  devtools(
    (...a) => ({
      ...createBearSlice(...a),
      ...createFishSlice(...a),
    }),
    { name: 'BoundStore' },
  ),
)
```

---

## Combining with Other Middleware

devtools should be the outermost middleware:

```ts
import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'

const useBearStore = create<BearState>()(
  devtools(
    persist(
      (set) => ({
        bears: 0,
        increase: (by) => set((state) => ({ bears: state.bears + by })),
      }),
      { name: 'bear-storage' },
    ),
    { name: 'BearStore' },
  ),
)
```

---

## DevTools Features

Once connected, Redux DevTools provides:

- **Time-travel debugging** - Step through state changes
- **Action history** - View all dispatched actions
- **State inspection** - Examine current and past states
- **Import/Export** - Save and restore state
- **Action replay** - Replay sequences of actions

<!--
Source references:
- https://zustand.docs.pmnd.rs/middlewares/devtools
-->
