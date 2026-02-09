---
name: patterns-modal
description: AntdModal patterns — Context-based modal management with form integration
---

# AntdModal Patterns — 基于 Context 的弹窗管理

基于 React Context + `useSyncExternalStore` 的 Modal 封装，支持命令式控制、泛型 options 透传、精确订阅。

核心理念：

- **声明式摆放** — `<AntdModal mid="xxx">` 放在页面中声明 Modal 结构
- **命令式控制** — `useAntModal('xxx')` 返回 `showModal / closeModal` 控制开关
- **Options 透传** — `showModal({ record })` 传递运行时数据给 Modal 子组件
- **精确订阅** — 每个 Modal 独立订阅，互不影响重渲染

## 1. 完整实现

### 1.1 类型定义

```typescript
// components/AntdModal/types.ts
import type { ModalProps } from 'antd'

/**
 * AntdModal 的 options 类型
 * 包含 antd ModalProps（排除 open）+ 任意自定义字段（可透传给 children）
 */
export type AntdModalOptions = Partial<Omit<ModalProps, 'open'>> &
  Record<string, unknown>

/** Context 中每个 Modal 的状态 */
export interface ModalEntry {
  open: boolean
  /** 来自 useAntModal hook 的 options，优先级高于 AntdModal 组件 props */
  hookOptions: AntdModalOptions
}

/** Context API */
export interface ContextApi {
  getEntry: (mid: string) => ModalEntry
  show: (mid: string, options?: AntdModalOptions) => void
  close: (mid: string) => void
  update: (mid: string, options: AntdModalOptions) => void
  subscribe: (mid: string, cb: () => void) => () => void
}

export const EMPTY_ENTRY: ModalEntry = Object.freeze({
  open: false,
  hookOptions: {},
})
```

### 1.2 Context & Provider

```typescript
// components/AntdModal/context.tsx
import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useRef,
  useSyncExternalStore,
  type PropsWithChildren,
} from 'react'
import type { ContextApi, ModalEntry } from './types'
import { EMPTY_ENTRY } from './types'

/* ======================== Global Context ======================== */

const Ctx = createContext<ContextApi | null>(null)

export const useCtx = () => {
  const ctx = useContext(Ctx)
  if (!ctx) throw new Error('[AntdModal] 需要在外层包裹 <AntdModalProvider>')
  return ctx
}

/* ======================== Provider ======================== */

export const AntdModalProvider = ({ children }: PropsWithChildren) => {
  const entries = useRef<Record<string, ModalEntry>>({})
  const subs = useRef<Record<string, Set<() => void>>>({})

  const emit = useCallback((mid: string) => {
    subs.current[mid]?.forEach((fn) => fn())
  }, [])

  const api = useMemo<ContextApi>(
    () => ({
      getEntry: (mid) => entries.current[mid] ?? EMPTY_ENTRY,

      show(mid, options) {
        const prev = entries.current[mid]
        entries.current[mid] = {
          open: true,
          hookOptions:
            options !== undefined ? options : (prev?.hookOptions ?? {}),
        }
        emit(mid)
      },

      close(mid) {
        const prev = entries.current[mid]
        if (!prev) return
        entries.current[mid] = { ...prev, open: false }
        emit(mid)
      },

      update(mid, options) {
        const prev = entries.current[mid] ?? { open: false, hookOptions: {} }
        entries.current[mid] = {
          ...prev,
          hookOptions: { ...prev.hookOptions, ...options },
        }
        emit(mid)
      },

      subscribe(mid, cb) {
        (subs.current[mid] ??= new Set()).add(cb)
        return () => {
          subs.current[mid]?.delete(cb)
        }
      },
    }),
    [emit],
  )

  return <Ctx.Provider value={api}>{children}</Ctx.Provider>
}

/* ======================== Mid Context ======================== */

/**
 * 内部 Context：AntdModal 仅注入 mid 字符串
 * value 是稳定的 string，不会因 options 变化触发额外重渲染
 */
export const MidCtx = createContext<string | null>(null)

/* ======================== Internal Hooks ======================== */

/** 订阅指定 mid 的状态，仅在该 mid 变化时触发重渲染 */
export const useModalEntry = (mid: string): ModalEntry => {
  const api = useCtx()

  const subscribe = useCallback(
    (cb: () => void) => api.subscribe(mid, cb),
    [api, mid],
  )
  const getSnapshot = useCallback(() => api.getEntry(mid), [api, mid])

  return useSyncExternalStore(subscribe, getSnapshot, () => EMPTY_ENTRY)
}
```

