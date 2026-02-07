---
name: use-effect
description: Side effects, cleanup, dependencies, and lifecycle equivalents
---

# useEffect Hook

`useEffect` lets you synchronize a component with external systems (APIs, subscriptions, DOM, etc.).

## Basic Usage

```jsx
import { useEffect } from 'react'

function Component() {
  useEffect(() => {
    // Effect runs after render
    console.log('Component rendered')
  })
  
  return <div>Hello</div>
}
```

## Dependency Array

### No Dependencies - Runs After Every Render

```jsx
useEffect(() => {
  console.log('Runs after every render')
})
```

### Empty Dependencies - Runs Once on Mount

```jsx
useEffect(() => {
  console.log('Runs only on mount')
}, [])
```

### With Dependencies - Runs When Dependencies Change

```jsx
function Profile({ userId }) {
  const [user, setUser] = useState(null)
  
  useEffect(() => {
    fetchUser(userId).then(setUser)
  }, [userId])  // Re-run when userId changes
  
  return <div>{user?.name}</div>
}
```

---

## Cleanup Function

Return a cleanup function to prevent memory leaks:

```jsx
useEffect(() => {
  // Setup
  const subscription = api.subscribe(data => {
    console.log(data)
  })
  
  // Cleanup
  return () => {
    subscription.unsubscribe()
  }
}, [])
```

### Common Cleanup Patterns

#### Timer Cleanup

```jsx
useEffect(() => {
  const timer = setTimeout(() => {
    console.log('Delayed action')
  }, 1000)
  
  return () => clearTimeout(timer)
}, [])
```

#### Event Listener Cleanup

```jsx
useEffect(() => {
  const handleResize = () => {
    console.log('Window resized')
  }
  
  window.addEventListener('resize', handleResize)
  
  return () => {
    window.removeEventListener('resize', handleResize)
  }
}, [])
```

#### WebSocket/Connection Cleanup

```jsx
useEffect(() => {
  const socket = new WebSocket('ws://localhost:8080')
  
  socket.onmessage = (event) => {
    console.log(event.data)
  }
  
  return () => {
    socket.close()
  }
}, [])
```

---

## Data Fetching

### Basic Pattern

```jsx
function UserProfile({ userId }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  
  useEffect(() => {
    setLoading(true)
    
    fetch(`/api/users/${userId}`)
      .then(response => response.json())
      .then(data => {
        setUser(data)
        setLoading(false)
      })
      .catch(err => {
        setError(err)
        setLoading(false)
      })
  }, [userId])
  
  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>
  
  return <div>{user.name}</div>
}
```

### With Async/Await

```jsx
useEffect(() => {
  let ignore = false
  
  async function fetchData() {
    try {
      const response = await fetch(`/api/users/${userId}`)
      const data = await response.json()
      
      if (!ignore) {
        setUser(data)
      }
    } catch (error) {
      if (!ignore) {
        setError(error)
      }
    }
  }
  
  fetchData()
  
  return () => {
    ignore = true  // Prevent race conditions
  }
}, [userId])
```

### With AbortController

```jsx
useEffect(() => {
  const controller = new AbortController()
  
  fetch(`/api/users/${userId}`, {
    signal: controller.signal
  })
    .then(response => response.json())
    .then(setUser)
    .catch(error => {
      if (error.name !== 'AbortError') {
        setError(error)
      }
    })
  
  return () => {
    controller.abort()
  }
}, [userId])
```

---

## Lifecycle Equivalents (Class Components)

### componentDidMount

```jsx
useEffect(() => {
  // Runs once after mount
  console.log('Component mounted')
}, [])
```

### componentDidUpdate

```jsx
useEffect(() => {
  // Runs after every update (skip mount with ref)
  console.log('Component updated')
})
```

### componentWillUnmount

```jsx
useEffect(() => {
  return () => {
    // Runs before unmount
    console.log('Component will unmount')
  }
}, [])
```

### Combined Lifecycle

