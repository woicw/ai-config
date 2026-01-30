---
name: react-webapp-builder
description: Guidelines and patterns for React business web application development. This skill should be used when developing features with React + TypeScript + Vite + Zustand + Tailwind CSS + ahooks + axios stack, using antd or shadcn/ui components. Provides code patterns, best practices, and examples for common business scenarios like forms, tables, CRUD operations, and state management.
license: Apache-2.0
---

# React Webapp Builder

业务前端开发的代码规范与最佳实践指南。

## 技术栈

| 类别 | 技术 | 用途 |
|------|------|------|
| 框架 | React 19+ | 函数式组件 + Hooks |
| 语言 | TypeScript | 类型安全 |
| 构建 | Vite | 开发构建 |
| 状态管理 | Zustand | 全局状态 |
| 样式 | Tailwind CSS | 原子化 CSS |
| Hooks | ahooks | 通用 Hooks |
| HTTP | axios | 请求封装 |
| 组件库 | antd / shadcn/ui | UI 组件 |

## 目录结构规范

```
src/
├── components/       # 通用组件
│   └── ui/           # 基础 UI 组件
├── hooks/            # 自定义 Hooks
├── stores/           # Zustand stores
├── pages/            # 页面组件
├── services/         # API 服务
├── utils/            # 工具函数
└── types/            # 类型定义
```

## 代码模式

### 1. Zustand Store

```typescript
// stores/useUserStore.ts
import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'

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

**选择器优化**（避免不必要渲染）:

```typescript
// 推荐：精确选择
const userName = useUserStore((s) => s.user?.name)

// 避免：选择整个 state
const { user } = useUserStore()
```

### 2. API 服务

```typescript
// services/api.ts
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000,
})

