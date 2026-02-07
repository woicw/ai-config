---
name: custom-hooks
description: Creating reusable custom hooks for stateful logic
---

# Custom Hooks

Custom hooks let you extract component logic into reusable functions. They follow the "use" naming convention and can use other hooks.

## Basic Custom Hook

```jsx
import { useState, useEffect } from 'react'

function useWindowWidth() {
  const [width, setWidth] = useState(window.innerWidth)
  
  useEffect(() => {
    const handleResize = () => setWidth(window.innerWidth)
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])
  
  return width
}

// Usage
function Component() {
  const width = useWindowWidth()
  return <div>Window width: {width}px</div>
}
```

---

## Naming Convention

- **Must** start with "use"
- **Should** describe what it does
- Use camelCase

```jsx
// ✅ Good
useUser()
useAuth()
useFetch()
useLocalStorage()
useDebounce()

// ❌ Bad
getUser()      // Doesn't start with "use"
userData()     // Doesn't start with "use"
use_auth()     // Wrong case
```

---

## Data Fetching Hook

```jsx
function useFetch(url) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  
  useEffect(() => {
    let ignore = false
    
    setLoading(true)
    
    fetch(url)
      .then(response => response.json())
      .then(json => {
        if (!ignore) {
          setData(json)
          setLoading(false)
        }
      })
      .catch(error => {
        if (!ignore) {
          setError(error)
          setLoading(false)
        }
      })
    
    return () => {
      ignore = true
    }
  }, [url])
  
  return { data, loading, error }
}

// Usage
function UserProfile({ userId }) {
  const { data: user, loading, error } = useFetch(`/api/users/${userId}`)
  
  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>
  
  return <div>{user.name}</div>
}
```

---

## Local Storage Hook

```jsx
function useLocalStorage(key, initialValue) {
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key)
      return item ? JSON.parse(item) : initialValue
    } catch (error) {
      console.log(error)
      return initialValue
    }
  })
  
  const setValue = (value) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value
      setStoredValue(valueToStore)
      window.localStorage.setItem(key, JSON.stringify(valueToStore))
    } catch (error) {
      console.log(error)
    }
  }
  
  return [storedValue, setValue]
}

// Usage
function Settings() {
  const [theme, setTheme] = useLocalStorage('theme', 'light')
  
  return (
    <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
      Current theme: {theme}
    </button>
  )
}
```

---

## Debounce Hook

```jsx
function useDebounce(value, delay) {
  const [debouncedValue, setDebouncedValue] = useState(value)
  
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValue(value)
    }, delay)
    
    return () => {
      clearTimeout(timer)
    }
  }, [value, delay])
  
  return debouncedValue
}

// Usage
function SearchInput() {
  const [searchTerm, setSearchTerm] = useState('')
  const debouncedSearchTerm = useDebounce(searchTerm, 500)
  
  useEffect(() => {
    if (debouncedSearchTerm) {
      // API call
      fetch(`/api/search?q=${debouncedSearchTerm}`)
    }
  }, [debouncedSearchTerm])
  
  return (
    <input
      value={searchTerm}
      onChange={e => setSearchTerm(e.target.value)}
    />
  )
}
```

---

## Previous Value Hook

```jsx
function usePrevious(value) {
  const ref = useRef()
  
  useEffect(() => {
    ref.current = value
  }, [value])
  
  return ref.current
}

// Usage
function Counter() {
  const [count, setCount] = useState(0)
  const prevCount = usePrevious(count)
  
  return (
    <div>
      <p>Current: {count}</p>
      <p>Previous: {prevCount}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  )
}
```

---

## Toggle Hook

```jsx
function useToggle(initialValue = false) {
  const [value, setValue] = useState(initialValue)
  
  const toggle = useCallback(() => {
    setValue(v => !v)
  }, [])
  
  return [value, toggle]
}

// Usage
function Modal() {
  const [isOpen, toggleOpen] = useToggle(false)
  
  return (
    <>
      <button onClick={toggleOpen}>Open Modal</button>
      {isOpen && (
        <div className="modal">
          <button onClick={toggleOpen}>Close</button>
        </div>
      )}
    </>
  )
}
```

---

## Media Query Hook

```jsx
function useMediaQuery(query) {
  const [matches, setMatches] = useState(() => {
    return window.matchMedia(query).matches
  })
  
  useEffect(() => {
    const mediaQuery = window.matchMedia(query)
    const handler = (event) => setMatches(event.matches)
    
    mediaQuery.addEventListener('change', handler)
    return () => mediaQuery.removeEventListener('change', handler)
  }, [query])
  
  return matches
}

// Usage
function ResponsiveComponent() {
  const isMobile = useMediaQuery('(max-width: 768px)')
  
  return (
    <div>
      {isMobile ? <MobileView /> : <DesktopView />}
    </div>
  )
}
```