```jsx
useEffect(() => {
  // componentDidMount
  console.log('Mounted')
  
  return () => {
    // componentWillUnmount
    console.log('Will unmount')
  }
}, [])

useEffect(() => {
  // componentDidUpdate (when dependencies change)
  console.log('Props or state updated')
}, [prop1, prop2])
```

---

## Common Patterns

### Debounced Search

```jsx
function SearchInput() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  
  useEffect(() => {
    const timer = setTimeout(() => {
      if (query) {
        fetch(`/api/search?q=${query}`)
          .then(res => res.json())
          .then(setResults)
      }
    }, 500)  // 500ms debounce
    
    return () => clearTimeout(timer)
  }, [query])
  
  return (
    <input 
      value={query}
      onChange={e => setQuery(e.target.value)}
    />
  )
}
```

### Document Title Updates

```jsx
function useDocumentTitle(title) {
  useEffect(() => {
    document.title = title
  }, [title])
}

function Page() {
  useDocumentTitle('My Page - App Name')
  return <div>Content</div>
}
```

### Interval

```jsx
function Timer() {
  const [count, setCount] = useState(0)
  
  useEffect(() => {
    const interval = setInterval(() => {
      setCount(c => c + 1)
    }, 1000)
    
    return () => clearInterval(interval)
  }, [])
  
  return <div>{count} seconds</div>
}
```

---

## Dependencies Best Practices

### Include All Dependencies

```jsx
function Example({ id, name }) {
  const [data, setData] = useState(null)
  
  useEffect(() => {
    // ❌ Missing dependencies
    fetch(`/api/${id}`)
      .then(res => res.json())
      .then(setData)
  }, [])
  
  useEffect(() => {
    // ✅ All dependencies included
    fetch(`/api/${id}?name=${name}`)
      .then(res => res.json())
      .then(setData)
  }, [id, name])
}
```

### Stable Function References

```jsx
function Example() {
  // ❌ Function recreated on every render
  const fetchData = () => {
    fetch('/api/data')
  }
  
  useEffect(() => {
    fetchData()
  }, [fetchData])  // Runs on every render
  
  // ✅ Use useCallback
  const fetchData = useCallback(() => {
    fetch('/api/data')
  }, [])
  
  useEffect(() => {
    fetchData()
  }, [fetchData])  // Runs once
}
```

### Move Logic Inside Effect

```jsx
function Example({ userId }) {
  // ❌ Unnecessary dependency
  const url = `/api/users/${userId}`
  
  useEffect(() => {
    fetch(url)
  }, [url, userId])
  
  // ✅ Move inside effect
  useEffect(() => {
    const url = `/api/users/${userId}`
    fetch(url)
  }, [userId])
}
```

---

## Common Pitfalls

### Infinite Loop

```jsx
function Example() {
  const [count, setCount] = useState(0)
  
  // ❌ Infinite loop - no dependency array
  useEffect(() => {
    setCount(count + 1)
  })
  
  // ❌ Infinite loop - object dependency
  useEffect(() => {
    setUser({ name: 'John' })
  }, [user])  // user is new object every render
  
  // ✅ Correct
  useEffect(() => {
    // Only run on specific condition
    if (someCondition) {
      setCount(c => c + 1)
    }
  }, [someCondition])
}
```

### Stale Closures

```jsx
function Example() {
  const [count, setCount] = useState(0)
  
  useEffect(() => {
    const interval = setInterval(() => {
      // ❌ Stale closure - always logs 0
      console.log(count)
    }, 1000)
    
    return () => clearInterval(interval)
  }, [])
  
  useEffect(() => {
    const interval = setInterval(() => {
      // ✅ Use functional update
      setCount(c => {
        console.log(c)  // Logs current count
        return c + 1
      })
    }, 1000)
    
    return () => clearInterval(interval)
  }, [])
}
```

<!--
Source references:
- https://react.dev/reference/react/useEffect
- https://react.dev/learn/lifecycle-of-reactive-effects
- https://react.dev/learn/synchronizing-with-effects
-->
