---
name: performance-hooks
description: React Compiler, useMemo, useCallback, React.memo, and optimization patterns
---

# Performance Optimization

React provides automatic optimization through React Compiler and manual optimization hooks.

## React Compiler (Recommended)

React Compiler automatically optimizes components, reducing the need for manual `useMemo`, `useCallback`, and `React.memo`.

### Setup

#### Install

```bash
npm install babel-plugin-react-compiler
```

#### Vite Configuration

```js
// vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { reactCompiler } from 'babel-plugin-react-compiler'

export default defineConfig({
  plugins: [
    react({
      babel: {
        plugins: [reactCompiler],
      },
    }),
  ],
})
```

#### Next.js Configuration

```js
// next.config.js
const { reactCompiler } = require('babel-plugin-react-compiler')

module.exports = {
  experimental: {
    reactCompiler: true, // Built-in support in Next.js 15+
  },
}
```

#### Webpack/Babel Configuration

```js
// babel.config.js
import { reactCompiler } from 'babel-plugin-react-compiler'

export default {
  plugins: [
    reactCompiler,
  ],
}
```

### How It Works

React Compiler automatically:
- Memoizes expensive computations
- Stabilizes function references
- Prevents unnecessary re-renders
- Optimizes component updates

**You can write code naturally without manual optimization:**

```jsx
// ✅ No need for useMemo/useCallback - React Compiler handles it
function ProductList({ products, filter }) {
  // Automatically memoized by compiler
  const filteredProducts = products.filter(p => p.category === filter)
  
  // Automatically memoized by compiler
  const handleAdd = (product) => {
    addToCart(product)
  }
  
  return (
    <ul>
      {filteredProducts.map(product => (
        <ProductCard 
          key={product.id}
          product={product}
          onAdd={handleAdd}
        />
      ))}
    </ul>
  )
}
```

### When React Compiler Optimizes

The compiler automatically optimizes:
- ✅ Expensive computations
- ✅ Function references passed as props
- ✅ Object/array props
- ✅ Component re-renders
- ✅ Context values

### When Manual Optimization Is Still Needed

Even with React Compiler, you may need manual optimization for:

#### 1. useEffect Dependencies

```jsx
// ✅ Still need useCallback for useEffect dependencies
function Component({ userId }) {
  const fetchUser = useCallback(async () => {
    const user = await api.getUser(userId)
    setUser(user)
  }, [userId])
  
  useEffect(() => {
    fetchUser()
  }, [fetchUser]) // Stable reference needed
}
```

#### 2. Third-Party Library Props

```jsx
// ✅ Some libraries require stable references
import { SomeLibrary } from 'third-party'

function Component() {
  const config = useMemo(() => ({
    option1: value1,
    option2: value2
  }), [value1, value2])
  
  return <SomeLibrary config={config} />
}
```

#### 3. Custom Comparison Logic

```jsx
// ✅ React.memo with custom comparison
const MyComponent = memo(
  function MyComponent({ items }) {
    return <div>{items.length} items</div>
  },
  (prevProps, nextProps) => {
    // Custom comparison logic
    return prevProps.items.length === nextProps.items.length
  }
)
```

#### 4. Legacy Codebases

For codebases not yet migrated to React Compiler, continue using manual optimizations.

### Migration Example

**Before (Manual Optimization):**

```jsx
import { useMemo, useCallback, memo } from 'react'

const ProductCard = memo(function ProductCard({ product, onAdd }) {
  return (
    <div>
      <h3>{product.name}</h3>
      <button onClick={() => onAdd(product)}>Add</button>
    </div>
  )
})

function ProductList({ products, filter }) {
  const filteredProducts = useMemo(() => {
    return products.filter(p => p.category === filter)
  }, [products, filter])
  
  const handleAdd = useCallback((product) => {
    addToCart(product)
  }, [])
  
  return (
    <ul>
      {filteredProducts.map(product => (
        <ProductCard 
          key={product.id}
          product={product}
          onAdd={handleAdd}
        />
      ))}
    </ul>
  )
}
```

**After (With React Compiler):**

```jsx
// ✅ React Compiler handles optimizations automatically
function ProductCard({ product, onAdd }) {
  return (
    <div>
      <h3>{product.name}</h3>
      <button onClick={() => onAdd(product)}>Add</button>
    </div>
  )
}

function ProductList({ products, filter }) {
  // Automatically memoized by compiler
  const filteredProducts = products.filter(p => p.category === filter)
  
  // Automatically memoized by compiler
  const handleAdd = (product) => {
    addToCart(product)
  }
  
  return (
    <ul>
      {filteredProducts.map(product => (
        <ProductCard 
          key={product.id}
          product={product}
          onAdd={handleAdd}
        />
      ))}
    </ul>
  )
}
```

### Migration Strategy