### 1.3 useAntModal Hook

```typescript
// components/AntdModal/useAntModal.ts
import { useCallback, useEffect, useMemo, useRef } from 'react'
import { useCtx, useModalEntry } from './context'
import type { AntdModalOptions } from './types'

export interface UseAntModalReturn {
  /** 打开弹窗，可传入运行时一次性 options（与 hook 默认 options 合并） */
  showModal: (runtimeOptions?: AntdModalOptions) => void
  /** 关闭弹窗 */
  closeModal: () => void
  /** 切换弹窗显隐 */
  toggleModal: () => void
  /** 增量更新 hook options（不改变 open 状态） */
  setOptions: (options: AntdModalOptions) => void
  /** 当前是否打开 */
  open: boolean
}

/**
 * 用于命令式控制 AntdModal 的 Hook
 *
 * @param mid - 唯一标识，对应 <AntdModal mid={mid}> 组件
 * @param options - 默认 options，优先级高于 AntdModal 组件 props，
 *                  支持 Modal 原生 props 和自定义字段（透传给 children）
 */
export const useAntModal = (
  mid: string,
  options?: AntdModalOptions,
): UseAntModalReturn => {
  const api = useCtx()
  const entry = useModalEntry(mid)
  const optsRef = useRef(options)

  useEffect(() => {
    optsRef.current = options
  })

  const showModal = useCallback(
    (runtime?: AntdModalOptions) => {
      const hasOpts = optsRef.current || runtime
      api.show(mid, hasOpts ? { ...optsRef.current, ...runtime } : undefined)
    },
    [api, mid],
  )

  const closeModal = useCallback(() => api.close(mid), [api, mid])

  const toggleModal = useCallback(() => {
    if (api.getEntry(mid).open) {
      api.close(mid)
    } else {
      const hasOpts = optsRef.current
      api.show(mid, hasOpts ? optsRef.current : undefined)
    }
  }, [api, mid])

  const setOptions = useCallback(
    (o: AntdModalOptions) => api.update(mid, o),
    [api, mid],
  )

  return useMemo(
    () => ({ showModal, closeModal, toggleModal, setOptions, open: entry.open }),
    [showModal, closeModal, toggleModal, setOptions, entry.open],
  )
}
```

### 1.4 useOptions Hook

```typescript
// components/AntdModal/useOptions.ts
import { useContext } from 'react'
import { MidCtx, useModalEntry } from './context'
import type { AntdModalOptions } from './types'

/**
 * 在 AntdModal 子组件中获取当前 Modal 的 hookOptions，无需传 mid
 *
 * 内部通过 MidCtx 拿到 mid，再用 useSyncExternalStore 精确订阅，
 * 仅在当前 mid 的 hookOptions 变化时触发重渲染
 */
export const useOptions = <
  T extends Record<string, unknown> = AntdModalOptions,
>(): T => {
  const mid = useContext(MidCtx)
  if (mid === null) {
    throw new Error('[useOptions] 只能在 <AntdModal> 的子组件中使用')
  }
  const { hookOptions } = useModalEntry(mid)
  return hookOptions as T
}
```

### 1.5 AntdModal 组件

