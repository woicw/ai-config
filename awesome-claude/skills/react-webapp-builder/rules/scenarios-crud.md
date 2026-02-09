---
name: scenarios-crud
description: Business scenarios for table CRUD and form submission with antd
---

# Business Scenarios - CRUD

## Table + CRUD (antd)

```typescript
import { Table, Button, Space, message } from 'antd'
import { useRequest, useAntdTable } from 'ahooks'
import { Form, Input } from 'antd'
import { useAntModal } from '@/components/AntdModal'
import { userService } from '@/services/user'

const UserList: FC = () => {
  const [form] = Form.useForm()

  const { tableProps, refresh } = useAntdTable(
    ({ current, pageSize }, formData) =>
      userService.getList({ page: current, size: pageSize, ...formData }),
    { form }
  )

  const { run: deleteUser } = useRequest(userService.delete, {
    manual: true,
    onSuccess: () => {
      message.success('Deleted')
      refresh()
    },
  })

  const { showModal: showDelete } = useAntModal('delete-user')
  const { showModal: showEdit } = useAntModal('user-form')

  const actions=new Map<string, (record: User) => void>([
    ['edit', (record) => showEdit({ title: '编辑用户', mode: 'edit', record, onSuccess: refresh })],
    ['delete', (record) => showDelete({ record })],
  ])

  const columns = [
    { title: 'Name', dataIndex: 'name' },
    { title: 'Email', dataIndex: 'email' },
    {
      title: 'Actions',
      render: (_: unknown, record: User) => (
        <Space>
          <Button type="link" onClick={ actions.get('edit')?.bind(null,record)}>
            Edit
          </Button>
          <Button type="link" danger onClick={ actions.get('delete')?.bind(null,record)}>
            Delete
          </Button>
        </Space>
      ),
    },
  ]

  return (
    <>
      <Form form={form} layout="inline" className="mb-4">
        <Form.Item name="keyword">
          <Input.Search placeholder="Search" onSearch={form.submit} />
        </Form.Item>
      </Form>

      <div className="mb-4">
        <Button type="primary" onClick={() => showEdit({ title: '新增用户', mode: 'create', onSuccess: refresh })}>
          New User
        </Button>
      </div>

      <Table columns={columns} rowKey="id" {...tableProps} />

      {/* Modal 声明式放置，实现见 patterns-modal.md */}
      <UserFormModal />
      <DeleteConfirmModal onConfirm={(record) => deleteUser(record.id)} />
    </>
  )
}
```

> **Modal 相关实现**（AntdModal 封装、表单弹窗、确认弹窗等）详见 [patterns-modal.md](./patterns-modal.md)

## Form Submission

```typescript
import { Form, Input, Button, message } from 'antd'
import { useRequest } from 'ahooks'

const CreateUser: FC<{ onSuccess: () => void }> = ({ onSuccess }) => {
  const [form] = Form.useForm()
  
  const { run, loading } = useRequest(userService.create, {
    manual: true,
    onSuccess: () => {
      message.success('Created')
      form.resetFields()
      onSuccess()
    },
  })

  return (
    <Form form={form} onFinish={run} layout="vertical">
      <Form.Item 
        name="name" 
        label="Name" 
        rules={[{ required: true, message: 'Please enter name' }]}
      >
        <Input />
      </Form.Item>
      <Form.Item 
        name="email" 
        label="Email" 
        rules={[
          { required: true, message: 'Please enter email' },
          { type: 'email', message: 'Invalid email format' },
        ]}
      >
        <Input />
      </Form.Item>
      <Button type="primary" htmlType="submit" loading={loading}>
        Create
      </Button>
    </Form>
  )
}
```
