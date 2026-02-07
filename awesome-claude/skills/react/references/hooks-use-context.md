---
name: use-context
description: Context API, provider/consumer pattern, and dependency injection
---

# useContext Hook

Context provides a way to pass data through the component tree without manually passing props at every level.

## Basic Usage

### Creating Context

```jsx
import { createContext, useContext, useState } from 'react'

// Create context with default value
const ThemeContext = createContext('light')

function App() {
  const [theme, setTheme] = useState('light')
  
  return (
    <ThemeContext.Provider value={theme}>
      <Page />
    </ThemeContext.Provider>
  )
}

function Page() {
  // Consume context
  const theme = useContext(ThemeContext)
  
  return <div className={`theme-${theme}`}>Content</div>
}
```

---

## Providing Context

### Single Value

```jsx
const ThemeContext = createContext('light')

function App() {
  const [theme, setTheme] = useState('light')
  
  return (
    <ThemeContext.Provider value={theme}>
      <Button />
    </ThemeContext.Provider>
  )
}

function Button() {
  const theme = useContext(ThemeContext)
  return <button className={`button-${theme}`}>Click</button>
}
```

### Object Value (State + Updater)

```jsx
const UserContext = createContext(null)

function App() {
  const [currentUser, setCurrentUser] = useState(null)
  
  const value = {
    currentUser,
    setCurrentUser
  }
  
  return (
    <UserContext.Provider value={value}>
      <Profile />
    </UserContext.Provider>
  )
}

function Profile() {
  const { currentUser, setCurrentUser } = useContext(UserContext)
  
  if (!currentUser) {
    return (
      <button onClick={() => setCurrentUser({ name: 'John' })}>
        Login
      </button>
    )
  }
  
  return <div>Welcome, {currentUser.name}</div>
}
```

---

## Multiple Contexts

```jsx
const ThemeContext = createContext('light')
const UserContext = createContext(null)

function App() {
  const [theme, setTheme] = useState('light')
  const [user, setUser] = useState(null)
  
  return (
    <ThemeContext.Provider value={theme}>
      <UserContext.Provider value={{ user, setUser }}>
        <Page />
      </UserContext.Provider>
    </ThemeContext.Provider>
  )
}

function Page() {
  const theme = useContext(ThemeContext)
  const { user } = useContext(UserContext)
  
  return (
    <div className={`theme-${theme}`}>
      {user ? `Hello, ${user.name}` : 'Not logged in'}
    </div>
  )
}
```

---

## Custom Context Hook Pattern

```jsx
// contexts/UserContext.jsx
const UserContext = createContext(null)

export function UserProvider({ children }) {
  const [user, setUser] = useState(null)
  
  const login = (userData) => {
    setUser(userData)
  }
  
  const logout = () => {
    setUser(null)
  }
  
  const value = {
    user,
    login,
    logout
  }
  
  return (
    <UserContext.Provider value={value}>
      {children}
    </UserContext.Provider>
  )
}

// Custom hook
export function useUser() {
  const context = useContext(UserContext)
  
  if (context === undefined) {
    throw new Error('useUser must be used within UserProvider')
  }
  
  return context
}

// Usage
function App() {
  return (
    <UserProvider>
      <Profile />
    </UserProvider>
  )
}

function Profile() {
  const { user, login, logout } = useUser()
  
  return (
    <div>
      {user ? (
        <>
          <p>Welcome, {user.name}</p>
          <button onClick={logout}>Logout</button>
        </>
      ) : (
        <button onClick={() => login({ name: 'John' })}>Login</button>
      )}
    </div>
  )
}
```

---

## Optimizing Context Performance

### Split Contexts