```typescript
// components/AntdModal/AntdModal.tsx
import type { ModalProps } from 'antd'
import { Modal } from 'antd'
import type { ReactNode } from 'react'
import { useCallback, useMemo } from 'react'
import { MidCtx, useCtx, useModalEntry } from './context'
import type { AntdModalOptions } from './types'

/* ======================== Modal Props 白名单 ======================== */

/** antd Modal 可接受的 prop keys，用于过滤自定义字段 */
const MODAL_PROP_KEYS: ReadonlySet<string> = new Set([
  // 基础
  'open', 'title', 'footer', 'width', 'centered', 'forceRender',
  'destroyOnClose', 'destroyOnHidden', 'loading',
  // 按钮
  'confirmLoading', 'okText', 'okType', 'okButtonProps',
  'cancelText', 'cancelButtonProps',
  // 回调
  'onOk', 'onCancel', 'afterClose', 'afterOpenChange',
  // 遮罩 & 关闭
  'mask', 'maskClosable', 'keyboard', 'closable', 'closeIcon',
  // 样式
  'className', 'rootClassName', 'wrapClassName', 'prefixCls',
  'style', 'rootStyle', 'bodyStyle', 'maskStyle',
  'styles', 'classNames',
  // 其他
  'zIndex', 'getContainer', 'modalRender', 'mousePosition',
  'wrapProps', 'transitionName', 'maskTransitionName',
  'focusTriggerAfterClose', 'focusable',
])

/** 从对象中只取 Modal 可接受的 props */
const pickModalProps = (obj: Record<string, unknown>): Partial<ModalProps> => {
  const result: Record<string, unknown> = {}
  for (const key of Object.keys(obj)) {
    if (MODAL_PROP_KEYS.has(key)) {
      result[key] = obj[key]
    }
  }
  return result as Partial<ModalProps>
}

/* ======================== AntdModal ======================== */

export interface AntdModalProps<
  T extends Record<string, unknown> = AntdModalOptions,
> extends Partial<Omit<ModalProps, 'open' | 'children'>> {
  /** Context 中的唯一标识 */
  mid: string
  /**
   * 支持 ReactNode 或 render function
   * render function 接收合并后的 hookOptions，泛型 T 可约束自定义字段类型
   */
  children?: ReactNode | ((options: T) => ReactNode)
}

/**
 * 受 Context 管理的 Modal 组件
 *
 * - `mid` 为唯一标识，与 useAntModal(mid) 配对使用
 * - 组件 props 作为基础配置，useAntModal 的 options 优先级更高
 * - 点击取消/遮罩/ESC 时自动关闭
 */
export const AntdModal = <
  T extends Record<string, unknown> = AntdModalOptions,
>({
  mid,
  children,
  ...componentProps
}: AntdModalProps<T>) => {
  const api = useCtx()
  const { open, hookOptions } = useModalEntry(mid)

  const hookModalProps = pickModalProps(hookOptions)

  const userOnCancel = (hookModalProps.onCancel ?? componentProps.onCancel) as
    | ModalProps['onCancel']
    | undefined
  const stableOnCancel = useCallback(
    (...args: Parameters<NonNullable<ModalProps['onCancel']>>) => {
      userOnCancel?.(...args)
      api.close(mid)
    },
    [api, mid, userOnCancel],
  )

  // 合并 props: 组件 props (低优先级) < hook Modal props (高优先级)
  const merged = useMemo<Partial<ModalProps>>(
    () => ({
      ...componentProps,
      ...hookModalProps,
      open,
      onCancel: stableOnCancel,
    }),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [open, hookOptions, stableOnCancel],
  )

  const renderedChildren =
    typeof children === 'function' ? children(hookOptions as T) : children

  return (
    <Modal {...(merged as ModalProps)}>
      <MidCtx.Provider value={mid}>{renderedChildren}</MidCtx.Provider>
    </Modal>
  )
}
```

### 1.6 导出

```typescript
// components/AntdModal/index.ts
export type { AntdModalOptions } from './types'
export { AntdModalProvider } from './context'
export { useAntModal, type UseAntModalReturn } from './useAntModal'
export { useOptions } from './useOptions'
export { AntdModal, type AntdModalProps } from './AntdModal'
```

## 2. Provider 配置

在应用入口包裹 `AntdModalProvider`：

```typescript
// main.tsx 或 App.tsx
import { AntdModalProvider } from '@/components/AntdModal'

function App() {
  return (
    <AntdModalProvider>
      <RouterProvider router={router} />
    </AntdModalProvider>
  )
}
```

## 3. 常规 Modal 用例

### 3.1 基础确认弹窗

```typescript
// pages/UserList.tsx
import { Button, message, Space } from 'antd'
import { AntdModal, useAntModal } from '@/components/AntdModal'
import type { User } from '@/types/user'

const UserList = () => {
  const { showModal: showDelete, closeModal: closeDelete } = useAntModal('delete-user', {
    title: '删除确认',
    width: 420,
  })

  const handleDelete = async (user: User) => {
    showDelete({ record: user })
  }

  const handleConfirmDelete = async () => {
    // 从 render function 中获取 record，见下方 AntdModal
    closeDelete()
    message.success('删除成功')
  }

  return (
    <>
      <Table
        dataSource={users}
        columns={[
          // ...其他列
          {
            title: '操作',
            render: (_, record) => (
              <Button danger onClick={() => handleDelete(record)}>删除</Button>
            ),
          },
        ]}
      />

      <AntdModal<{ record: User }> mid="delete-user" onOk={handleConfirmDelete}>
        {(opts) => (
          <p>确认删除用户 <strong>{opts.record?.name}</strong> 吗？此操作不可恢复。</p>
        )}
      </AntdModal>
    </>
  )
}
```

