---
name: conditional-rendering
description: Conditional rendering with ternary, &&, and early returns
---

# Conditional Rendering

React allows you to conditionally render components based on state or props.

## Conditional Operators

### Ternary Operator

```jsx
function Greeting({ isLoggedIn }) {
  return (
    <div>
      {isLoggedIn ? (
        <h1>Welcome back!</h1>
      ) : (
        <h1>Please sign in</h1>
      )}
    </div>
  )
}
```

### Logical && Operator

```jsx
function Notifications({ count }) {
  return (
    <div>
      <h1>Inbox</h1>
      {count > 0 && (
        <p>You have {count} unread messages</p>
      )}
    </div>
  )
}
```

### Logical || Operator

```jsx
function UserName({ name }) {
  return <h1>{name || 'Guest'}</h1>
}
```

---

## Early Returns

### Guard Clauses

```jsx
function UserProfile({ user }) {
  if (!user) {
    return <div>Loading...</div>
  }
  
  if (user.error) {
    return <div>Error: {user.error}</div>
  }
  
  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  )
}
```

### Multiple Conditions

```jsx
function Dashboard({ user, loading, error }) {
  if (loading) {
    return <LoadingSpinner />
  }
  
  if (error) {
    return <ErrorMessage error={error} />
  }
  
  if (!user) {
    return <LoginPrompt />
  }
  
  return <DashboardContent user={user} />
}
```

---

## Conditional Rendering Patterns

### Show/Hide Elements

```jsx
function Modal({ isOpen, onClose, children }) {
  if (!isOpen) {
    return null
  }
  
  return (
    <div className="modal">
      <div className="modal-content">
        {children}
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  )
}
```

### Loading States

```jsx
function DataDisplay({ data, loading }) {
  return (
    <div>
      {loading ? (
        <LoadingSpinner />
      ) : (
        <DataTable data={data} />
      )}
    </div>
  )
}
```

### Error States

```jsx
function UserList({ users, error }) {
  if (error) {
    return <ErrorMessage message={error} />
  }
  
  if (users.length === 0) {
    return <EmptyState message="No users found" />
  }
  
  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}
```

---

## Complex Conditions

### Multiple Ternaries

```jsx
function StatusBadge({ status }) {
  return (
    <span className={
      status === 'active' ? 'badge-green' :
      status === 'pending' ? 'badge-yellow' :
      status === 'inactive' ? 'badge-gray' :
      'badge-default'
    }>
      {status}
    </span>
  )
}
```

### Object Mapping

```jsx
function StatusBadge({ status }) {
  const badges = {
    active: <span className="badge-green">Active</span>,
    pending: <span className="badge-yellow">Pending</span>,
    inactive: <span className="badge-gray">Inactive</span>
  }
  
  return badges[status] || <span>Unknown</span>
}
```

### Switch-like Pattern

```jsx
function Notification({ type, message }) {
  const getIcon = () => {
    switch (type) {
      case 'success':
        return <SuccessIcon />
      case 'error':
        return <ErrorIcon />
      case 'warning':
        return <WarningIcon />
      default:
        return <InfoIcon />
    }
  }
  
  return (
    <div className={`notification notification-${type}`}>
      {getIcon()}
      <span>{message}</span>
    </div>
  )
}
```

---

## Conditional Props

### Spreading Conditionally

```jsx
function Button({ primary, disabled, children }) {
  return (
    <button
      className={primary ? 'btn-primary' : 'btn-default'}
      {...(disabled && { disabled: true })}
    >
      {children}
    </button>
  )
}
```

### Conditional Attributes

```jsx
function Input({ label, required, error }) {
  return (
    <div>
      <label>
        {label}
        {required && <span className="required">*</span>}
      </label>
      <input
        className={error ? 'input-error' : 'input'}
        aria-invalid={error ? 'true' : 'false'}
        aria-required={required ? 'true' : 'false'}
      />
      {error && <span className="error-message">{error}</span>}
    </div>
  )
}
```

---

## Preventing Render

### Return null

```jsx
function Warning({ show, message }) {
  if (!show) {
    return null
  }
  
  return <div className="warning">{message}</div>
}
```

