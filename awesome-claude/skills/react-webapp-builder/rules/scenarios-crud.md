---
name: scenarios-crud
description: Business scenarios for table CRUD, form submission, and edit modal with antd
---

# Business Scenarios - CRUD

## Table + CRUD (antd)

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
      message.success('Deleted')
      refresh()
    },
  })

  const columns = [
    { title: 'Name', dataIndex: 'name' },
    { title: 'Email', dataIndex: 'email' },
    {
      title: 'Actions',
      render: (_: unknown, record: User) => (
        <Space>
          <Button type="link" onClick={() => editModal.show(record)}>
            Edit
          </Button>
          <Button 
            type="link" 
            danger 
            onClick={() => Modal.confirm({
              title: 'Confirm delete?',
              onOk: () => deleteUser(record.id),
            })}
          >
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

## Edit Modal

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
        message.success(isEdit ? 'Updated' : 'Created')
        onClose()
        onSuccess()
      },
    }
  )

  return (
    <Modal
      title={isEdit ? 'Edit User' : 'New User'}
      open={open}
      onCancel={onClose}
      onOk={form.submit}
      confirmLoading={loading}
    >
      <Form form={form} onFinish={run} layout="vertical">
        <Form.Item name="name" label="Name" rules={[{ required: true }]}>
          <Input />
        </Form.Item>
        <Form.Item name="email" label="Email" rules={[{ type: 'email' }]}>
          <Input />
        </Form.Item>
      </Form>
    </Modal>
  )
}
```
