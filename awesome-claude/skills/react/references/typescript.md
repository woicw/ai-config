---
name: typescript-react
description: Typing props, state, hooks, children, and events in React with TypeScript
---

# TypeScript with React

TypeScript provides type safety and better developer experience for React applications.

## Component Props

### Basic Props Interface

```tsx
interface ButtonProps {
  label: string
  onClick: () => void
  disabled?: boolean
}

function Button({ label, onClick, disabled }: ButtonProps) {
  return (
    <button onClick={onClick} disabled={disabled}>
      {label}
    </button>
  )
}
```

### With Children

```tsx
interface CardProps {
  title: string
  children: React.ReactNode
}

function Card({ title, children }: CardProps) {
  return (
    <div className="card">
      <h2>{title}</h2>
      <div>{children}</div>
    </div>
  )
}
```

### Optional Props

```tsx
interface UserProfileProps {
  name: string
  age?: number
  email?: string
}

function UserProfile({ name, age, email }: UserProfileProps) {
  return (
    <div>
      <h1>{name}</h1>
      {age && <p>Age: {age}</p>}
      {email && <p>Email: {email}</p>}
    </div>
  )
}
```

### Default Props

```tsx
interface ButtonProps {
  variant?: 'primary' | 'secondary'
  size?: 'small' | 'medium' | 'large'
}

function Button({ 
  variant = 'primary', 
  size = 'medium',
  children 
}: ButtonProps) {
  return (
    <button className={`btn-${variant} btn-${size}`}>
      {children}
    </button>
  )
}
```

---

## useState Hook

### Type Inference

```tsx
// Type inferred as number
const [count, setCount] = useState(0)

// Type inferred as string | null
const [name, setName] = useState<string | null>(null)
```

### Explicit Types

```tsx
// Explicit type annotation
const [count, setCount] = useState<number>(0)

// Union types
type Status = 'idle' | 'loading' | 'success' | 'error'
const [status, setStatus] = useState<Status>('idle')

// Complex types
interface User {
  id: string
  name: string
  email: string
}

const [user, setUser] = useState<User | null>(null)
```

### Discriminated Unions

```tsx
type RequestState =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: any }
  | { status: 'error'; error: Error }

const [requestState, setRequestState] = useState<RequestState>({ 
  status: 'idle' 
})

// Type narrowing
if (requestState.status === 'success') {
  console.log(requestState.data) // TypeScript knows data exists
}
```

---

## useRef Hook

### DOM Refs

```tsx
function Input() {
  const inputRef = useRef<HTMLInputElement>(null)
  
  const focusInput = () => {
    inputRef.current?.focus()
  }
  
  return (
    <>
      <input ref={inputRef} type="text" />
      <button onClick={focusInput}>Focus</button>
    </>
  )
}
```

### Mutable Values

```tsx
function Timer() {
  const intervalRef = useRef<number | undefined>(undefined)
  
  useEffect(() => {
    intervalRef.current = setInterval(() => {
      console.log('Tick')
    }, 1000)
    
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
      }
    }
  }, [])
  
  return <div>Timer</div>
}
```

### Generic Refs

```tsx
function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T>()
  
  useEffect(() => {
    ref.current = value
  }, [value])
  
  return ref.current
}
```

---

## useCallback & useMemo

### useCallback

```tsx
interface ProductPageProps {
  productId: string
  referrer: string
}

function ProductPage({ productId, referrer }: ProductPageProps) {
  const handleSubmit = useCallback((orderDetails: OrderDetails) => {
    post(`/product/${productId}/buy`, {
      referrer,
      orderDetails
    })
  }, [productId, referrer])
  
  return <Form onSubmit={handleSubmit} />
}
```

### useMemo

```tsx
function ExpensiveComponent({ items }: { items: Item[] }) {
  const sortedItems = useMemo(() => {
    return items.sort((a, b) => a.name.localeCompare(b.name))
  }, [items])
  
  return (
    <ul>
      {sortedItems.map(item => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  )
}
```

---

