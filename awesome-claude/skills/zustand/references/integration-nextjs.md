---
name: nextjs
description: Next.js integration with SSR support and hydration
---

# Next.js Integration

Next.js presents unique challenges for Zustand due to server-side rendering and per-request isolation.

## Key Challenges

1. **Per-request store** - Server handles concurrent requests; stores must be isolated
2. **SSR friendly** - Avoid hydration mismatches between server and client
3. **SPA routing friendly** - Reset stores on route changes if needed
4. **Server caching friendly** - Compatible with Next.js aggressive caching

---

## Setup Pattern

### 1. Create Store Factory

Use `createStore` (not `create`) for SSR:

```ts
// stores/counter-store.ts
import { createStore } from 'zustand/vanilla'

export interface CounterState {
  count: number
}

export interface CounterActions {
  increment: () => void
  decrement: () => void
}

export type CounterStore = CounterState & CounterActions

export const defaultInitState: CounterState = {
  count: 0,
}

export const createCounterStore = (
  initState: CounterState = defaultInitState,
) => {
  return createStore<CounterStore>()((set) => ({
    ...initState,
    increment: () => set((state) => ({ count: state.count + 1 })),
    decrement: () => set((state) => ({ count: state.count - 1 })),
  }))
}
```

### 2. Create Context Provider

```tsx
// providers/counter-store-provider.tsx
'use client'

import { type ReactNode, createContext, useRef, useContext } from 'react'
import { useStore } from 'zustand'

import {
  type CounterStore,
  createCounterStore,
  defaultInitState,
} from '@/stores/counter-store'

export type CounterStoreApi = ReturnType<typeof createCounterStore>

export const CounterStoreContext = createContext<CounterStoreApi | undefined>(
  undefined,
)

export interface CounterStoreProviderProps {
  children: ReactNode
  initialState?: Partial<CounterStore>
}

export const CounterStoreProvider = ({
  children,
  initialState,
}: CounterStoreProviderProps) => {
  const storeRef = useRef<CounterStoreApi | null>(null)
  
  if (!storeRef.current) {
    storeRef.current = createCounterStore({
      ...defaultInitState,
      ...initialState,
    })
  }

  return (
    <CounterStoreContext.Provider value={storeRef.current}>
      {children}
    </CounterStoreContext.Provider>
  )
}

export const useCounterStore = <T,>(
  selector: (store: CounterStore) => T,
): T => {
  const counterStoreContext = useContext(CounterStoreContext)

  if (!counterStoreContext) {
    throw new Error('useCounterStore must be used within CounterStoreProvider')
  }

  return useStore(counterStoreContext, selector)
}
```

### 3. Add Provider to Layout

#### App Router (app/)

```tsx
// app/layout.tsx
import { CounterStoreProvider } from '@/providers/counter-store-provider'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <CounterStoreProvider>{children}</CounterStoreProvider>
      </body>
    </html>
  )
}
```

#### Pages Router (pages/)

```tsx
// pages/_app.tsx
import type { AppProps } from 'next/app'
import { CounterStoreProvider } from '@/providers/counter-store-provider'

export default function App({ Component, pageProps }: AppProps) {
  return (
    <CounterStoreProvider>
      <Component {...pageProps} />
    </CounterStoreProvider>
  )
}
```

### 4. Use in Components

```tsx
// components/Counter.tsx
'use client'

import { useCounterStore } from '@/providers/counter-store-provider'

export function Counter() {
  const count = useCounterStore((state) => state.count)
  const increment = useCounterStore((state) => state.increment)
  const decrement = useCounterStore((state) => state.decrement)

  return (
    <div>
      <span>Count: {count}</span>
      <button onClick={increment}>+</button>
      <button onClick={decrement}>-</button>
    </div>
  )
}
```

---

## Server State Initialization

### Pass Initial State from Server

```tsx
// app/page.tsx
import { CounterStoreProvider } from '@/providers/counter-store-provider'
import { Counter } from '@/components/Counter'

async function getInitialCount() {
  // Fetch from API or database
  return { count: 10 }
}

export default async function Page() {
  const initialState = await getInitialCount()

  return (
    <CounterStoreProvider initialState={initialState}>
      <Counter />
    </CounterStoreProvider>
  )
}
```

---

## Persist Middleware with SSR

### Skip Hydration Pattern

```ts
// stores/bear-store.ts
import { createStore } from 'zustand/vanilla'
import { persist, createJSONStorage } from 'zustand/middleware'

export const createBearStore = () => {
  return createStore<BearStore>()(
    persist(
      (set) => ({
        bears: 0,
        addBear: () => set((state) => ({ bears: state.bears + 1 })),
      }),
      {
        name: 'bear-storage',
        storage: createJSONStorage(() => localStorage),
        skipHydration: true, // Skip automatic hydration
      },
    ),
  )
}
```

### Manual Hydration in Component

```tsx
'use client'

import { useEffect } from 'react'
import { useBearStore } from '@/providers/bear-store-provider'

export function BearCounter() {
  const bears = useBearStore((state) => state.bears)
  const store = useBearStore((state) => state)

  useEffect(() => {
    // Manually rehydrate on client
    useBearStore.persist?.rehydrate()
  }, [])

  return <div>{bears} bears</div>
}
```

---

## Common Patterns

### Route-Level Providers

For route-specific stores:

```tsx
// app/dashboard/layout.tsx
import { DashboardStoreProvider } from '@/providers/dashboard-store-provider'

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <DashboardStoreProvider>
      {children}
    </DashboardStoreProvider>
  )
}
```

### Multiple Stores

```tsx
// app/layout.tsx
export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <UserStoreProvider>
          <ThemeStoreProvider>
            <CartStoreProvider>
              {children}
            </CartStoreProvider>
          </ThemeStoreProvider>
        </UserStoreProvider>
      </body>
    </html>
  )
}
```

---

## Without Provider (Global Store)

For simpler cases where SSR isolation isn't needed:

```ts
// stores/theme-store.ts
import { create } from 'zustand'

export const useThemeStore = create<ThemeState>()((set) => ({
  theme: 'light',
  toggleTheme: () =>
    set((state) => ({ theme: state.theme === 'light' ? 'dark' : 'light' })),
}))
```

**Caution:** Global stores share state across all requests on the server. Only use for client-only state.

<!--
Source references:
- https://zustand.docs.pmnd.rs/guides/nextjs
- https://zustand.docs.pmnd.rs/guides/ssr-and-hydration
-->
