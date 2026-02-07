---
name: use-reducer
description: Complex state management with reducers, actions, and dispatch
---

# useReducer Hook

`useReducer` is an alternative to `useState` for managing complex state logic. It's inspired by Redux patterns.

## Basic Usage

```jsx
import { useReducer } from 'react'

function reducer(state, action) {
  switch (action.type) {
    case 'increment':
      return { count: state.count + 1 }
    case 'decrement':
      return { count: state.count - 1 }
    default:
      throw new Error(`Unknown action: ${action.type}`)
  }
}

function Counter() {
  const [state, dispatch] = useReducer(reducer, { count: 0 })
  
  return (
    <>
      <p>Count: {state.count}</p>
      <button onClick={() => dispatch({ type: 'increment' })}>+</button>
      <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
    </>
  )
}
```

## Syntax

```jsx
const [state, dispatch] = useReducer(reducer, initialArg, init?)
```

- **reducer**: Function that determines how state updates
- **initialArg**: Initial state value
- **init**: Optional lazy initializer function

---

## Reducer Function

### Basic Reducer

```jsx
function reducer(state, action) {
  switch (action.type) {
    case 'added':
      return [...state, { id: action.id, text: action.text }]
    case 'deleted':
      return state.filter(item => item.id !== action.id)
    case 'changed':
      return state.map(item =>
        item.id === action.id ? action.payload : item
      )
    default:
      throw new Error(`Unknown action: ${action.type}`)
  }
}
```

### With Payload

```jsx
function reducer(state, action) {
  switch (action.type) {
    case 'set_name':
      return { ...state, name: action.payload }
    case 'set_age':
      return { ...state, age: action.payload }
    case 'update_profile':
      return { ...state, ...action.payload }
    default:
      return state
  }
}

// Usage
dispatch({ type: 'set_name', payload: 'John' })
dispatch({ type: 'update_profile', payload: { name: 'John', age: 30 } })
```

---

## When to Use useReducer

### Use useState for:

- Simple state (primitives, single objects)
- Independent state variables
- No complex update logic

### Use useReducer for:

- Complex state objects with multiple sub-values
- State transitions depend on previous state
- Related state updates (multiple fields change together)
- Testing reducer logic separately

---

## Todo List Example

```jsx
import { useReducer } from 'react'

function todosReducer(state, action) {
  switch (action.type) {
    case 'added': {
      return [
        ...state,
        {
          id: action.id,
          text: action.text,
          done: false
        }
      ]
    }
    case 'changed': {
      return state.map(todo =>
        todo.id === action.task.id ? action.task : todo
      )
    }
    case 'deleted': {
      return state.filter(todo => todo.id !== action.id)
    }
    case 'toggled': {
      return state.map(todo =>
        todo.id === action.id ? { ...todo, done: !todo.done } : todo
      )
    }
    default: {
      throw new Error('Unknown action: ' + action.type)
    }
  }
}

function TodoApp() {
  const [todos, dispatch] = useReducer(todosReducer, [])
  const [nextId, setNextId] = useState(0)
  
  function handleAddTodo(text) {
    dispatch({
      type: 'added',
      id: nextId,
      text: text
    })
    setNextId(nextId + 1)
  }
  
  function handleChangeTodo(task) {
    dispatch({
      type: 'changed',
      task: task
    })
  }
  
  function handleDeleteTodo(id) {
    dispatch({
      type: 'deleted',
      id: id
    })
  }
  
  function handleToggleTodo(id) {
    dispatch({
      type: 'toggled',
      id: id
    })
  }
  
  return (
    <>
      <AddTodo onAdd={handleAddTodo} />
      <TodoList
        todos={todos}
        onChange={handleChangeTodo}
        onDelete={handleDeleteTodo}
        onToggle={handleToggleTodo}
      />
    </>
  )
}
```

---

## Lazy Initialization

Initialize state lazily with an init function:

```jsx
function init(initialCount) {
  return { count: initialCount }
}

function reducer(state, action) {
  switch (action.type) {
    case 'increment':
      return { count: state.count + 1 }
    case 'decrement':
      return { count: state.count - 1 }
    case 'reset':
      return init(action.payload)
    default:
      throw new Error()
  }
}

function Counter({ initialCount }) {
  const [state, dispatch] = useReducer(reducer, initialCount, init)
  
  return (
    <>
      Count: {state.count}
      <button onClick={() => dispatch({ type: 'reset', payload: initialCount })}>
        Reset
      </button>
      <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
      <button onClick={() => dispatch({ type: 'increment' })}>+</button>
    </>
  )
}
```

---

## Form State Management