### 3.2 详情预览弹窗

```typescript
// pages/OrderList.tsx
import { Descriptions } from 'antd'
import { AntdModal, useAntModal, useOptions } from '@/components/AntdModal'
import type { Order } from '@/types/order'

// 子组件通过 useOptions 获取数据，无需 props 传递
const OrderDetail = () => {
  const { record } = useOptions<{ record: Order }>()

  return (
    <Descriptions column={2} bordered>
      <Descriptions.Item label="订单号">{record?.orderNo}</Descriptions.Item>
      <Descriptions.Item label="金额">{record?.amount}</Descriptions.Item>
      <Descriptions.Item label="状态">{record?.status}</Descriptions.Item>
      <Descriptions.Item label="创建时间">{record?.createdAt}</Descriptions.Item>
    </Descriptions>
  )
}

const OrderList = () => {
  const { showModal } = useAntModal('order-detail', {
    title: '订单详情',
    width: 640,
    footer: null,
  })

  return (
    <>
      <Table
        dataSource={orders}
        columns={[
          // ...
          {
            title: '操作',
            render: (_, record) => (
              <Button type="link" onClick={() => showModal({ record })}>
                查看详情
              </Button>
            ),
          },
        ]}
      />

      <AntdModal mid="order-detail">
        <OrderDetail />
      </AntdModal>
    </>
  )
}
```

## 4. Modal 表单用例

### 4.1 新增/编辑共用表单弹窗

```typescript
// pages/UserManage/UserFormModal.tsx
import { Form, Input, Select, message } from 'antd'
import { useRequest } from 'ahooks'
import { AntdModal, useAntModal, useOptions } from '@/components/AntdModal'
import { createUser, updateUser } from '@/api/user'
import type { User } from '@/types/user'

interface UserFormOptions {
  mode: 'create' | 'edit'
  record?: User
}

const UserForm = () => {
  const { mode, record } = useOptions<UserFormOptions>()
  const [form] = Form.useForm()

  // 编辑模式下回填表单
  useEffect(() => {
    if (mode === 'edit' && record) {
      form.setFieldsValue(record)
    } else {
      form.resetFields()
    }
  }, [mode, record, form])

  return (
    <Form form={form} layout="vertical" name="userForm">
      <Form.Item name="name" label="姓名" rules={[{ required: true, message: '请输入姓名' }]}>
        <Input placeholder="请输入姓名" />
      </Form.Item>
      <Form.Item name="email" label="邮箱" rules={[{ required: true, type: 'email' }]}>
        <Input placeholder="请输入邮箱" />
      </Form.Item>
      <Form.Item name="role" label="角色" rules={[{ required: true }]}>
        <Select
          placeholder="请选择角色"
          options={[
            { label: '管理员', value: 'admin' },
            { label: '普通用户', value: 'user' },
          ]}
        />
      </Form.Item>
    </Form>
  )
}
```

```typescript
// pages/UserManage/index.tsx
import { Button, Space, message } from 'antd'
import { useRequest } from 'ahooks'
import { AntdModal, useAntModal } from '@/components/AntdModal'
import { createUser, updateUser, getUserList } from '@/api/user'
import type { User } from '@/types/user'
import { UserForm } from './UserFormModal'

const UserManage = () => {
  const formRef = useRef<FormInstance>(null)

  const { data, refresh } = useRequest(getUserList)

  const { showModal, closeModal } = useAntModal('user-form', {
    width: 520,
    destroyOnClose: true,
  })

  const { run: submitForm, loading } = useRequest(
    async (values: Partial<User>, mode: 'create' | 'edit', id?: string) => {
      if (mode === 'create') {
        await createUser(values)
        message.success('创建成功')
      } else {
        await updateUser(id!, values)
        message.success('更新成功')
      }
    },
    {
      manual: true,
      onSuccess: () => {
        closeModal()
        refresh()
      },
    },
  )

  const handleAdd = () => {
    showModal({
      title: '新增用户',
      mode: 'create',
    })
  }

  const handleEdit = (record: User) => {
    showModal({
      title: '编辑用户',
      mode: 'edit',
      record,
    })
  }

  // Modal onOk 触发表单提交
  const handleOk = async () => {
    const values = await formRef.current?.validateFields()
    const opts = useAntModal // 此处通过 render function 获取
    // 见下方完整方案
  }

  return (
    <>
      <div className="mb-4">
        <Button type="primary" onClick={handleAdd}>新增用户</Button>
      </div>

      <Table
        dataSource={data?.list}
        columns={[
          { title: '姓名', dataIndex: 'name' },
          { title: '邮箱', dataIndex: 'email' },
          { title: '角色', dataIndex: 'role' },
          {
            title: '操作',
            render: (_, record) => (
              <Space>
                <Button type="link" onClick={() => handleEdit(record)}>编辑</Button>
              </Space>
            ),
          },
        ]}
      />

      {/* render function 方式：直接获取 mode/record */}
      <AntdModal<{ mode: 'create' | 'edit'; record?: User }>
        mid="user-form"
        confirmLoading={loading}
        onOk={async () => {
          const values = await formRef.current?.validateFields()
          // 从 getEntry 拿到当前 options 不可行，推荐用 ref 方案
        }}
      >
        {(opts) => <UserForm ref={formRef} mode={opts.mode} record={opts.record} />}
      </AntdModal>
    </>
  )
}
```