---

## Async Hook

```jsx
function useAsync(asyncFunction, immediate = true) {
  const [status, setStatus] = useState('idle')
  const [value, setValue] = useState(null)
  const [error, setError] = useState(null)
  
  const execute = useCallback(() => {
    setStatus('pending')
    setValue(null)
    setError(null)
    
    return asyncFunction()
      .then(response => {
        setValue(response)
        setStatus('success')
      })
      .catch(error => {
        setError(error)
        setStatus('error')
      })
  }, [asyncFunction])
  
  useEffect(() => {
    if (immediate) {
      execute()
    }
  }, [execute, immediate])
  
  return { execute, status, value, error }
}

// Usage
function UserProfile({ userId }) {
  const { status, value: user, error } = useAsync(
    () => fetch(`/api/users/${userId}`).then(r => r.json()),
    true
  )
  
  if (status === 'pending') return <div>Loading...</div>
  if (status === 'error') return <div>Error: {error.message}</div>
  
  return <div>{user.name}</div>
}
```

---

## Interval Hook

```jsx
function useInterval(callback, delay) {
  const savedCallback = useRef()
  
  useEffect(() => {
    savedCallback.current = callback
  }, [callback])
  
  useEffect(() => {
    if (delay !== null) {
      const id = setInterval(() => savedCallback.current(), delay)
      return () => clearInterval(id)
    }
  }, [delay])
}

// Usage
function Timer() {
  const [count, setCount] = useState(0)
  
  useInterval(() => {
    setCount(count + 1)
  }, 1000)
  
  return <div>Count: {count}</div>
}
```

---

## Form Hook

```jsx
function useForm(initialValues) {
  const [values, setValues] = useState(initialValues)
  const [errors, setErrors] = useState({})
  
  const handleChange = (e) => {
    const { name, value } = e.target
    setValues(prev => ({ ...prev, [name]: value }))
  }
  
  const handleSubmit = (onSubmit, validate) => (e) => {
    e.preventDefault()
    
    if (validate) {
      const validationErrors = validate(values)
      setErrors(validationErrors)
      
      if (Object.keys(validationErrors).length === 0) {
        onSubmit(values)
      }
    } else {
      onSubmit(values)
    }
  }
  
  const reset = () => {
    setValues(initialValues)
    setErrors({})
  }
  
  return {
    values,
    errors,
    handleChange,
    handleSubmit,
    reset
  }
}

// Usage
function ContactForm() {
  const { values, errors, handleChange, handleSubmit, reset } = useForm({
    name: '',
    email: ''
  })
  
  const validate = (values) => {
    const errors = {}
    if (!values.name) errors.name = 'Required'
    if (!values.email) errors.email = 'Required'
    return errors
  }
  
  const onSubmit = (values) => {
    console.log('Submit:', values)
  }
  
  return (
    <form onSubmit={handleSubmit(onSubmit, validate)}>
      <input
        name="name"
        value={values.name}
        onChange={handleChange}
      />
      {errors.name && <span>{errors.name}</span>}
      
      <input
        name="email"
        value={values.email}
        onChange={handleChange}
      />
      {errors.email && <span>{errors.email}</span>}
      
      <button type="submit">Submit</button>
      <button type="button" onClick={reset}>Reset</button>
    </form>
  )
}
```

---

## TypeScript

```tsx
function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)
  
  useEffect(() => {
    let ignore = false
    
    fetch(url)
      .then(response => response.json())
      .then((json: T) => {
        if (!ignore) {
          setData(json)
          setLoading(false)
        }
      })
      .catch((error: Error) => {
        if (!ignore) {
          setError(error)
          setLoading(false)
        }
      })
    
    return () => {
      ignore = true
    }
  }, [url])
  
  return { data, loading, error }
}

// Usage
interface User {
  id: number
  name: string
}

function UserProfile({ userId }: { userId: number }) {
  const { data: user, loading, error } = useFetch<User>(`/api/users/${userId}`)
  
  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>
  
  return <div>{user?.name}</div>
}
```

---

## Best Practices

1. **Name with "use" prefix** - Required for React to recognize as hook
2. **Keep focused** - Each hook should do one thing well
3. **Return arrays for similar values** - `[value, setValue]`
4. **Return objects for different types** - `{ data, loading, error }`
5. **Accept configuration objects** for complex options
6. **Document dependencies** clearly
7. **Handle cleanup** in useEffect returns
8. **Make reusable** but not over-engineered

<!--
Source references:
- https://react.dev/learn/reusing-logic-with-custom-hooks
-->
