---
name: patterns-zustand
description: Zustand store patterns and auth state management
---

# Zustand Store Patterns

## Basic Store

```typescript
// stores/useUserStore.ts
import { create } from 'zustand'

interface UserState {
  user: User | null
  token: string | null
  setUser: (user: User) => void
  setToken: (token: string) => void
  logout: () => void
}

export const useUserStore = create<UserState>(
      (set) => ({
        user: null,
        token: null,
        setUser: (user) => set({ user }),
        setToken: (token) => set({ token }),
        logout: () => set({ user: null, token: null }),
      }),
)
```

## Selector Optimization

Avoid unnecessary re-renders by using precise selectors:

```typescript
// ✅ Recommended: precise selector
const userName = useUserStore((s) => s.user?.name)

// ❌ Avoid: selecting entire state
const { user } = useUserStore()
```

## Auth Store

```typescript
// stores/useAuthStore.ts
import { create } from 'zustand'

interface AuthState {
  token: string | null
  user: User | null
  isAuthenticated: boolean
  login: (token: string, user: User) => void
  logout: () => void
}

export const useAuthStore = create<AuthState>(
    (set) => ({
      token: null,
      user: null,
      isAuthenticated: false,
      login: (token, user) => set({ token, user, isAuthenticated: true }),
      logout: () => set({ token: null, user: null, isAuthenticated: false }),
    })
)
```

## Route Guard

```typescript
const PrivateRoute: FC<{ children: ReactNode }> = ({ children }) => {
  const isAuth = useAuthStore((s) => s.isAuthenticated)
  if (!isAuth) return <Navigate to="/login" replace />
  return <>{children}</>
}
```