## Event Handlers

### Form Events

```tsx
function Form() {
  const [value, setValue] = useState('')
  
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setValue(e.target.value)
  }
  
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    console.log(value)
  }
  
  return (
    <form onSubmit={handleSubmit}>
      <input value={value} onChange={handleChange} />
      <button type="submit">Submit</button>
    </form>
  )
}
```

### Mouse Events

```tsx
function Button() {
  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    console.log('Clicked', e.currentTarget)
  }
  
  return <button onClick={handleClick}>Click me</button>
}
```

### Keyboard Events

```tsx
function Input() {
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      console.log('Enter pressed')
    }
  }
  
  return <input onKeyDown={handleKeyDown} />
}
```

### Generic Event Handler

```tsx
function useEventHandler<T extends HTMLElement>(
  handler: (e: React.MouseEvent<T>) => void
) {
  return handler
}

const handleClick = useEventHandler<HTMLButtonElement>((e) => {
  console.log(e.currentTarget) // Typed as HTMLButtonElement
})
```

---

## useReducer

```tsx
interface State {
  count: number
  step: number
}

type Action =
  | { type: 'increment' }
  | { type: 'decrement' }
  | { type: 'reset' }
  | { type: 'setStep'; step: number }

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'increment':
      return { ...state, count: state.count + state.step }
    case 'decrement':
      return { ...state, count: state.count - state.step }
    case 'reset':
      return { ...state, count: 0 }
    case 'setStep':
      return { ...state, step: action.step }
    default:
      return state
  }
}

function Counter() {
  const [state, dispatch] = useReducer(reducer, { count: 0, step: 1 })
  
  return (
    <div>
      <p>Count: {state.count}</p>
      <button onClick={() => dispatch({ type: 'increment' })}>+</button>
      <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
    </div>
  )
}
```

---

## useContext

```tsx
interface User {
  id: string
  name: string
  email: string
}

interface AuthContextType {
  user: User | null
  login: (credentials: Credentials) => Promise<void>
  logout: () => Promise<void>
  loading: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
```

---

## Generic Components

```tsx
interface ListProps<T> {
  items: T[]
  renderItem: (item: T) => React.ReactNode
  keyExtractor: (item: T) => string | number
}

function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
  return (
    <ul>
      {items.map(item => (
        <li key={keyExtractor(item)}>
          {renderItem(item)}
        </li>
      ))}
    </ul>
  )
}

// Usage
<List
  items={users}
  renderItem={user => <div>{user.name}</div>}
  keyExtractor={user => user.id}
/>
```

---

## forwardRef

```tsx
interface InputProps {
  label: string
  error?: string
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, ...props }, ref) => {
    return (
      <div>
        <label>{label}</label>
        <input ref={ref} {...props} />
        {error && <span className="error">{error}</span>}
      </div>
    )
  }
)

Input.displayName = 'Input'
```

---

## useImperativeHandle

```tsx
interface InputHandle {
  focus: () => void
  scrollIntoView: () => void
  getValue: () => string
}

interface InputProps {
  defaultValue?: string
}

const Input = forwardRef<InputHandle, InputProps>(
  ({ defaultValue = '' }, ref) => {
    const inputRef = useRef<HTMLInputElement>(null)
    
    useImperativeHandle(ref, () => ({
      focus: () => inputRef.current?.focus(),
      scrollIntoView: () => inputRef.current?.scrollIntoView(),
      getValue: () => inputRef.current?.value || ''
    }), [])
    
    return <input ref={inputRef} defaultValue={defaultValue} />
  }
)

Input.displayName = 'Input'
```

---

## Custom Hooks