### CSS Display

```jsx
function Warning({ show, message }) {
  return (
    <div
      className="warning"
      style={{ display: show ? 'block' : 'none' }}
    >
      {message}
    </div>
  )
}
```

---

## Auth Patterns

### Protected Component

```jsx
function ProtectedRoute({ user, children }) {
  if (!user) {
    return <Navigate to="/login" />
  }
  
  return children
}

// Usage
<ProtectedRoute user={currentUser}>
  <Dashboard />
</ProtectedRoute>
```

### Role-Based Access

```jsx
function AdminPanel({ user }) {
  if (!user) {
    return <LoginPrompt />
  }
  
  if (user.role !== 'admin') {
    return <AccessDenied />
  }
  
  return <AdminDashboard />
}
```

### Permission Check

```jsx
function EditButton({ user, resource }) {
  const canEdit = user?.permissions.includes('edit') && 
                  resource.ownerId === user.id
  
  if (!canEdit) {
    return null
  }
  
  return <button>Edit</button>
}
```

---

## Loading Patterns

### Skeleton Screens

```jsx
function UserCard({ user, loading }) {
  if (loading) {
    return (
      <div className="user-card">
        <div className="skeleton avatar" />
        <div className="skeleton text" />
        <div className="skeleton text short" />
      </div>
    )
  }
  
  return (
    <div className="user-card">
      <img src={user.avatar} alt={user.name} />
      <h3>{user.name}</h3>
      <p>{user.bio}</p>
    </div>
  )
}
```

### Suspense

```jsx
import { Suspense } from 'react'

function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <UserProfile />
    </Suspense>
  )
}
```

---

## Feature Flags

```jsx
function FeatureWrapper({ feature, fallback, children }) {
  const features = useFeatureFlags()
  
  if (!features[feature]) {
    return fallback || null
  }
  
  return children
}

// Usage
<FeatureWrapper feature="newUI" fallback={<OldUI />}>
  <NewUI />
</FeatureWrapper>
```

---

## Best Practices

### Avoid Deep Nesting

```jsx
// ❌ Bad - deeply nested
function Component({ user, loading, error }) {
  return (
    <div>
      {loading ? (
        <Spinner />
      ) : (
        error ? (
          <Error />
        ) : (
          user ? (
            <UserInfo user={user} />
          ) : (
            <NoUser />
          )
        )
      )}
    </div>
  )
}

// ✅ Good - early returns
function Component({ user, loading, error }) {
  if (loading) return <Spinner />
  if (error) return <Error />
  if (!user) return <NoUser />
  
  return <UserInfo user={user} />
}
```

### Use Meaningful Variable Names

```jsx
// ❌ Bad
{x && <Component />}

// ✅ Good
const hasPermission = user?.role === 'admin'
{hasPermission && <AdminPanel />}
```

### Avoid Truthiness Bugs

```jsx
// ❌ Bad - 0 renders as "0"
{count && <div>Count: {count}</div>}

// ✅ Good
{count > 0 && <div>Count: {count}</div>}

// Or
{count !== 0 && <div>Count: {count}</div>}
```

### Extract Complex Conditions

```jsx
// ❌ Bad
{user && user.age >= 18 && user.verified && !user.banned && (
  <AccessButton />
)}

// ✅ Good
const canAccess = user?.age >= 18 && 
                  user?.verified && 
                  !user?.banned

{canAccess && <AccessButton />}

// ✅ Better - use function
function canUserAccess(user) {
  if (!user) return false
  return user.age >= 18 && user.verified && !user.banned
}

{canUserAccess(user) && <AccessButton />}
```

---

## TypeScript

```tsx
type UserProfileProps = {
  user: User | null
  loading: boolean
  error?: string
}

function UserProfile({ user, loading, error }: UserProfileProps) {
  if (loading) {
    return <LoadingSpinner />
  }
  
  if (error) {
    return <ErrorMessage message={error} />
  }
  
  if (!user) {
    return <EmptyState message="No user found" />
  }
  
  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  )
}
```

<!--
Source references:
- https://react.dev/learn/conditional-rendering
-->
