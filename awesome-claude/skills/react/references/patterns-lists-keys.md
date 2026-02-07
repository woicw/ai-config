---
name: lists-keys
description: Rendering arrays, key prop, and unique identifiers
---

# Lists and Keys

React efficiently renders lists of elements using the `map()` function and requires unique `key` props.

## Basic List Rendering

```jsx
function TodoList() {
  const todos = [
    { id: 1, text: 'Learn React' },
    { id: 2, text: 'Build an app' },
    { id: 3, text: 'Deploy to production' }
  ]
  
  return (
    <ul>
      {todos.map(todo => (
        <li key={todo.id}>{todo.text}</li>
      ))}
    </ul>
  )
}
```

---

## The Key Prop

Keys help React identify which items have changed, been added, or removed.

### What Makes a Good Key?

```jsx
// ✅ Good - stable ID from data
<li key={user.id}>{user.name}</li>

// ✅ Good - database ID
<li key={product.productId}>{product.name}</li>

// ⚠️ Acceptable - generated stable ID (if no natural ID)
<li key={`user-${user.email}`}>{user.name}</li>

// ❌ Bad - array index
<li key={index}>{item.name}</li>

// ❌ Bad - random value
<li key={Math.random()}>{item.name}</li>
```

### Why Not Use Index?

```jsx
function TodoList() {
  const [todos, setTodos] = useState([
    { id: 1, text: 'First', done: false },
    { id: 2, text: 'Second', done: false }
  ])
  
  // ❌ Bad - using index as key
  return (
    <ul>
      {todos.map((todo, index) => (
        <li key={index}>
          <input type="checkbox" checked={todo.done} />
          {todo.text}
        </li>
      ))}
    </ul>
  )
  
  // Problem: When you remove or reorder items,
  // React will incorrectly reuse DOM elements
  // Checkbox state might not match the correct todo
}
```

---

## Common Patterns

### Rendering from State

```jsx
function UserList() {
  const [users, setUsers] = useState([
    { id: 1, name: 'John', email: 'john@example.com' },
    { id: 2, name: 'Jane', email: 'jane@example.com' }
  ])
  
  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>
          <h3>{user.name}</h3>
          <p>{user.email}</p>
        </li>
      ))}
    </ul>
  )
}
```

### With Component Extraction

```jsx
function UserCard({ user }) {
  return (
    <div className="user-card">
      <h3>{user.name}</h3>
      <p>{user.email}</p>
    </div>
  )
}

function UserList({ users }) {
  return (
    <div>
      {users.map(user => (
        <UserCard key={user.id} user={user} />
      ))}
    </div>
  )
}
```

### With Event Handlers

```jsx
function TodoList({ todos, onToggle, onDelete }) {
  return (
    <ul>
      {todos.map(todo => (
        <li key={todo.id}>
          <input
            type="checkbox"
            checked={todo.done}
            onChange={() => onToggle(todo.id)}
          />
          <span>{todo.text}</span>
          <button onClick={() => onDelete(todo.id)}>Delete</button>
        </li>
      ))}
    </ul>
  )
}
```

---

## Filtering and Sorting

### Filtering

```jsx
function ProductList({ products, category }) {
  const filteredProducts = products.filter(p => 
    category === 'all' || p.category === category
  )
  
  return (
    <ul>
      {filteredProducts.map(product => (
        <li key={product.id}>{product.name}</li>
      ))}
    </ul>
  )
}
```

### Sorting

```jsx
function UserList({ users, sortBy }) {
  const sortedUsers = [...users].sort((a, b) => {
    if (sortBy === 'name') {
      return a.name.localeCompare(b.name)
    }
    if (sortBy === 'age') {
      return a.age - b.age
    }
    return 0
  })
  
  return (
    <ul>
      {sortedUsers.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}
```

### Filtering and Sorting Together

```jsx
function ProductList({ products, category, sortBy }) {
  const processedProducts = products
    .filter(p => category === 'all' || p.category === category)
    .sort((a, b) => {
      if (sortBy === 'name') return a.name.localeCompare(b.name)
      if (sortBy === 'price') return a.price - b.price
      return 0
    })
  
  return (
    <ul>
      {processedProducts.map(product => (
        <li key={product.id}>
          {product.name} - ${product.price}
        </li>
      ))}
    </ul>
  )
}
```

---

## Empty Lists

```jsx
function TodoList({ todos }) {
  if (todos.length === 0) {
    return <p>No todos yet. Add one to get started!</p>
  }
  
  return (
    <ul>
      {todos.map(todo => (
        <li key={todo.id}>{todo.text}</li>
      ))}
    </ul>
  )
}

// Or inline
function TodoList({ todos }) {
  return (
    <>
      {todos.length === 0 ? (
        <p>No todos yet</p>
      ) : (
        <ul>
          {todos.map(todo => (
            <li key={todo.id}>{todo.text}</li>
          ))}
        </ul>
      )}
    </>
  )
}
```