```tsx
interface UseFetchResult<T> {
  data: T | null
  loading: boolean
  error: Error | null
  refetch: () => Promise<void>
}

function useFetch<T>(url: string): UseFetchResult<T> {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)
  
  const fetchData = useCallback(async () => {
    try {
      setLoading(true)
      const response = await fetch(url)
      const json = await response.json()
      setData(json)
    } catch (err) {
      setError(err as Error)
    } finally {
      setLoading(false)
    }
  }, [url])
  
  useEffect(() => {
    fetchData()
  }, [fetchData])
  
  return { data, loading, error, refetch: fetchData }
}

// Usage
function UserProfile({ userId }: { userId: string }) {
  const { data: user, loading, error } = useFetch<User>(`/api/users/${userId}`)
  
  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>
  if (!user) return null
  
  return <div>{user.name}</div>
}
```

---

## Component Props with Generics

```tsx
interface SelectProps<T> {
  options: T[]
  value: T | null
  onChange: (value: T) => void
  getLabel: (option: T) => string
  getValue: (option: T) => string
}

function Select<T>({ 
  options, 
  value, 
  onChange, 
  getLabel, 
  getValue 
}: SelectProps<T>) {
  return (
    <select 
      value={value ? getValue(value) : ''}
      onChange={(e) => {
        const selected = options.find(opt => getValue(opt) === e.target.value)
        if (selected) onChange(selected)
      }}
    >
      {options.map(option => (
        <option key={getValue(option)} value={getValue(option)}>
          {getLabel(option)}
        </option>
      ))}
    </select>
  )
}

// Usage
interface User {
  id: string
  name: string
}

<Select<User>
  options={users}
  value={selectedUser}
  onChange={setSelectedUser}
  getLabel={user => user.name}
  getValue={user => user.id}
/>
```

---

## React.ReactNode Types

```tsx
// Most common - accepts anything renderable
children: React.ReactNode

// Only elements
children: React.ReactElement

// Only string
children: string

// Array of elements
children: React.ReactElement[]

// Specific element type
children: React.ReactElement<ButtonProps>
```

---

## Common Patterns

### Component with Ref

```tsx
interface ButtonProps {
  children: React.ReactNode
  onClick?: () => void
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ children, onClick }, ref) => {
    return (
      <button ref={ref} onClick={onClick}>
        {children}
      </button>
    )
  }
)

Button.displayName = 'Button'
```

### Higher-Order Component

```tsx
interface WithLoadingProps {
  loading: boolean
}

function withLoading<P extends object>(
  Component: React.ComponentType<P>
) {
  return function WithLoadingComponent(props: P & WithLoadingProps) {
    const { loading, ...rest } = props
    
    if (loading) {
      return <div>Loading...</div>
    }
    
    return <Component {...(rest as P)} />
  }
}
```

### Polymorphic Component

```tsx
type PolymorphicComponentProps<E extends React.ElementType> = {
  as?: E
  children: React.ReactNode
} & React.ComponentPropsWithoutRef<E>

function PolymorphicComponent<E extends React.ElementType = 'div'>({
  as,
  children,
  ...props
}: PolymorphicComponentProps<E>) {
  const Component = as || 'div'
  return <Component {...props}>{children}</Component>
}

// Usage
<PolymorphicComponent as="button" onClick={handleClick}>
  Click me
</PolymorphicComponent>
```

---

## Type Utilities

### Extract Props Type

```tsx
type ButtonProps = React.ComponentProps<'button'>
type InputProps = React.ComponentProps<'input'>

// From component
type MyButtonProps = React.ComponentProps<typeof MyButton>
```

### Component Props Without Ref

```tsx
type ButtonProps = React.ComponentPropsWithoutRef<'button'>
```

### Component Props With Ref

```tsx
type InputProps = React.ComponentPropsWithRef<'input'>
```

---

## Strict Mode Considerations

### useRef in React 19+

```tsx
// ❌ Error in React 19 - requires argument
const ref = useRef()

// ✅ Correct
const ref = useRef<HTMLInputElement>(null)
const ref = useRef<number | undefined>(undefined)
```

### createContext

```tsx
// ❌ Error in React 19 - requires argument
const Context = createContext()

// ✅ Correct
const Context = createContext<AuthContextType | undefined>(undefined)
```

<!--
Source references:
- https://react.dev/learn/typescript
- https://react.dev/reference/react/types
-->
