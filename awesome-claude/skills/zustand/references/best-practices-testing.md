---
name: testing
description: Unit testing Zustand stores with Jest/Vitest
---

# Testing Stores

## Setting Up Mocks

### Vitest Mock

Create a mock file at `__mocks__/zustand.ts`:

```ts
// __mocks__/zustand.ts
import { act } from '@testing-library/react'
import type * as ZustandExportedTypes from 'zustand'
export * from 'zustand'

const { create: actualCreate, createStore: actualCreateStore } =
  await vi.importActual<typeof ZustandExportedTypes>('zustand')

// Hold reset functions for all stores
export const storeResetFns = new Set<() => void>()

const createUncurried = <T>(
  stateCreator: ZustandExportedTypes.StateCreator<T>,
) => {
  const store = actualCreate(stateCreator)
  const initialState = store.getInitialState()
  storeResetFns.add(() => {
    store.setState(initialState, true)
  })
  return store
}

export const create = (<T>(
  stateCreator: ZustandExportedTypes.StateCreator<T>,
) => {
  console.log('zustand create mock')
  return typeof stateCreator === 'function'
    ? createUncurried(stateCreator)
    : createUncurried
}) as typeof ZustandExportedTypes.create

const createStoreUncurried = <T>(
  stateCreator: ZustandExportedTypes.StateCreator<T>,
) => {
  const store = actualCreateStore(stateCreator)
  const initialState = store.getInitialState()
  storeResetFns.add(() => {
    store.setState(initialState, true)
  })
  return store
}

export const createStore = (<T>(
  stateCreator: ZustandExportedTypes.StateCreator<T>,
) => {
  console.log('zustand createStore mock')
  return typeof stateCreator === 'function'
    ? createStoreUncurried(stateCreator)
    : createStoreUncurried
}) as typeof ZustandExportedTypes.createStore

// Reset all stores after each test
afterEach(() => {
  act(() => {
    storeResetFns.forEach((resetFn) => {
      resetFn()
    })
  })
})
```

### Jest Mock

Same structure but use `jest.requireActual`:

```ts
// __mocks__/zustand.ts
import { act } from '@testing-library/react'
import type * as ZustandExportedTypes from 'zustand'
export * from 'zustand'

const { create: actualCreate, createStore: actualCreateStore } =
  jest.requireActual<typeof ZustandExportedTypes>('zustand')

// ... rest is identical to Vitest mock
```

---

## Basic Unit Tests

### Testing Store Logic

```ts
import { useBearStore } from '../src/stores/bear'

describe('Bear Store', () => {
  it('should initialize with 0 bears', () => {
    const { bears } = useBearStore.getState()
    expect(bears).toBe(0)
  })

  it('should increase bears', () => {
    const { increase } = useBearStore.getState()
    increase(5)
    expect(useBearStore.getState().bears).toBe(5)
  })

  it('should reset state between tests', () => {
    // State is automatically reset by the mock
    expect(useBearStore.getState().bears).toBe(0)
  })
})
```

### Testing Async Actions

```ts
import { useFishStore } from '../src/stores/fish'

describe('Fish Store', () => {
  beforeEach(() => {
    vi.mock('fetch')
  })

  it('should fetch fishes', async () => {
    global.fetch = vi.fn().mockResolvedValue({
      json: () => Promise.resolve([{ id: 1, name: 'Nemo' }]),
    })

    await useFishStore.getState().fetchFishes()

    expect(useFishStore.getState().fishes).toHaveLength(1)
    expect(useFishStore.getState().loading).toBe(false)
  })

  it('should handle fetch errors', async () => {
    global.fetch = vi.fn().mockRejectedValue(new Error('Network error'))

    await useFishStore.getState().fetchFishes()

    expect(useFishStore.getState().error).toBe('Network error')
  })
})
```

---

## Testing Components

### With React Testing Library

```tsx
import { render, screen, fireEvent } from '@testing-library/react'
import { useBearStore } from '../src/stores/bear'
import BearCounter from '../src/components/BearCounter'

describe('BearCounter Component', () => {
  it('should display initial bear count', () => {
    render(<BearCounter />)
    expect(screen.getByText('0 bears')).toBeInTheDocument()
  })

  it('should update when store changes', async () => {
    render(<BearCounter />)

    // Directly update store
    useBearStore.setState({ bears: 5 })

    expect(await screen.findByText('5 bears')).toBeInTheDocument()
  })

  it('should increment on button click', async () => {
    render(<BearCounter />)

    fireEvent.click(screen.getByRole('button', { name: /add/i }))

    expect(await screen.findByText('1 bears')).toBeInTheDocument()
  })
})
```

---

## Setting Initial State

### For Individual Tests

```ts
it('should handle edge case with many bears', () => {
  useBearStore.setState({ bears: 1000 })
  
  const { bears, reset } = useBearStore.getState()
  expect(bears).toBe(1000)
  
  reset()
  expect(useBearStore.getState().bears).toBe(0)
})
```

### With Partial State

```ts
it('should merge state correctly', () => {
  useBearStore.setState({ bears: 5 }) // Merges with existing state
  
  expect(useBearStore.getState().bears).toBe(5)
  expect(useBearStore.getState().food).toBe('honey') // Other state preserved
})
```

---

## Manual Reset Pattern

If not using the mock, reset stores manually:

```ts
import { useBearStore } from '../src/stores/bear'

describe('Bear Store (without mock)', () => {
  beforeEach(() => {
    // Reset to initial state
    useBearStore.setState(useBearStore.getInitialState(), true)
  })

  it('should work with fresh state', () => {
    expect(useBearStore.getState().bears).toBe(0)
  })
})
```

---

## Testing with Middleware

### Persist Middleware

```ts
import { useBearStore } from '../src/stores/bear'

describe('Persisted Store', () => {
  beforeEach(() => {
    localStorage.clear()
  })

  it('should clear persisted data', () => {
    useBearStore.setState({ bears: 10 })
    useBearStore.persist.clearStorage()
    
    expect(localStorage.getItem('bear-storage')).toBeNull()
  })
})
```

### Devtools Middleware

No special handling needed - devtools doesn't affect test behavior.

---

## E2E Tests

For E2E tests with Playwright/Cypress, no special Zustand handling is needed. The store works normally in the browser environment.

<!--
Source references:
- https://zustand.docs.pmnd.rs/guides/testing
-->
