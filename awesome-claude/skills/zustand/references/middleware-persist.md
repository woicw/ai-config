---
name: persist
description: Persisting store data to localStorage, sessionStorage, or custom storage
---

# Persist Middleware

The `persist` middleware persists store state to storage (localStorage by default).

## Basic Usage

```ts
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

const useBearStore = create<BearState>()(
  persist(
    (set) => ({
      bears: 0,
      addBear: () => set((state) => ({ bears: state.bears + 1 })),
    }),
    {
      name: 'bear-storage', // unique name (required)
    },
  ),
)
```

## Configuration Options

### Custom Storage

```ts
import { persist, createJSONStorage } from 'zustand/middleware'

const useBearStore = create<BearState>()(
  persist(
    (set) => ({ /* ... */ }),
    {
      name: 'bear-storage',
      storage: createJSONStorage(() => sessionStorage), // default: localStorage
    },
  ),
)
```

### Partial State Persistence

Only persist specific state keys:

```ts
persist(
  (set) => ({
    bears: 0,
    fishes: 0,
    addBear: () => set((s) => ({ bears: s.bears + 1 })),
  }),
  {
    name: 'bear-storage',
    partialize: (state) => ({ bears: state.bears }), // only persist bears
  },
)
```

### State Versioning & Migration

Handle state migrations when schema changes:

```ts
persist(
  (set) => ({ /* ... */ }),
  {
    name: 'bear-storage',
    version: 1, // increment when schema changes
    migrate: (persistedState, version) => {
      if (version === 0) {
        // Migration from version 0 to 1
        (persistedState as any).newField = 'default'
      }
      return persistedState as BearState
    },
  },
)
```

### Merge Strategy

Customize how persisted state merges with initial state:

```ts
persist(
  (set) => ({ /* ... */ }),
  {
    name: 'bear-storage',
    merge: (persistedState, currentState) => ({
      ...currentState,
      ...(persistedState as BearState),
    }),
  },
)
```

---

## SSR & Hydration

### Skip Automatic Hydration

For SSR applications, control hydration timing:

```ts
const useBearStore = create<BearState>()(
  persist(
    (set) => ({ /* ... */ }),
    {
      name: 'bear-storage',
      skipHydration: true, // disable automatic hydration
    },
  ),
)
```

### Manual Hydration

```tsx
import { useEffect } from 'react'
import { useBearStore } from './store'

function App() {
  useEffect(() => {
    useBearStore.persist.rehydrate()
  }, [])

  return <Component />
}
```

### Check Hydration Status

```ts
// Has the store been hydrated?
const hasHydrated = useBearStore.persist.hasHydrated()

// Subscribe to hydration completion
useBearStore.persist.onHydrate((state) => {
  console.log('Hydration started')
})

useBearStore.persist.onFinishHydration((state) => {
  console.log('Hydration finished')
})
```

---

## Persist API

Access persist utilities on the store:

```ts
// Rehydrate from storage
useBearStore.persist.rehydrate()

// Clear persisted state
useBearStore.persist.clearStorage()

// Get storage options
useBearStore.persist.getOptions()

// Set new options
useBearStore.persist.setOptions({ name: 'new-name' })

// Check hydration status
useBearStore.persist.hasHydrated()
```

---

## Custom Storage Engines

### Async Storage (React Native)

```ts
import AsyncStorage from '@react-native-async-storage/async-storage'

const useBearStore = create<BearState>()(
  persist(
    (set) => ({ /* ... */ }),
    {
      name: 'bear-storage',
      storage: createJSONStorage(() => AsyncStorage),
    },
  ),
)
```

### Custom Implementation

```ts
import { StateStorage } from 'zustand/middleware'

const customStorage: StateStorage = {
  getItem: async (name) => {
    return await myAsyncGet(name)
  },
  setItem: async (name, value) => {
    await myAsyncSet(name, value)
  },
  removeItem: async (name) => {
    await myAsyncRemove(name)
  },
}

persist(
  (set) => ({ /* ... */ }),
  {
    name: 'bear-storage',
    storage: createJSONStorage(() => customStorage),
  },
)
```

---

## Combining with Other Middleware

Order matters - persist should wrap the innermost state creator:

```ts
import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'
import { immer } from 'zustand/middleware/immer'

const useBearStore = create<BearState>()(
  devtools(
    persist(
      immer((set) => ({
        bears: 0,
        increase: (by) => set((state) => { state.bears += by }),
      })),
      { name: 'bear-storage' },
    ),
  ),
)
```

<!--
Source references:
- https://zustand.docs.pmnd.rs/integrations/persisting-store-data
- https://zustand.docs.pmnd.rs/middlewares/persist
-->
