---
name: patterns-component
description: Component patterns, custom hooks, utility functions, and type definitions
---

# Component Patterns

## Component Structure

```typescript
import { FC } from 'react'
import { cn } from '@/utils/cn'

interface Props {
  title: string
  disabled?: boolean
  className?: string
  onSubmit: (data: FormData) => void
}

export const MyComponent: FC<Props> = ({ 
  title, 
  disabled = false, 
  className,
  onSubmit 
}) => {
  return (
    <div className={cn('p-4 rounded-lg', className)}>
      {/* ... */}
    </div>
  )
}
```

## Custom Hooks

### useNavigateWithQuery

```typescript
// hooks/useNavigateWithQuery.ts
import { useNavigate, useSearchParams, type NavigateOptions, type To } from 'react-router';

export const useNavigateWithQuery = () => {
  const navigate = useNavigate();
  const [query] = useSearchParams();
  const navigateWithQuery = (path: number | string, options?: NavigateOptions) => {
    if (typeof path === 'number') {
      navigate(path as unknown as To, options);
      return;
    }
    const [pathname, search] = (path as string).split('?');
    const newQuery = new URLSearchParams(search);
    for (const [key, value] of newQuery) {
      query.set(key, value);
    }
    navigate(`${pathname}?${query?.toString()}`, options);
  };

  return navigateWithQuery;
};


// Usage
const navigate = useNavigateWithQuery()
// navigate('/users/1')
// navigate('/users/1?page=2')
// navigate('/users/1?page=2&size=10')
```

### useUrlState

```typescript
import { useSearchParams } from 'react-router'
import { useMemoizedFn } from 'ahooks'

const useUrlState = <T extends Record<string, string>>(defaultValue: T) => {
  const [searchParams, setSearchParams] = useSearchParams()
  
  const state = useMemo(() => {
    const result = { ...defaultValue }
    for (const key of Object.keys(defaultValue)) {
      result[key] = searchParams.get(key) || defaultValue[key]
    }
    return result
  }, [searchParams])

  const setState = useMemoizedFn((patch: Partial<T>) => {
    setSearchParams((prev) => {
      Object.entries(patch).forEach(([k, v]) => {
        if (v) prev.set(k, v)
        else prev.delete(k)
      })
      return prev
    })
  })

  return [state, setState] as const
}
```

## Utility Functions

### cn (className merge)

```typescript
// utils/cn.ts
import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export const cn = (...inputs: ClassValue[]) => twMerge(clsx(inputs))
```

## Type Definitions

```typescript
// types/api.ts
export interface PageParams {
  page: number
  size: number
}

export interface PageResponse<T> {
  list: T[]
  total: number
  page: number
  size: number
}

// types/user.ts
export interface User {
  id: string
  name: string
  email: string
  avatar?: string
  createdAt: string
}

export type CreateUserDTO = Omit<User, 'id' | 'createdAt'>
export type UpdateUserDTO = Partial<CreateUserDTO>
```