```jsx
function formReducer(state, action) {
  switch (action.type) {
    case 'update_field':
      return {
        ...state,
        [action.field]: action.value
      }
    case 'submit':
      return {
        ...state,
        submitting: true,
        error: null
      }
    case 'submit_success':
      return {
        ...state,
        submitting: false,
        submitted: true
      }
    case 'submit_error':
      return {
        ...state,
        submitting: false,
        error: action.error
      }
    case 'reset':
      return action.initialState
    default:
      return state
  }
}

function ContactForm() {
  const initialState = {
    name: '',
    email: '',
    message: '',
    submitting: false,
    submitted: false,
    error: null
  }
  
  const [state, dispatch] = useReducer(formReducer, initialState)
  
  const updateField = (field, value) => {
    dispatch({ type: 'update_field', field, value })
  }
  
  const handleSubmit = async (e) => {
    e.preventDefault()
    dispatch({ type: 'submit' })
    
    try {
      await api.submitForm(state)
      dispatch({ type: 'submit_success' })
    } catch (error) {
      dispatch({ type: 'submit_error', error: error.message })
    }
  }
  
  return (
    <form onSubmit={handleSubmit}>
      <input
        value={state.name}
        onChange={e => updateField('name', e.target.value)}
      />
      <input
        value={state.email}
        onChange={e => updateField('email', e.target.value)}
      />
      <textarea
        value={state.message}
        onChange={e => updateField('message', e.target.value)}
      />
      <button type="submit" disabled={state.submitting}>
        {state.submitting ? 'Submitting...' : 'Submit'}
      </button>
      {state.error && <p className="error">{state.error}</p>}
      {state.submitted && <p className="success">Submitted!</p>}
    </form>
  )
}
```

---

## Combining with Context

```jsx
const TodoContext = createContext(null)
const TodoDispatchContext = createContext(null)

function TodoProvider({ children }) {
  const [todos, dispatch] = useReducer(todosReducer, [])
  
  return (
    <TodoContext.Provider value={todos}>
      <TodoDispatchContext.Provider value={dispatch}>
        {children}
      </TodoDispatchContext.Provider>
    </TodoContext.Provider>
  )
}

function useTodos() {
  return useContext(TodoContext)
}

function useTodosDispatch() {
  return useContext(TodoDispatchContext)
}

// Usage
function AddTodo() {
  const dispatch = useTodosDispatch()
  const [text, setText] = useState('')
  
  return (
    <form onSubmit={e => {
      e.preventDefault()
      dispatch({
        type: 'added',
        id: Date.now(),
        text: text
      })
      setText('')
    }}>
      <input value={text} onChange={e => setText(e.target.value)} />
      <button type="submit">Add</button>
    </form>
  )
}

function TodoList() {
  const todos = useTodos()
  const dispatch = useTodosDispatch()
  
  return (
    <ul>
      {todos.map(todo => (
        <li key={todo.id}>
          <input
            type="checkbox"
            checked={todo.done}
            onChange={() => {
              dispatch({
                type: 'toggled',
                id: todo.id
              })
            }}
          />
          {todo.text}
          <button onClick={() => {
            dispatch({
              type: 'deleted',
              id: todo.id
            })
          }}>Delete</button>
        </li>
      ))}
    </ul>
  )
}
```

---

## TypeScript

```tsx
type State = {
  count: number
  step: number
}

type Action =
  | { type: 'increment' }
  | { type: 'decrement' }
  | { type: 'set_step'; payload: number }
  | { type: 'reset' }

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'increment':
      return { ...state, count: state.count + state.step }
    case 'decrement':
      return { ...state, count: state.count - state.step }
    case 'set_step':
      return { ...state, step: action.payload }
    case 'reset':
      return { count: 0, step: 1 }
    default:
      // TypeScript ensures all cases are handled
      const _exhaustive: never = action
      return state
  }
}

function Counter() {
  const [state, dispatch] = useReducer(reducer, { count: 0, step: 1 })
  
  return (
    <>
      <p>Count: {state.count}</p>
      <p>Step: {state.step}</p>
      <button onClick={() => dispatch({ type: 'increment' })}>+</button>
      <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
      <input
        type="number"
        value={state.step}
        onChange={e => dispatch({
          type: 'set_step',
          payload: Number(e.target.value)
        })}
      />
      <button onClick={() => dispatch({ type: 'reset' })}>Reset</button>
    </>
  )
}
```

---

## Best Practices

### Keep Reducers Pure

```jsx
// ❌ Bad - side effects in reducer
function reducer(state, action) {
  switch (action.type) {
    case 'added':
      fetch('/api/todos', { method: 'POST' })  // ❌ Side effect
      return [...state, action.todo]
  }
}

// ✅ Good - side effects in component
function TodoApp() {
  const [todos, dispatch] = useReducer(reducer, [])
  
  const addTodo = async (todo) => {
    await fetch('/api/todos', { method: 'POST', body: JSON.stringify(todo) })
    dispatch({ type: 'added', todo })
  }
}
```

### Always Return New State

```jsx
// ❌ Bad - mutates state
function reducer(state, action) {
  switch (action.type) {
    case 'increment':
      state.count++  // ❌ Mutation
      return state
  }
}

// ✅ Good - returns new object
function reducer(state, action) {
  switch (action.type) {
    case 'increment':
      return { ...state, count: state.count + 1 }
  }
}
```

### Use Action Creators

```jsx
// Action creators
const actions = {
  addTodo: (id, text) => ({ type: 'added', id, text }),
  deleteTodo: (id) => ({ type: 'deleted', id }),
  toggleTodo: (id) => ({ type: 'toggled', id })
}

// Usage
dispatch(actions.addTodo(1, 'Learn React'))
dispatch(actions.toggleTodo(1))
```

<!--
Source references:
- https://react.dev/reference/react/useReducer
- https://react.dev/learn/extracting-state-logic-into-a-reducer
-->