```jsx
// ❌ Bad - causes unnecessary rerenders
const AppContext = createContext()

function AppProvider({ children }) {
  const [user, setUser] = useState(null)
  const [theme, setTheme] = useState('light')
  
  return (
    <AppContext.Provider value={{ user, setUser, theme, setTheme }}>
      {children}
    </AppContext.Provider>
  )
}

// ✅ Good - separate concerns
const UserContext = createContext()
const ThemeContext = createContext()

function AppProvider({ children }) {
  const [user, setUser] = useState(null)
  const [theme, setTheme] = useState('light')
  
  return (
    <UserContext.Provider value={{ user, setUser }}>
      <ThemeContext.Provider value={{ theme, setTheme }}>
        {children}
      </ThemeContext.Provider>
    </UserContext.Provider>
  )
}
```

### Memoize Context Value

```jsx
import { useMemo, useCallback } from 'react'

function UserProvider({ children }) {
  const [user, setUser] = useState(null)
  
  // Memoize functions
  const login = useCallback((userData) => {
    setUser(userData)
  }, [])
  
  const logout = useCallback(() => {
    setUser(null)
  }, [])
  
  // Memoize context value
  const value = useMemo(() => ({
    user,
    login,
    logout
  }), [user, login, logout])
  
  return (
    <UserContext.Provider value={value}>
      {children}
    </UserContext.Provider>
  )
}
```

### Separate State and Actions

```jsx
const UserStateContext = createContext(null)
const UserActionsContext = createContext(null)

function UserProvider({ children }) {
  const [user, setUser] = useState(null)
  
  const actions = useMemo(() => ({
    login: (userData) => setUser(userData),
    logout: () => setUser(null)
  }), [])
  
  return (
    <UserStateContext.Provider value={user}>
      <UserActionsContext.Provider value={actions}>
        {children}
      </UserActionsContext.Provider>
    </UserStateContext.Provider>
  )
}

function useUserState() {
  return useContext(UserStateContext)
}

function useUserActions() {
  return useContext(UserActionsContext)
}

// Component only rerenders when user changes, not on action changes
function Profile() {
  const user = useUserState()
  const { logout } = useUserActions()
  
  return user && <button onClick={logout}>Logout</button>
}
```

---

## Common Patterns

### Auth Context

```jsx
const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  
  useEffect(() => {
    // Check auth on mount
    checkAuth()
      .then(setUser)
      .finally(() => setLoading(false))
  }, [])
  
  const login = async (credentials) => {
    const user = await api.login(credentials)
    setUser(user)
  }
  
  const logout = async () => {
    await api.logout()
    setUser(null)
  }
  
  const value = useMemo(() => ({
    user,
    loading,
    login,
    logout
  }), [user, loading])
  
  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
```

### Theme Context

```jsx
const ThemeContext = createContext('light')

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('theme') || 'light'
  })
  
  useEffect(() => {
    localStorage.setItem('theme', theme)
    document.documentElement.setAttribute('data-theme', theme)
  }, [theme])
  
  const toggleTheme = useCallback(() => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light')
  }, [])
  
  const value = useMemo(() => ({
    theme,
    setTheme,
    toggleTheme
  }), [theme, toggleTheme])
  
  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  )
}

export function useTheme() {
  const context = useContext(ThemeContext)
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider')
  }
  return context
}
```

---

## Combining Providers

### Wrapper Component

```jsx
function AppProviders({ children }) {
  return (
    <ThemeProvider>
      <AuthProvider>
        <NotificationProvider>
          {children}
        </NotificationProvider>
      </AuthProvider>
    </ThemeProvider>
  )
}

function App() {
  return (
    <AppProviders>
      <Router />
    </AppProviders>
  )
}
```

### Compose Providers Utility

```jsx
function composeProviders(...providers) {
  return ({ children }) => {
    return providers.reduceRight((acc, Provider) => {
      return <Provider>{acc}</Provider>
    }, children)
  }
}

const AllProviders = composeProviders(
  ThemeProvider,
  AuthProvider,
  NotificationProvider
)

function App() {
  return (
    <AllProviders>
      <Router />
    </AllProviders>
  )
}
```

---

## TypeScript

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

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  
  // ... implementation
  
  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
```

<!--
Source references:
- https://react.dev/reference/react/useContext
- https://react.dev/reference/react/createContext
- https://react.dev/learn/passing-data-deeply-with-context
-->