### 4.2 推荐方案：表单 Modal 封装（内聚 onOk）

将表单验证和提交逻辑内聚到子组件，通过 `onSuccess` 回调通知外部：

```typescript
// components/UserFormModal.tsx
import { Form, Input, Select, message } from 'antd'
import { useRequest } from 'ahooks'
import { AntdModal, useAntModal, useOptions } from '@/components/AntdModal'
import { createUser, updateUser } from '@/api/user'
import type { User } from '@/types/user'

interface FormModalOptions {
  mode: 'create' | 'edit'
  record?: User
  onSuccess?: () => void
}

/** 内部表单组件 — 内聚验证 + 提交逻辑 */
const InnerForm = () => {
  const { mode, record, onSuccess } = useOptions<FormModalOptions>()
  const [form] = Form.useForm()
  const { closeModal } = useAntModal('user-form')

  useEffect(() => {
    if (mode === 'edit' && record) {
      form.setFieldsValue(record)
    } else {
      form.resetFields()
    }
  }, [mode, record, form])

  const { run: handleSubmit, loading } = useRequest(
    async () => {
      const values = await form.validateFields()
      if (mode === 'create') {
        await createUser(values)
        message.success('创建成功')
      } else {
        await updateUser(record!.id, values)
        message.success('更新成功')
      }
    },
    {
      manual: true,
      onSuccess: () => {
        closeModal()
        onSuccess?.()
      },
    },
  )

  return (
    <>
      {/* 通过 setOptions 上报 loading 状态给 Modal confirmLoading */}
      <AntdModalConfirmLoading loading={loading} />
      <Form form={form} layout="vertical">
        <Form.Item name="name" label="姓名" rules={[{ required: true }]}>
          <Input placeholder="请输入姓名" />
        </Form.Item>
        <Form.Item name="email" label="邮箱" rules={[{ required: true, type: 'email' }]}>
          <Input placeholder="请输入邮箱" />
        </Form.Item>
        <Form.Item name="role" label="角色" rules={[{ required: true }]}>
          <Select
            placeholder="请选择角色"
            options={[
              { label: '管理员', value: 'admin' },
              { label: '普通用户', value: 'user' },
            ]}
          />
        </Form.Item>
      </Form>
    </>
  )
}

// 同步 loading → confirmLoading 的辅助组件
const AntdModalConfirmLoading = ({ loading }: { loading: boolean }) => {
  const { setOptions } = useAntModal('user-form')
  useEffect(() => {
    setOptions({ confirmLoading: loading })
  }, [loading, setOptions])
  return null
}
```

上面的方案过于复杂，**推荐的最佳实践**是 `footer` 自定义 + 表单内聚：