---

## Nested Lists

```jsx
function CommentThread({ comments }) {
  return (
    <ul>
      {comments.map(comment => (
        <li key={comment.id}>
          <Comment comment={comment} />
          {comment.replies && comment.replies.length > 0 && (
            <CommentThread comments={comment.replies} />
          )}
        </li>
      ))}
    </ul>
  )
}
```

---

## Dynamic Lists

### Adding Items

```jsx
function TodoApp() {
  const [todos, setTodos] = useState([])
  const [nextId, setNextId] = useState(1)
  
  const addTodo = (text) => {
    setTodos([...todos, { id: nextId, text, done: false }])
    setNextId(nextId + 1)
  }
  
  return (
    <>
      <AddTodoForm onAdd={addTodo} />
      <ul>
        {todos.map(todo => (
          <li key={todo.id}>{todo.text}</li>
        ))}
      </ul>
    </>
  )
}
```

### Removing Items

```jsx
function TodoApp() {
  const [todos, setTodos] = useState([
    { id: 1, text: 'First' },
    { id: 2, text: 'Second' }
  ])
  
  const deleteTodo = (id) => {
    setTodos(todos.filter(todo => todo.id !== id))
  }
  
  return (
    <ul>
      {todos.map(todo => (
        <li key={todo.id}>
          {todo.text}
          <button onClick={() => deleteTodo(todo.id)}>Delete</button>
        </li>
      ))}
    </ul>
  )
}
```

### Updating Items

```jsx
function TodoApp() {
  const [todos, setTodos] = useState([
    { id: 1, text: 'First', done: false },
    { id: 2, text: 'Second', done: false }
  ])
  
  const toggleTodo = (id) => {
    setTodos(todos.map(todo =>
      todo.id === id
        ? { ...todo, done: !todo.done }
        : todo
    ))
  }
  
  return (
    <ul>
      {todos.map(todo => (
        <li key={todo.id}>
          <input
            type="checkbox"
            checked={todo.done}
            onChange={() => toggleTodo(todo.id)}
          />
          {todo.text}
        </li>
      ))}
    </ul>
  )
}
```

---

## Fragments in Lists

When you need multiple root elements:

```jsx
function Glossary({ items }) {
  return (
    <dl>
      {items.map(item => (
        <Fragment key={item.id}>
          <dt>{item.term}</dt>
          <dd>{item.description}</dd>
        </Fragment>
      ))}
    </dl>
  )
}
```

---

## Performance Considerations

### Virtualization for Long Lists

```jsx
// For very long lists (1000+ items), use virtualization
import { FixedSizeList } from 'react-window'

function VirtualizedList({ items }) {
  const Row = ({ index, style }) => (
    <div style={style}>
      {items[index].name}
    </div>
  )
  
  return (
    <FixedSizeList
      height={600}
      itemCount={items.length}
      itemSize={35}
      width="100%"
    >
      {Row}
    </FixedSizeList>
  )
}
```

### Memoize List Items

```jsx
const TodoItem = memo(function TodoItem({ todo, onToggle, onDelete }) {
  return (
    <li>
      <input
        type="checkbox"
        checked={todo.done}
        onChange={() => onToggle(todo.id)}
      />
      {todo.text}
      <button onClick={() => onDelete(todo.id)}>Delete</button>
    </li>
  )
})

function TodoList({ todos, onToggle, onDelete }) {
  return (
    <ul>
      {todos.map(todo => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onToggle={onToggle}
          onDelete={onDelete}
        />
      ))}
    </ul>
  )
}
```

---

## Best Practices

1. **Always use keys** when rendering lists
2. **Keys must be unique** among siblings
3. **Keys should be stable** - don't use random values
4. **Prefer data IDs** over array indices
5. **Extract list items** into separate components
6. **Generate IDs when necessary** - use libraries like `uuid` or `nanoid`
7. **Don't use index as key** unless list is static and never reordered

---

## Generating IDs

When your data doesn't have natural IDs:

```jsx
import { nanoid } from 'nanoid'

function TodoApp() {
  const [todos, setTodos] = useState([])
  
  const addTodo = (text) => {
    setTodos([...todos, {
      id: nanoid(),  // Generates unique ID
      text,
      done: false
    }])
  }
  
  return (
    <ul>
      {todos.map(todo => (
        <li key={todo.id}>{todo.text}</li>
      ))}
    </ul>
  )
}
```

<!--
Source references:
- https://react.dev/learn/rendering-lists
- https://react.dev/learn/tutorial-tic-tac-toe
-->