1. **Enable React Compiler** in your build configuration
2. **Test thoroughly** - verify behavior matches before/after
3. **Remove manual optimizations** gradually, starting with simple cases
4. **Keep manual optimizations** only for:
   - External system synchronization (useEffect dependencies)
   - Third-party library compatibility issues
   - Complex custom comparison logic
5. **Monitor performance** - use React DevTools Profiler to verify improvements

---

## Manual Optimization Hooks

When React Compiler is not available or for specific cases, use these hooks:

## useMemo

Memoize expensive computations:

```jsx
import { useMemo } from 'react'

function ProductList({ products, filter }) {
  const filteredProducts = useMemo(() => {
    console.log('Filtering products...')
    return products.filter(p => p.category === filter)
  }, [products, filter])
  
  return (
    <ul>
      {filteredProducts.map(p => (
        <li key={p.id}>{p.name}</li>
      ))}
    </ul>
  )
}
```

### Syntax

```jsx
const memoizedValue = useMemo(() => computeExpensiveValue(a, b), [a, b])
```

---

## useCallback

Memoize function references:

```jsx
import { useCallback } from 'react'

function Parent() {
  const [count, setCount] = useState(0)
  
  // Without useCallback - new function on every render
  const handleClick = () => {
    setCount(count + 1)
  }
  
  // With useCallback - same function reference
  const handleClickMemo = useCallback(() => {
    setCount(c => c + 1)
  }, [])
  
  return <Child onClick={handleClickMemo} />
}
```

### Syntax

```jsx
const memoizedCallback = useCallback(() => {
  doSomething(a, b)
}, [a, b])
```

---

## React.memo

Prevent unnecessary component re-renders:

```jsx
import { memo } from 'react'

const ExpensiveComponent = memo(function ExpensiveComponent({ data }) {
  console.log('Rendering ExpensiveComponent')
  return <div>{data}</div>
})

function Parent() {
  const [count, setCount] = useState(0)
  const [data, setData] = useState('Hello')
  
  return (
    <>
      <button onClick={() => setCount(count + 1)}>Count: {count}</button>
      {/* Only re-renders when data changes */}
      <ExpensiveComponent data={data} />
    </>
  )
}
```

### With Custom Comparison

```jsx
const MyComponent = memo(
  function MyComponent({ items }) {
    return <div>{items.length} items</div>
  },
  (prevProps, nextProps) => {
    // Return true if props are equal (skip re-render)
    return prevProps.items.length === nextProps.items.length
  }
)
```

---

## When to Use

### useMemo

Use when:
- Computation is expensive
- Value is used in dependency arrays
- Value is passed as prop to memoized component

```jsx
function TodoList({ todos, filter }) {
  // ✅ Good - expensive computation
  const sortedTodos = useMemo(() => {
    return [...todos].sort((a, b) => 
      a.priority - b.priority
    )
  }, [todos])
  
  // ❌ Bad - simple computation
  const count = useMemo(() => todos.length, [todos])
  
  // ✅ Better - just use directly
  const count = todos.length
}
```

### useCallback

Use when:
- Function is passed to memoized child component
- Function is in dependency array of useEffect/useMemo
- Function is used in event handlers with frequent re-renders

```jsx
function Parent() {
  const [count, setCount] = useState(0)
  
  // ✅ Good - passed to memoized child
  const handleSubmit = useCallback((data) => {
    api.submit(data)
  }, [])
  
  return <MemoizedForm onSubmit={handleSubmit} />
}
```

---

## Optimization Patterns

### Stabilize Object/Array Props

```jsx
function ProductPage({ productId, referrer }) {
  // ❌ Bad - new object on every render
  const product = useData('/product/' + productId)
  const options = { productId, referrer }
  
  return <ShippingForm options={options} />
  
  // ✅ Good - memoize object
  const options = useMemo(() => ({
    productId,
    referrer
  }), [productId, referrer])
  
  return <ShippingForm options={options} />
}
```

### Optimize Context

```jsx
function MyProvider({ children }) {
  const [state, setState] = useState({})
  
  // ❌ Bad - new object every render
  const value = { state, setState }
  
  // ✅ Good - memoize context value
  const value = useMemo(() => ({
    state,
    setState
  }), [state])
  
  return (
    <MyContext.Provider value={value}>
      {children}
    </MyContext.Provider>
  )
}
```

### Separate State and Actions

```jsx
const StateContext = createContext(null)
const ActionsContext = createContext(null)

function Provider({ children }) {
  const [state, setState] = useState({})
  
  // Actions don't change
  const actions = useMemo(() => ({
    update: (data) => setState(data),
    reset: () => setState({})
  }), [])
  
  return (
    <StateContext.Provider value={state}>
      <ActionsContext.Provider value={actions}>
        {children}
      </ActionsContext.Provider>
    </StateContext.Provider>
  )
}
```

---

## Complete Example

