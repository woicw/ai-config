---
name: react-state-management
description: useState hook, state updates, batching, and functional updates
---

# State Management with useState

The `useState` hook lets components "remember" values between renders.

## Basic Usage

```jsx
import { useState } from 'react'

function Counter() {
  const [count, setCount] = useState(0)
  
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  )
}
```

## State Declaration

### Primitive Values

```jsx
const [count, setCount] = useState(0)
const [name, setName] = useState('John')
const [isActive, setIsActive] = useState(false)
```

### Objects

```jsx
const [user, setUser] = useState({
  name: 'John',
  age: 30,
  email: 'john@example.com'
})
```

### Arrays

```jsx
const [items, setItems] = useState([])
const [todos, setTodos] = useState([
  { id: 1, text: 'Learn React', done: false }
])
```

### Lazy Initialization

Expensive initial state should be computed only once:

```jsx
// ❌ Bad - runs on every render
const [data, setData] = useState(expensiveComputation())

// ✅ Good - runs only on mount
const [data, setData] = useState(() => expensiveComputation())
```

---

## Updating State

### Direct Updates

```jsx
function Example() {
  const [count, setCount] = useState(0)
  
  const increment = () => {
    setCount(count + 1)
  }
  
  return <button onClick={increment}>Count: {count}</button>
}
```

### Functional Updates (Recommended for Updates Based on Previous State)

```jsx
function Counter() {
  const [count, setCount] = useState(0)
  
  const increment = () => {
    // ✅ Use updater function
    setCount(prevCount => prevCount + 1)
  }
  
  const incrementByThree = () => {
    // ✅ Each update uses latest state
    setCount(c => c + 1)
    setCount(c => c + 1)
    setCount(c => c + 1)
  }
  
  return (
    <>
      <p>Count: {count}</p>
      <button onClick={increment}>+1</button>
      <button onClick={incrementByThree}>+3</button>
    </>
  )
}
```

### Why Functional Updates Matter

```jsx
function Counter() {
  const [count, setCount] = useState(0)
  
  const handleClick = () => {
    // ❌ All three use the same count value (0)
    // Result: count becomes 1, not 3
    setCount(count + 1)  // setCount(0 + 1)
    setCount(count + 1)  // setCount(0 + 1)
    setCount(count + 1)  // setCount(0 + 1)
  }
  
  const handleClickCorrect = () => {
    // ✅ Each uses the result of the previous update
    // Result: count becomes 3
    setCount(c => c + 1)  // setCount(0 => 1)
    setCount(c => c + 1)  // setCount(1 => 2)
    setCount(c => c + 1)  // setCount(2 => 3)
  }
  
  return <button onClick={handleClickCorrect}>Count: {count}</button>
}
```

---

## Updating Objects

Objects must be replaced, not mutated:

```jsx
function Form() {
  const [user, setUser] = useState({
    name: 'John',
    age: 30
  })
  
  // ❌ Wrong - mutates state
  const updateAge = () => {
    user.age = 31
    setUser(user)
  }
  
  // ✅ Correct - creates new object
  const updateAge = () => {
    setUser({
      ...user,
      age: 31
    })
  }
  
  // ✅ With functional update
  const updateAge = () => {
    setUser(prevUser => ({
      ...prevUser,
      age: prevUser.age + 1
    }))
  }
  
  return (
    <div>
      <p>{user.name}, {user.age}</p>
      <button onClick={updateAge}>Birthday</button>
    </div>
  )
}
```

### Nested Objects

```jsx
function Profile() {
  const [user, setUser] = useState({
    name: 'John',
    address: {
      city: 'New York',
      zip: '10001'
    }
  })
  
  const updateCity = (newCity) => {
    setUser({
      ...user,
      address: {
        ...user.address,
        city: newCity
      }
    })
  }
  
  return <button onClick={() => updateCity('Boston')}>Move to Boston</button>
}
```

---

## Updating Arrays

### Adding Items

```jsx
function TodoList() {
  const [todos, setTodos] = useState([])
  
  const addTodo = (text) => {
    // ✅ Create new array with spread
    setTodos([...todos, { id: Date.now(), text, done: false }])
    
    // ✅ Or use concat
    setTodos(todos.concat({ id: Date.now(), text, done: false }))
  }
}
```

### Removing Items

```jsx
const removeTodo = (id) => {
  setTodos(todos.filter(todo => todo.id !== id))
}
```

### Updating Items

```jsx
const toggleTodo = (id) => {
  setTodos(todos.map(todo =>
    todo.id === id
      ? { ...todo, done: !todo.done }
      : todo
  ))
}
```

### Sorting

```jsx
const sortTodos = () => {
  // ❌ Wrong - sort mutates array
  setTodos(todos.sort((a, b) => a.text.localeCompare(b.text)))
  
  // ✅ Correct - create copy first
  setTodos([...todos].sort((a, b) => a.text.localeCompare(b.text)))
}
```

---

## State Batching

React automatically batches multiple state updates in event handlers:

```jsx
function Example() {
  const [count, setCount] = useState(0)
  const [flag, setFlag] = useState(false)
  
  const handleClick = () => {
    // Both updates batched - only one re-render
    setCount(c => c + 1)
    setFlag(f => !f)
  }
  
  return <button onClick={handleClick}>Update</button>
}
```

### In React 18+

Automatic batching also works in async code:

```jsx
const handleClick = async () => {
  await fetch('/api/data')
  
  // Both updates batched - only one re-render
  setCount(c => c + 1)
  setFlag(f => !f)
}
```

---

## Multiple State Variables

### Separate State

```jsx
function Form() {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [age, setAge] = useState(0)
  
  return (
    <form>
      <input value={name} onChange={e => setName(e.target.value)} />
      <input value={email} onChange={e => setEmail(e.target.value)} />
      <input value={age} onChange={e => setAge(Number(e.target.value))} />
    </form>
  )
}
```

### Single State Object

```jsx
function Form() {
  const [form, setForm] = useState({
    name: '',
    email: '',
    age: 0
  })
  
  const updateField = (field, value) => {
    setForm(prev => ({
      ...prev,
      [field]: value
    }))
  }
  
  return (
    <form>
      <input 
        value={form.name} 
        onChange={e => updateField('name', e.target.value)} 
      />
      <input 
        value={form.email} 
        onChange={e => updateField('email', e.target.value)} 
      />
      <input 
        value={form.age} 
        onChange={e => updateField('age', Number(e.target.value))} 
      />
    </form>
  )
}
```

---

## Resetting State

### With Key Prop

```jsx
function ProfilePage({ userId }) {
  return <Profile key={userId} userId={userId} />
}

function Profile({ userId }) {
  const [data, setData] = useState(null)
  // When userId changes, key changes, component remounts with fresh state
}
```

### Manual Reset

```jsx
function Form() {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  
  const reset = () => {
    setName('')
    setEmail('')
  }
  
  return (
    <form>
      <input value={name} onChange={e => setName(e.target.value)} />
      <input value={email} onChange={e => setEmail(e.target.value)} />
      <button type="button" onClick={reset}>Reset</button>
    </form>
  )
}
```

---

## State vs Props

| State | Props |
|-------|-------|
| Owned by component | Passed from parent |
| Mutable (via setState) | Read-only |
| Can be changed | Cannot be changed |
| Used for dynamic data | Used for configuration |

<!--
Source references:
- https://react.dev/reference/react/useState
- https://react.dev/learn/queueing-a-series-of-state-updates
- https://react.dev/learn/updating-objects-in-state
- https://react.dev/learn/updating-arrays-in-state
-->
