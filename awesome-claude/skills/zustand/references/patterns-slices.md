---
name: slices-pattern
description: Modular store organization using the slices pattern
---

# Slices Pattern

The slices pattern divides state and actions into independent modules, improving maintainability for larger applications.

## Basic Slices

### Define Individual Slices

```ts
// bearSlice.ts
import { StateCreator } from 'zustand'

export interface BearSlice {
  bears: number
  addBear: () => void
}

export const createBearSlice: StateCreator<BearSlice> = (set) => ({
  bears: 0,
  addBear: () => set((state) => ({ bears: state.bears + 1 })),
})
```

```ts
// fishSlice.ts
import { StateCreator } from 'zustand'

export interface FishSlice {
  fishes: number
  addFish: () => void
}

export const createFishSlice: StateCreator<FishSlice> = (set) => ({
  fishes: 0,
  addFish: () => set((state) => ({ fishes: state.fishes + 1 })),
})
```

### Combine Slices

```ts
// store.ts
import { create } from 'zustand'
import { createBearSlice, BearSlice } from './bearSlice'
import { createFishSlice, FishSlice } from './fishSlice'

export const useBoundStore = create<BearSlice & FishSlice>()((...a) => ({
  ...createBearSlice(...a),
  ...createFishSlice(...a),
}))
```

---

## Cross-Slice Communication

### Accessing Other Slices

When a slice needs to access another slice's state or actions:

```ts
import { StateCreator } from 'zustand'

interface BearSlice {
  bears: number
  addBear: () => void
  eatFish: () => void // depends on FishSlice
}

interface FishSlice {
  fishes: number
  addFish: () => void
}

// Type the full store in StateCreator
const createBearSlice: StateCreator<
  BearSlice & FishSlice, // Full store type
  [],
  [],
  BearSlice // This slice's type
> = (set) => ({
  bears: 0,
  addBear: () => set((state) => ({ bears: state.bears + 1 })),
  eatFish: () => set((state) => ({ fishes: state.fishes - 1 })),
})

const createFishSlice: StateCreator<
  BearSlice & FishSlice,
  [],
  [],
  FishSlice
> = (set) => ({
  fishes: 0,
  addFish: () => set((state) => ({ fishes: state.fishes + 1 })),
})
```

### Shared Actions

Create a shared slice for cross-cutting concerns:

```ts
interface SharedSlice {
  addBoth: () => void
  getBoth: () => number
}

const createSharedSlice: StateCreator<
  BearSlice & FishSlice & SharedSlice,
  [],
  [],
  SharedSlice
> = (set, get) => ({
  addBoth: () => {
    get().addBear()
    get().addFish()
  },
  getBoth: () => get().bears + get().fishes,
})

// Combine all slices
const useBoundStore = create<BearSlice & FishSlice & SharedSlice>()(
  (...a) => ({
    ...createBearSlice(...a),
    ...createFishSlice(...a),
    ...createSharedSlice(...a),
  }),
)
```

---

## With Middleware

### Persist Middleware

```ts
import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { createBearSlice } from './bearSlice'
import { createFishSlice } from './fishSlice'

export const useBoundStore = create<BearSlice & FishSlice>()(
  persist(
    (...a) => ({
      ...createBearSlice(...a),
      ...createFishSlice(...a),
    }),
    { name: 'bound-store' },
  ),
)
```

### Devtools with Named Actions

```ts
import { create, StateCreator } from 'zustand'
import { devtools } from 'zustand/middleware'

interface BearSlice {
  bears: number
  addBear: () => void
}

const createBearSlice: StateCreator<
  BearSlice,
  [['zustand/devtools', never]],
  [],
  BearSlice
> = (set) => ({
  bears: 0,
  addBear: () =>
    set((state) => ({ bears: state.bears + 1 }), false, 'bear/addBear'),
})

const useBoundStore = create<BearSlice>()(
  devtools(
    (...a) => ({
      ...createBearSlice(...a),
    }),
    { name: 'BoundStore' },
  ),
)
```

---

## File Organization

Recommended structure:

```
stores/
├── index.ts           # Combined store export
├── bearSlice.ts       # Bear state & actions
├── fishSlice.ts       # Fish state & actions
└── sharedSlice.ts     # Cross-slice actions
```

### Re-export Pattern

```ts
// stores/index.ts
import { create } from 'zustand'
import { createBearSlice, BearSlice } from './bearSlice'
import { createFishSlice, FishSlice } from './fishSlice'

type Store = BearSlice & FishSlice

export const useStore = create<Store>()((...a) => ({
  ...createBearSlice(...a),
  ...createFishSlice(...a),
}))

// Re-export types
export type { BearSlice, FishSlice }
```

---

## TypeScript Best Practices

### StateCreator Generic Parameters

```ts
StateCreator<
  T,      // Full store type (combined slices)
  Mps,    // Middleware mutators (e.g., [['zustand/devtools', never]])
  Mcs,    // Middleware creators
  U       // This slice's type (what this creator returns)
>
```

### Example with Immer

```ts
import { StateCreator } from 'zustand'
import { immer } from 'zustand/middleware/immer'

interface BearSlice {
  bears: number
  addBear: () => void
}

const createBearSlice: StateCreator<
  BearSlice,
  [['zustand/immer', never]],
  [],
  BearSlice
> = (set) => ({
  bears: 0,
  addBear: () =>
    set((state) => {
      state.bears += 1
    }),
})
```

<!--
Source references:
- https://zustand.docs.pmnd.rs/guides/slices-pattern
- https://zustand.docs.pmnd.rs/guides/advanced-typescript
-->