```typescript
// components/UserFormModal.tsx — 最佳实践
import { Button, Form, Input, Select, Space, message } from 'antd'
import { useRequest } from 'ahooks'
import { AntdModal, useAntModal, useOptions } from '@/components/AntdModal'
import { createUser, updateUser } from '@/api/user'
import type { User } from '@/types/user'

interface FormModalOptions {
  mode: 'create' | 'edit'
  record?: User
  onSuccess?: () => void
}

const UserFormContent = () => {
  const { mode, record, onSuccess } = useOptions<FormModalOptions>()
  const { closeModal } = useAntModal('user-form')
  const [form] = Form.useForm()

  useEffect(() => {
    if (mode === 'edit' && record) {
      form.setFieldsValue(record)
    } else {
      form.resetFields()
    }
  }, [mode, record, form])

  const { run: handleSubmit, loading } = useRequest(
    async () => {
      const values = await form.validateFields()
      mode === 'create'
        ? await createUser(values)
        : await updateUser(record!.id, values)
    },
    {
      manual: true,
      onSuccess: () => {
        message.success(mode === 'create' ? '创建成功' : '更新成功')
        closeModal()
        onSuccess?.()
      },
    },
  )

  return (
    <>
      <Form form={form} layout="vertical">
        <Form.Item name="name" label="姓名" rules={[{ required: true }]}>
          <Input placeholder="请输入姓名" />
        </Form.Item>
        <Form.Item name="email" label="邮箱" rules={[{ required: true, type: 'email' }]}>
          <Input placeholder="请输入邮箱" />
        </Form.Item>
        <Form.Item name="role" label="角色" rules={[{ required: true }]}>
          <Select
            placeholder="请选择角色"
            options={[
              { label: '管理员', value: 'admin' },
              { label: '普通用户', value: 'user' },
            ]}
          />
        </Form.Item>
      </Form>
      {/* 自定义 footer 内聚提交逻辑 */}
      <div className="flex justify-end gap-2 mt-4">
        <Button onClick={closeModal}>取消</Button>
        <Button type="primary" loading={loading} onClick={handleSubmit}>
          确定
        </Button>
      </div>
    </>
  )
}

/** 用户表单弹窗 — 页面中声明式使用 */
export const UserFormModal = () => (
  <AntdModal mid="user-form" footer={null} width={520} destroyOnClose>
    <UserFormContent />
  </AntdModal>
)
```

### 4.3 页面使用表单弹窗

```typescript
// pages/UserManage/index.tsx
import { Button, Space, Table } from 'antd'
import { useRequest } from 'ahooks'
import { useAntModal } from '@/components/AntdModal'
import { getUserList } from '@/api/user'
import { UserFormModal } from '@/components/UserFormModal'
import type { User } from '@/types/user'

const UserManage = () => {
  const { data, refresh } = useRequest(getUserList)

  const { showModal } = useAntModal('user-form')

  const handleAdd = () => {
    showModal({ title: '新增用户', mode: 'create', onSuccess: refresh })
  }

  const handleEdit = (record: User) => {
    showModal({ title: '编辑用户', mode: 'edit', record, onSuccess: refresh })
  }

  return (
    <>
      <div className="mb-4">
        <Button type="primary" onClick={handleAdd}>新增用户</Button>
      </div>

      <Table
        dataSource={data?.list}
        rowKey="id"
        columns={[
          { title: '姓名', dataIndex: 'name' },
          { title: '邮箱', dataIndex: 'email' },
          { title: '角色', dataIndex: 'role' },
          {
            title: '操作',
            render: (_, record: User) => (
              <Space>
                <Button type="link" onClick={() => handleEdit(record)}>编辑</Button>
              </Space>
            ),
          },
        ]}
      />

      {/* 声明式放置，不关心开关逻辑 */}
      <UserFormModal />
    </>
  )
}
```

## 5. 最佳实践

### 命名规范

| 场景 | mid 命名 | 示例 |
|------|---------|------|
| CRUD 表单 | `{entity}-form` | `user-form`, `order-form` |
| 删除确认 | `delete-{entity}` | `delete-user` |
| 详情预览 | `{entity}-detail` | `order-detail` |
| 自定义 | `{page}-{action}` | `dashboard-export` |

### 优先级

```
组件 props (AntdModal) < hook 默认 options (useAntModal) < 运行时 options (showModal)
```

### 注意事项

- **Provider 位置**：`AntdModalProvider` 在应用最外层，确保所有 Modal 可被管理
- **destroyOnClose**：表单弹窗建议开启，避免表单状态残留
- **footer={null}**：表单弹窗推荐自定义 footer，将提交逻辑内聚到子组件
- **泛型约束**：使用 `AntdModal<T>` 和 `useOptions<T>` 获得类型安全的 options
- **onSuccess 回调**：通过 options 传入回调函数，Modal 关闭后刷新列表数据
