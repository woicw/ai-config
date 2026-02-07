---
name: use-ref
description: DOM refs, mutable values, useImperativeHandle, and forwardRef
---

# useRef Hook

`useRef` creates a mutable reference that persists across renders without triggering re-renders.

## Basic Usage

```jsx
import { useRef } from 'react'

function Component() {
  const ref = useRef(initialValue)
  
  // Access/modify via ref.current
  ref.current = newValue
}
```

---

## DOM References

### Accessing DOM Elements

```jsx
function InputFocus() {
  const inputRef = useRef(null)
  
  const handleFocus = () => {
    inputRef.current.focus()
  }
  
  return (
    <>
      <input ref={inputRef} />
      <button onClick={handleFocus}>Focus Input</button>
    </>
  )
}
```

### Common DOM Operations

```jsx
function VideoPlayer() {
  const videoRef = useRef(null)
  
  return (
    <>
      <video ref={videoRef} src="video.mp4" />
      <button onClick={() => videoRef.current.play()}>Play</button>
      <button onClick={() => videoRef.current.pause()}>Pause</button>
    </>
  )
}
```

### Measuring Elements

```jsx
function MeasureElement() {
  const divRef = useRef(null)
  const [dimensions, setDimensions] = useState({ width: 0, height: 0 })
  
  useEffect(() => {
    if (divRef.current) {
      const { width, height } = divRef.current.getBoundingClientRect()
      setDimensions({ width, height })
    }
  }, [])
  
  return (
    <div ref={divRef}>
      Width: {dimensions.width}, Height: {dimensions.height}
    </div>
  )
}
```

---

## Storing Mutable Values

### Previous Value

```jsx
function Counter() {
  const [count, setCount] = useState(0)
  const prevCountRef = useRef(0)
  
  useEffect(() => {
    prevCountRef.current = count
  })
  
  const prevCount = prevCountRef.current
  
  return (
    <div>
      <p>Current: {count}</p>
      <p>Previous: {prevCount}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  )
}
```

### Timers and Intervals

```jsx
function Stopwatch() {
  const [time, setTime] = useState(0)
  const intervalRef = useRef(null)
  
  const start = () => {
    if (intervalRef.current) return
    
    intervalRef.current = setInterval(() => {
      setTime(t => t + 1)
    }, 1000)
  }
  
  const stop = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current)
      intervalRef.current = null
    }
  }
  
  useEffect(() => {
    return () => stop()  // Cleanup
  }, [])
  
  return (
    <>
      <p>Time: {time}s</p>
      <button onClick={start}>Start</button>
      <button onClick={stop}>Stop</button>
    </>
  )
}
```

### Avoiding Stale Closures

```jsx
function Chat() {
  const [message, setMessage] = useState('')
  const messageRef = useRef('')
  
  useEffect(() => {
    messageRef.current = message
  }, [message])
  
  useEffect(() => {
    const interval = setInterval(() => {
      // Always has latest message
      console.log(messageRef.current)
    }, 1000)
    
    return () => clearInterval(interval)
  }, [])  // Empty deps - no stale closure
  
  return (
    <input
      value={message}
      onChange={e => setMessage(e.target.value)}
    />
  )
}
```

---

## forwardRef

Pass refs from parent to child components:

```jsx
import { forwardRef } from 'react'

const MyInput = forwardRef((props, ref) => {
  return <input ref={ref} {...props} />
})

function Form() {
  const inputRef = useRef(null)
  
  return (
    <>
      <MyInput ref={inputRef} />
      <button onClick={() => inputRef.current.focus()}>
        Focus Input
      </button>
    </>
  )
}
```

### With TypeScript

```tsx
interface InputProps {
  placeholder?: string
}

const MyInput = forwardRef<HTMLInputElement, InputProps>((props, ref) => {
  return <input ref={ref} {...props} />
})
```

---

## useImperativeHandle

Customize the ref handle exposed to parent components:

