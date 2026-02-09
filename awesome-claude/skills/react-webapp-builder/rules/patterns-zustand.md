---
name: patterns-zustand
description: Zustand store patterns — UserInfo use case
---

# Zustand Store Patterns — UserInfo 用例实践

## 1. 类型定义

```typescript
// types/user.ts
interface UserInfo {
  id: string
  name: string
  avatar: string
  email: string
  roles: string[]
  permissions: string[]
}
```

## 2. Store 定义

token 由后端通过 httpOnly cookie 管理，前端 store 只负责 userInfo：

```typescript
// stores/useUserStore.ts
import { create } from 'zustand'
import { getUserInfo, loginApi, logoutApi, type LoginParams } from '@/api/user'

interface UserState {
  userInfo: UserInfo | null
  // actions
  login: (params: LoginParams) => Promise<void>
  fetchUserInfo: () => Promise<void>
  logout: () => void
}

export const useUserStore = create<UserState>()((set, get) => ({
  userInfo: null,

  async login(params) {
    await loginApi(params) // 后端 set-cookie
    await get().fetchUserInfo()
  },

  async fetchUserInfo() {
    const userInfo = await getUserInfo()
    set({ userInfo })
  },

  logout() {
    logoutApi() // 后端清除 cookie
    set({ userInfo: null })
  },
}))
```

## 3. Selector 优化

精确选择器避免不必要的重渲染：

```typescript
// ✅ 精确选择所需字段
const userName = useUserStore((s) => s.userInfo?.name)
const roles = useUserStore((s) => s.userInfo?.roles)

// ✅ 派生值用 shallow 比较
import { useShallow } from 'zustand/shallow'

const { name, avatar } = useUserStore(
  useShallow((s) => ({ name: s.userInfo?.name, avatar: s.userInfo?.avatar })),
)

// ❌ 避免：选择整个 state 导致任何字段变化都重渲染
const { userInfo } = useUserStore()
```

## 4. 权限检查 Hook

```typescript
// hooks/usePermission.ts
export function usePermission() {
  const permissions = useUserStore((s) => s.userInfo?.permissions ?? [])
  const roles = useUserStore((s) => s.userInfo?.roles ?? [])

  const hasPermission = (code: string) => permissions.includes(code)
  const hasRole = (role: string) => roles.includes(role)

  return { hasPermission, hasRole }
}
```

## 5. 入口 Layout（鉴权 + 用户初始化）

将路由守卫和用户信息初始化统一放在入口 Layout 中处理：

```typescript
// layouts/BasicLayout.tsx
function BasicLayout() {
  const userInfo = useUserStore((s) => s.userInfo)
  const fetchUserInfo = useUserStore((s) => s.fetchUserInfo)
  const [loading, setLoading] = useState(true)
  const [authFailed, setAuthFailed] = useState(false)

  useEffect(() => {
    if (userInfo) {
      setLoading(false)
      return
    }
    fetchUserInfo()
      .then(() => setLoading(false))
      .catch(() => setAuthFailed(true))
  }, [userInfo, fetchUserInfo])

  // cookie 无效或过期 → 跳转登录页
  if (authFailed) return <Navigate to="/login" replace />

  // 加载用户信息中
  if (loading) return <PageLoading />

  return (
    <div className="flex h-screen">
      <Sidebar />
      <main className="flex-1 overflow-auto">
        <Header />
        <Outlet />
      </main>
    </div>
  )
}
```

路由配置：

```typescript
// router/index.tsx
const router = createBrowserRouter([
  {
    path: '/login',
    element: <LoginPage />,
  },
  {
    path: '/',
    element: <BasicLayout />,
    children: [
      { index: true, element: <DashboardPage /> },
      { path: 'users', element: <UserListPage /> },
      // ...其他需要鉴权的页面
    ],
  },
])
```

## 7. 响应拦截器（401 处理）

token 在 cookie 中由浏览器自动携带，请求拦截器无需手动注入。只需处理 401：

```typescript
// utils/request.ts
import axios from 'axios'
import { useUserStore } from '@/stores/useUserStore'

const request = axios.create({ baseURL: '/api' })

request.interceptors.response.use(undefined, (error) => {
  if (error.response?.status === 401) {
    useUserStore.getState().logout()
    window.location.href = '/login'
  }
  return Promise.reject(error)
})
```
