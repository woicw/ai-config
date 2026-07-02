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

## Component-Level Hooks（逻辑与视图分离）

组件内部的状态、事件处理、副作用统一封装进**组件级 hook**，不和 JSX 写在一起。组件体只做两件事：调用 hook 拿到状态/事件，渲染 JSX。

该模式适用于**所有组件**——`components/` 下的共享组件和 `pages/` 下的页面组件同样遵循。hook 放在组件目录的 `hooks/` 子目录中：

```
components/user-card/
├── index.tsx              # 组件：hook 输出 + JSX
└── hooks/
    └── use-user-card.ts   # 组件级 hook：状态 + 事件 + 副作用

pages/user-list/
├── index.tsx              # 页面组件：同样只有 hook 输出 + JSX
├── components/            # 页面私有组件（内部结构同上）
└── hooks/
    └── use-user-list.ts   # 页面级 hook
```

```typescript
// components/user-card/hooks/use-user-card.ts
import { useState } from 'react'
import { useMemoizedFn } from 'ahooks'

interface Options {
  userId: string
  onFollowed?: (userId: string) => void
}

export const useUserCard = ({ userId, onFollowed }: Options) => {
  const [expanded, setExpanded] = useState(false)
  const [following, setFollowing] = useState(false)

  const handleToggle = useMemoizedFn(() => {
    setExpanded((v) => !v)
  })

  const handleFollow = useMemoizedFn(async () => {
    setFollowing(true)
    try {
      await followUser(userId)
      onFollowed?.(userId)
    } finally {
      setFollowing(false)
    }
  })

  return { expanded, following, handleToggle, handleFollow }
}
```

```typescript
// components/user-card/index.tsx
import { FC } from 'react'
import { useUserCard } from './hooks/use-user-card'

interface Props {
  userId: string
  onFollowed?: (userId: string) => void
}

export const UserCard: FC<Props> = ({ userId, onFollowed }) => {
  const { expanded, following, handleToggle, handleFollow } = useUserCard({ userId, onFollowed })

  return (
    <div className="p-4 rounded-lg">
      <button onClick={handleToggle}>{expanded ? 'Collapse' : 'Expand'}</button>
      <button disabled={following} onClick={handleFollow}>Follow</button>
      {/* ... */}
    </div>
  )
}
```

**约定：**

- 组件文件（`index.tsx`）里不出现 `useState` / `useEffect` / 事件处理函数体，全部收进组件目录下 `hooks/use-<组件名>.ts`
- hook 与组件一一对应，命名为 `use` + 组件名；组件衍生的其他 hooks 也放同一 `hooks/` 目录
- 页面组件（`pages/` 下）同样遵循：页面逻辑收进页面目录的 `hooks/` 中
- hook 返回值即组件的全部动态输入：状态 + 事件回调；JSX 只消费，不定义逻辑
- 纯展示组件（只渲染 props、无内部状态和事件）不需要建 hook

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