```jsx
import { useRef, useImperativeHandle, forwardRef } from 'react'

const MyInput = forwardRef((props, ref) => {
  const inputRef = useRef(null)
  
  useImperativeHandle(ref, () => ({
    focus() {
      inputRef.current.focus()
    },
    scrollIntoView() {
      inputRef.current.scrollIntoView()
    }
  }), [])
  
  return <input ref={inputRef} {...props} />
})

function Form() {
  const inputRef = useRef(null)
  
  return (
    <>
      <MyInput ref={inputRef} />
      <button onClick={() => inputRef.current.focus()}>Focus</button>
      <button onClick={() => inputRef.current.scrollIntoView()}>Scroll</button>
    </>
  )
}
```

### With TypeScript

```tsx
interface InputHandle {
  focus: () => void
  scrollIntoView: () => void
}

const MyInput = forwardRef<InputHandle, {}>((props, ref) => {
  const inputRef = useRef<HTMLInputElement>(null)
  
  useImperativeHandle(ref, () => ({
    focus() {
      inputRef.current?.focus()
    },
    scrollIntoView() {
      inputRef.current?.scrollIntoView()
    }
  }))
  
  return <input ref={inputRef} />
})

function Form() {
  const inputRef = useRef<InputHandle>(null)
  
  return (
    <>
      <MyInput ref={inputRef} />
      <button onClick={() => inputRef.current?.focus()}>Focus</button>
    </>
  )
}
```

---

## Ref Callback

Use a function for dynamic refs:

```jsx
function DynamicList({ items }) {
  const itemsRef = useRef(new Map())
  
  return (
    <ul>
      {items.map(item => (
        <li
          key={item.id}
          ref={node => {
            if (node) {
              itemsRef.current.set(item.id, node)
            } else {
              itemsRef.current.delete(item.id)
            }
          }}
        >
          {item.text}
        </li>
      ))}
    </ul>
  )
}
```

---

## Common Patterns

### Scroll to Bottom

```jsx
function ChatMessages({ messages }) {
  const bottomRef = useRef(null)
  
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])
  
  return (
    <div>
      {messages.map(msg => (
        <div key={msg.id}>{msg.text}</div>
      ))}
      <div ref={bottomRef} />
    </div>
  )
}
```

### Click Outside

```jsx
function Dropdown() {
  const [isOpen, setIsOpen] = useState(false)
  const dropdownRef = useRef(null)
  
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false)
      }
    }
    
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])
  
  return (
    <div ref={dropdownRef}>
      <button onClick={() => setIsOpen(!isOpen)}>Toggle</button>
      {isOpen && <div>Dropdown content</div>}
    </div>
  )
}
```

### Debounced Input

```jsx
function SearchInput() {
  const [value, setValue] = useState('')
  const [searchTerm, setSearchTerm] = useState('')
  const timerRef = useRef(null)
  
  const handleChange = (e) => {
    setValue(e.target.value)
    
    if (timerRef.current) {
      clearTimeout(timerRef.current)
    }
    
    timerRef.current = setTimeout(() => {
      setSearchTerm(e.target.value)
    }, 500)
  }
  
  return (
    <div>
      <input value={value} onChange={handleChange} />
      <p>Searching for: {searchTerm}</p>
    </div>
  )
}
```

---

## useRef vs useState

| useRef | useState |
|--------|----------|
| Doesn't trigger re-render | Triggers re-render |
| Mutable (`.current`) | Immutable (via setter) |
| Can update synchronously | Updates are batched |
| Use for DOM refs, timers | Use for UI state |
| Value persists | Value persists |

---

## Best Practices

### Don't Read/Write During Render

```jsx
function Component() {
  const ref = useRef(0)
  
  // ❌ Bad - reading during render
  const value = ref.current
  
  // ❌ Bad - writing during render
  ref.current = ref.current + 1
  
  // ✅ Good - read/write in event handler
  const handleClick = () => {
    ref.current = ref.current + 1
    console.log(ref.current)
  }
  
  // ✅ Good - read/write in effect
  useEffect(() => {
    ref.current = 0
  }, [])
}
```

### Use Refs for Non-Render Data

```jsx
// ✅ Good - doesn't affect rendering
const timerRef = useRef(null)
const countRef = useRef(0)

// ❌ Bad - use useState instead
const [timer, setTimer] = useState(null)
```

<!--
Source references:
- https://react.dev/reference/react/useRef
- https://react.dev/reference/react/forwardRef
- https://react.dev/reference/react/useImperativeHandle
-->
