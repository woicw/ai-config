---
name: react-components-jsx
description: Functional components, JSX syntax, props, and composition
---

# React Components & JSX

Components are the building blocks of React applications. Modern React uses functional components with hooks.

## Functional Components

### Basic Component

```jsx
function Greeting({ name }) {
  return <h1>Hello, {name}!</h1>
}

export default function App() {
  return <Greeting name="World" />
}
```

### With TypeScript

```tsx
interface GreetingProps {
  name: string
}

function Greeting({ name }: GreetingProps) {
  return <h1>Hello, {name}!</h1>
}
```

---

## JSX Syntax

JSX is a syntax extension that looks like HTML but is transformed into JavaScript.

### Embedding Expressions

```jsx
function Profile({ user }) {
  return (
    <div>
      <h1>{user.name}</h1>
      <p>Age: {user.age}</p>
      <p>Result: {2 + 2}</p>
    </div>
  )
}
```

### JSX Attributes

```jsx
// Use camelCase for attributes
<img 
  src={user.avatarUrl}
  alt={user.name}
  className="avatar"  // class → className
  onClick={handleClick}
/>

// Style as object
<div style={{ color: 'red', fontSize: 16 }}>Text</div>
```

### Fragments

Return multiple elements without extra DOM nodes:

```jsx
// Short syntax (most common)
function List() {
  return (
    <>
      <li>Item 1</li>
      <li>Item 2</li>
    </>
  )
}

// Explicit Fragment (when you need key prop)
import { Fragment } from 'react'

function List({ items }) {
  return items.map(item => (
    <Fragment key={item.id}>
      <dt>{item.term}</dt>
      <dd>{item.description}</dd>
    </Fragment>
  ))
}
```

---

## Props

Props are arguments passed to components. They are read-only.

### Basic Props

```jsx
function Welcome({ name, age }) {
  return <p>Hello {name}, you are {age} years old</p>
}

<Welcome name="Sara" age={28} />
```

### Default Props

```jsx
function Button({ text = 'Click me', disabled = false }) {
  return <button disabled={disabled}>{text}</button>
}
```

### Rest Props (Spreading)

```jsx
function Input({ label, ...rest }) {
  return (
    <label>
      {label}
      <input {...rest} />
    </label>
  )
}

<Input label="Name" type="text" placeholder="Enter name" />
```

### Children Prop

```jsx
function Card({ children, title }) {
  return (
    <div className="card">
      <h2>{title}</h2>
      <div className="card-body">{children}</div>
    </div>
  )
}

<Card title="Profile">
  <p>User content here</p>
</Card>
```

### Render Props Pattern

```jsx
function DataProvider({ render }) {
  const [data, setData] = useState([])
  
  useEffect(() => {
    fetchData().then(setData)
  }, [])
  
  return render(data)
}

<DataProvider 
  render={data => (
    <ul>
      {data.map(item => <li key={item.id}>{item.name}</li>)}
    </ul>
  )}
/>
```

---

## Component Composition

### Container/Presentational Pattern

```jsx
// Presentational component
function UserCard({ user, onEdit }) {
  return (
    <div className="user-card">
      <h3>{user.name}</h3>
      <p>{user.email}</p>
      <button onClick={onEdit}>Edit</button>
    </div>
  )
}

// Container component
function UserCardContainer({ userId }) {
  const [user, setUser] = useState(null)
  
  useEffect(() => {
    fetchUser(userId).then(setUser)
  }, [userId])
  
  const handleEdit = () => {
    // Edit logic
  }
  
  if (!user) return <div>Loading...</div>
  
  return <UserCard user={user} onEdit={handleEdit} />
}
```

### Slot Pattern (Named Children)

```jsx
function Layout({ header, sidebar, content }) {
  return (
    <div className="layout">
      <header>{header}</header>
      <aside>{sidebar}</aside>
      <main>{content}</main>
    </div>
  )
}

<Layout
  header={<Header />}
  sidebar={<Sidebar />}
  content={<MainContent />}
/>
```

---

## Event Handling

### Basic Events

```jsx
function Button() {
  const handleClick = (e) => {
    e.preventDefault()
    console.log('Button clicked')
  }
  
  return <button onClick={handleClick}>Click me</button>
}
```

### With Parameters

```jsx
function List({ items }) {
  const handleDelete = (id) => {
    console.log('Delete item', id)
  }
  
  return (
    <ul>
      {items.map(item => (
        <li key={item.id}>
          {item.name}
          <button onClick={() => handleDelete(item.id)}>Delete</button>
        </li>
      ))}
    </ul>
  )
}
```

### Common Events

```jsx
function Form() {
  return (
    <>
      <input
        onChange={(e) => console.log(e.target.value)}
        onFocus={() => console.log('focused')}
        onBlur={() => console.log('blurred')}
      />
      <form onSubmit={(e) => e.preventDefault()}>
        <button type="submit">Submit</button>
      </form>
    </>
  )
}
```

---

## Export/Import Patterns

### Default Export

```jsx
// Button.jsx
export default function Button({ children }) {
  return <button>{children}</button>
}

// App.jsx
import Button from './Button'
```

### Named Export

```jsx
// components.jsx
export function Button({ children }) {
  return <button>{children}</button>
}

export function Input({ value }) {
  return <input value={value} />
}

// App.jsx
import { Button, Input } from './components'
```

<!--
Source references:
- https://react.dev/learn
- https://react.dev/learn/installation
- https://react.dev/learn/describing-the-ui
-->