```jsx
import { memo, useMemo, useCallback, useState } from 'react'

// Memoized child component
const ProductCard = memo(function ProductCard({ product, onAdd }) {
  console.log('Rendering ProductCard:', product.id)
  
  return (
    <div>
      <h3>{product.name}</h3>
      <p>${product.price}</p>
      <button onClick={() => onAdd(product)}>Add to Cart</button>
    </div>
  )
})

function ProductList({ products, category }) {
  const [cart, setCart] = useState([])
  
  // Memoize filtered products
  const filteredProducts = useMemo(() => {
    console.log('Filtering products...')
    return products.filter(p => p.category === category)
  }, [products, category])
  
  // Memoize sorted products
  const sortedProducts = useMemo(() => {
    console.log('Sorting products...')
    return [...filteredProducts].sort((a, b) => a.price - b.price)
  }, [filteredProducts])
  
  // Memoize callback
  const handleAddToCart = useCallback((product) => {
    setCart(prev => [...prev, product])
  }, [])
  
  // Memoize cart total
  const cartTotal = useMemo(() => {
    return cart.reduce((sum, item) => sum + item.price, 0)
  }, [cart])
  
  return (
    <div>
      <p>Cart Total: ${cartTotal}</p>
      <div>
        {sortedProducts.map(product => (
          <ProductCard
            key={product.id}
            product={product}
            onAdd={handleAddToCart}
          />
        ))}
      </div>
    </div>
  )
}
```

---

## Common Pitfalls

### Over-optimization

```jsx
// ❌ Bad - unnecessary memoization
const count = useMemo(() => items.length, [items])
const double = useMemo(() => count * 2, [count])
const message = useMemo(() => `Count: ${count}`, [count])

// ✅ Good - simple calculations
const count = items.length
const double = count * 2
const message = `Count: ${count}`
```

### Unstable Dependencies

```jsx
function Component({ config }) {
  // ❌ Bad - config is new object every render
  const processedData = useMemo(() => {
    return processData(config)
  }, [config])
  
  // ✅ Good - destructure needed values
  const { apiUrl, timeout } = config
  const processedData = useMemo(() => {
    return processData({ apiUrl, timeout })
  }, [apiUrl, timeout])
}
```

### Wrong Hook

```jsx
function Component() {
  // ❌ Bad - useMemo for function
  const handleClick = useMemo(() => {
    return () => console.log('clicked')
  }, [])
  
  // ✅ Good - useCallback for function
  const handleClick = useCallback(() => {
    console.log('clicked')
  }, [])
}
```

---

## Profiling and Debugging

### React DevTools Profiler

```jsx
import { Profiler } from 'react'

function onRenderCallback(
  id,
  phase,
  actualDuration,
  baseDuration,
  startTime,
  commitTime
) {
  console.log(`${id} (${phase}) took ${actualDuration}ms`)
}

function App() {
  return (
    <Profiler id="ProductList" onRender={onRenderCallback}>
      <ProductList />
    </Profiler>
  )
}
```

### Log Renders

```jsx
function useRenderCount(componentName) {
  const renderCount = useRef(0)
  
  useEffect(() => {
    renderCount.current += 1
    console.log(`${componentName} rendered ${renderCount.current} times`)
  })
}

function MyComponent() {
  useRenderCount('MyComponent')
  // ...
}
```

---

## Best Practices

### With React Compiler

1. **Enable React Compiler** - Let it handle automatic optimizations
2. **Write code naturally** - No need for manual useMemo/useCallback in most cases
3. **Measure performance** - Use React DevTools Profiler to verify optimizations
4. **Keep manual optimizations** only for edge cases compiler can't handle
5. **Use production builds** - Compiler optimizations are most effective in production

### Without React Compiler

1. **Measure first** - Don't optimize prematurely
2. **Start without memoization** - Add only when needed
3. **Use React DevTools Profiler** to find bottlenecks
4. **Memoize expensive computations** not cheap ones
5. **Include all dependencies** in dependency arrays
6. **Consider code splitting** for large components
7. **Use production builds** for accurate performance testing

---

## Performance Checklist

### With React Compiler

- [ ] React Compiler enabled in build configuration
- [ ] Verified compiler optimizations in production build
- [ ] Removed unnecessary manual optimizations
- [ ] Identified slow renders with Profiler
- [ ] Kept manual optimizations only where needed
- [ ] Split large components
- [ ] Lazy load routes/components

### Without React Compiler

- [ ] Identified slow renders with Profiler
- [ ] Used React.memo for expensive components
- [ ] Memoized callbacks passed to children
- [ ] Memoized expensive computations
- [ ] Optimized context re-renders
- [ ] Split large components
- [ ] Lazy load routes/components
- [ ] Verified in production build

<!--
Source references:
- https://react.dev/reference/react/useMemo
- https://react.dev/reference/react/useCallback
- https://react.dev/reference/react/memo
-->
