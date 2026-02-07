---
name: patterns-data-fetching
description: API service setup with axios and data fetching patterns with ahooks
---

# API Service & Data Fetching

## Axios Instance

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

## Service Module

```typescript
// services/user.ts
import api from './api'

export const getList = (params: UserListParams) => 
  api.get<UserListResponse>('/users', { params })

export const getById = (id: string) => 
  api.get<User>(`/users/${id}`)

export const create = (data: CreateUserDTO) => 
  api.post<User>('/users', data)

export const update = (id: string, data: UpdateUserDTO) => 
  api.put<User>(`/users/${id}`, data)

export const remove = (id: string) => 
  api.delete(`/users/${id}`)
```

## ahooks useRequest

### Auto Request

```typescript
import { useRequest } from 'ahooks'
import { getList } from '@/services/user'

const { data, loading, error, refresh } = useRequest(
  () => getList({ page: 1 })
)
```

### Manual Trigger

```typescript
const { run, loading } = useRequest(create, {
  manual: true,
  onSuccess: () => {
    message.success('Created')
    refresh()
  },
})
```

### Pagination

```typescript
const { data, loading, pagination } = useRequest(
  ({ current, pageSize }) => 
    getList({ page: current, size: pageSize }),
  { paginated: true }
)
```

### Debounced Search

```typescript
const { run: search } = useRequest(getList, {
  manual: true,
  debounceWait: 300,
})
```