api.interceptors.request.use((config) => {
  const token = useUserStore.getState().token
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  (res) => res.data,
  (err) => {
    if (err.response?.status === 401) {
      useUserStore.getState().logout()
    }
    return Promise.reject(err)
  }
)

export default api
```

```typescript
// services/user.ts
import api from './api'

 export const getList = (params: UserListParams) => 
    api.get<UserListResponse>('/users', { params })
  
 export const getById= (id: string) => 
    api.get<User>(`/users/${id}`)
  
 export const create= (data: CreateUserDTO) => 
    api.post<User>('/users', data)
  
 export const update= (id: string, data: UpdateUserDTO) => 
    api.put<User>(`/users/${id}`, data)
  
 export const delete= (id: string) => 
    api.delete(`/users/${id}`)

```

### 3. ahooks 数据请求

```typescript
import { useRequest } from 'ahooks'
import { getList } from '@/services/user'

// 自动请求
const { data, loading, error, refresh } = useRequest(
  () => getList({ page: 1 })
)

// 手动触发
const { run, loading } = useRequest(create, {
  manual: true,
  onSuccess: () => {
    message.success('创建成功')
    refresh()
  },
})

// 分页
const { data, loading, pagination } = useRequest(
  ({ current, pageSize }) => 
    getList({ page: current, size: pageSize }),
  { paginated: true }
)

// 防抖搜索
const { run: search } = useRequest(getList, {
  manual: true,
  debounceWait: 300,
})
```

### 4. 组件编写

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

### 5. 自定义 Hook

```typescript
// hooks/useModal.ts
import { useState, useCallback } from 'react'

export const useModal = <T = unknown>(initialData?: T) => {
  const [open, setOpen] = useState(false)
  const [data, setData] = useState<T | undefined>(initialData)

  const show = useCallback((d?: T) => {
    setData(d)
    setOpen(true)
  }, [])

  const hide = useCallback(() => {
    setOpen(false)
    setData(undefined)
  }, [])

  return { open, data, show, hide }
}

// 使用
const editModal = useModal<User>()
// editModal.show(user)
// editModal.hide()
// editModal.open, editModal.data
```

## 业务场景

### 表格 + CRUD (antd)

```typescript
import { Table, Button, Space, Modal, Form, Input, message } from 'antd'
import { useRequest, useAntdTable } from 'ahooks'
import { userService } from '@/services/user'
import { useModal } from '@/hooks/useModal'

const UserList: FC = () => {
  const [form] = Form.useForm()
  const editModal = useModal<User>()
  
  const { tableProps, refresh } = useAntdTable(
    ({ current, pageSize }, formData) =>
      userService.getList({ page: current, size: pageSize, ...formData }),
    { form }
  )

  const { run: deleteUser } = useRequest(userService.delete, {
    manual: true,
    onSuccess: () => {
      message.success('删除成功')
      refresh()
    },
  })

  const columns = [
    { title: '姓名', dataIndex: 'name' },
    { title: '邮箱', dataIndex: 'email' },
    {
      title: '操作',
      render: (_: unknown, record: User) => (
        <Space>
          <Button type="link" onClick={() => editModal.show(record)}>
            编辑
          </Button>
          <Button 
            type="link" 
            danger 
            onClick={() => Modal.confirm({
              title: '确认删除?',
              onOk: () => deleteUser(record.id),
            })}
          >
            删除
          </Button>
        </Space>
      ),
    },
  ]

  return (
    <>
      <Form form={form} layout="inline" className="mb-4">
        <Form.Item name="keyword">
          <Input.Search placeholder="搜索" onSearch={form.submit} />
        </Form.Item>
      </Form>
      
      <Table columns={columns} rowKey="id" {...tableProps} />
      
      <EditModal 
        open={editModal.open} 
        data={editModal.data} 
        onClose={editModal.hide}
        onSuccess={refresh}
      />
    </>
  )
}
```

### 表单提交

```typescript
import { Form, Input, Button, message } from 'antd'
import { useRequest } from 'ahooks'

const CreateUser: FC<{ onSuccess: () => void }> = ({ onSuccess }) => {
  const [form] = Form.useForm()
  
  const { run, loading } = useRequest(userService.create, {
    manual: true,
    onSuccess: () => {
      message.success('创建成功')
      form.resetFields()
      onSuccess()
    },
  })

  return (
    <Form form={form} onFinish={run} layout="vertical">
      <Form.Item 
        name="name" 
        label="姓名" 
        rules={[{ required: true, message: '请输入姓名' }]}
      >
        <Input />
      </Form.Item>
      <Form.Item 
        name="email" 
        label="邮箱" 
        rules={[
          { required: true, message: '请输入邮箱' },
          { type: 'email', message: '邮箱格式错误' },
        ]}
      >
        <Input />
      </Form.Item>
      <Button type="primary" htmlType="submit" loading={loading}>
        创建
      </Button>
    </Form>
  )
}
```

### 编辑弹窗

```typescript
import { Modal, Form, Input, message } from 'antd'
import { useRequest } from 'ahooks'
import { useEffect } from 'react'

interface EditModalProps {
  open: boolean
  data?: User
  onClose: () => void
  onSuccess: () => void
}

const EditModal: FC<EditModalProps> = ({ open, data, onClose, onSuccess }) => {
  const [form] = Form.useForm()
  const isEdit = !!data?.id

  useEffect(() => {
    if (open && data) {
      form.setFieldsValue(data)
    } else {
      form.resetFields()
    }
  }, [open, data])

  const { run, loading } = useRequest(
    (values) => isEdit 
      ? userService.update(data!.id, values) 
      : userService.create(values),
    {
      manual: true,
      onSuccess: () => {
        message.success(isEdit ? '更新成功' : '创建成功')
        onClose()
        onSuccess()
      },
    }
  )

  return (
    <Modal
      title={isEdit ? '编辑用户' : '新建用户'}
      open={open}
      onCancel={onClose}
      onOk={form.submit}
      confirmLoading={loading}
    >
      <Form form={form} onFinish={run} layout="vertical">
        <Form.Item name="name" label="姓名" rules={[{ required: true }]}>
          <Input />
        </Form.Item>
        <Form.Item name="email" label="邮箱" rules={[{ type: 'email' }]}>
          <Input />
        </Form.Item>
      </Form>
    </Modal>
  )
}
```

### 认证状态

```typescript
// stores/useAuthStore.ts
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

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

// 路由守卫
const PrivateRoute: FC<{ children: ReactNode }> = ({ children }) => {
  const isAuth = useAuthStore((s) => s.isAuthenticated)
  if (!isAuth) return <Navigate to="/login" replace />
  return <>{children}</>
}
```

### 列表筛选 + URL 同步

```typescript
import { useSearchParams } from 'react-router-dom'
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

## 工具函数

```typescript
// utils/cn.ts
import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export const cn = (...inputs: ClassValue[]) => twMerge(clsx(inputs))
```

## 类型定义

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

## References

- **shadcn/ui**: <https://ui.shadcn.com/docs/components>
- **antd**: <https://ant.design/components/overview-cn>
- **ahooks**: <https://ahooks.js.org/zh-CN>
- **Zustand**: <https://zustand-demo.pmnd.rs/>
