---
name: antd-modal
description: Ant Design Modal component for displaying dialog boxes, confirmations, and forms. Use when building modals, dialogs, confirmations, or any overlay content.
---

# Modal Component

Modal is a core component in Ant Design for displaying dialogs, confirmations, and forms, providing both declarative and imperative usage patterns.

## Basic Usage (Declarative)

```tsx
import { Modal, Button } from 'antd';
import { useState } from 'react';

const BasicModal = () => {
  const [open, setOpen] = useState(false);

  return (
    <>
      <Button type="primary" onClick={() => setOpen(true)}>
        Open Modal
      </Button>
      <Modal
        title="Basic Modal"
        open={open}
        onOk={() => setOpen(false)}
        onCancel={() => setOpen(false)}
      >
        <p>Some contents...</p>
      </Modal>
    </>
  );
};
```

## Imperative API

### Using App.useApp() (Recommended)

```tsx
import { Modal, Button, App } from 'antd';
import { ExclamationCircleOutlined } from '@ant-design/icons';

const ModalWithHooks = () => {
  const { modal } = App.useApp();

  const showConfirm = () => {
    modal.confirm({
      title: 'Do you want to delete this item?',
      icon: <ExclamationCircleOutlined />,
      content: 'This action cannot be undone.',
      okText: 'Yes, Delete',
      okType: 'danger',
      cancelText: 'Cancel',
      onOk() {
        return new Promise((resolve) => {
          setTimeout(() => {
            console.log('Item deleted');
            resolve(true);
          }, 1000);
        });
      },
      onCancel() {
        console.log('Cancelled');
      },
    });
  };

  return (
    <App>
      <Button onClick={showConfirm}>Show Confirm</Button>
    </App>
  );
};
```

### Promise Support

```tsx
const { modal } = App.useApp();

// Returns true when clicking onOk, false when clicking onCancel
const confirmed = await modal.confirm({
  title: 'Confirm Action',
  content: 'Do you want to proceed?',
});

if (confirmed) {
  console.log('User confirmed');
} else {
  console.log('User cancelled');
}
```

### Static Methods

```tsx
import { Modal } from 'antd';

// Info message
Modal.info({
  title: 'Information',
  content: 'This is an informational message.',
});

// Success message
Modal.success({
  title: 'Success',
  content: 'Operation completed successfully.',
});

// Error message
Modal.error({
  title: 'Error',
  content: 'Something went wrong.',
});

// Warning message
Modal.warning({
  title: 'Warning',
  content: 'This action may have consequences.',
});
```

## Modal Properties

### Basic Properties

- **open** (boolean) - Whether to show modal
- **title** (ReactNode) - Title
- **footer** (ReactNode | null) - Footer content, set to null to hide footer
- **width** (string | number) - Modal width, default 520px
- **centered** (boolean) - Whether to center vertically
- **mask** (boolean) - Whether to show mask, default true
- **maskClosable** (boolean) - Whether to close on mask click, default true
- **closable** (boolean) - Whether to show close button in top right, default true
- **closeIcon** (ReactNode) - Custom close icon
- **zIndex** (number) - Modal z-index

### Event Callbacks

- **onOk** ((e: MouseEvent) => void | Promise) - Callback when OK button is clicked
- **onCancel** ((e: MouseEvent) => void) - Callback when Cancel button is clicked
- **afterOpenChange** ((open: boolean) => void) - Callback after modal opens/closes
- **afterClose** (() => void) - Callback after modal is completely closed

### Style Related

- **className** (string) - Modal container class name
- **wrapClassName** (string) - Modal wrapper class name
- **style** (CSSProperties) - Modal container style
- **maskStyle** (CSSProperties) - Mask style
- **bodyStyle** (CSSProperties) - Modal body style
- **destroyOnClose** (boolean) - Destroy child elements on close, default false

### Others

- **keyboard** (boolean) - Whether to support ESC to close, default true
- **confirmLoading** (boolean) - OK button loading state
- **okText** (ReactNode) - OK button text
- **okType** (string) - OK button type, default 'primary'
- **okButtonProps** (ButtonProps) - OK button properties
- **cancelText** (ReactNode) - Cancel button text
- **cancelButtonProps** (ButtonProps) - Cancel button properties
- **forceRender** (boolean) - Force render Modal, default false

## Form Integration

### Using Form in Modal

```tsx
import { Modal, Form, Input, Button } from 'antd';

const ModalWithForm = () => {
  const [open, setOpen] = useState(false);
  const [confirmLoading, setConfirmLoading] = useState(false);
  const [form] = Form.useForm();

  const handleOk = async () => {
    try {
      const values = await form.validateFields();
      setConfirmLoading(true);

      // Simulate API call
      await new Promise((resolve) => setTimeout(resolve, 1500));

      console.log('Form values:', values);
      form.resetFields();
      setOpen(false);
    } catch (error) {
      console.log('Validation failed:', error);
    } finally {
      setConfirmLoading(false);
    }
  };

  const handleCancel = () => {
    form.resetFields();
    setOpen(false);
  };

  return (
    <>
      <Button type="primary" onClick={() => setOpen(true)}>
        Create User
      </Button>
      <Modal
        title="Create New User"
        open={open}
        onOk={handleOk}
        confirmLoading={confirmLoading}
        onCancel={handleCancel}
        okText="Create"
        cancelText="Cancel"
      >
        <Form form={form} layout="vertical">
          <Form.Item name="name" label="Name" rules={[{ required: true }]}>
            <Input placeholder="Enter name" />
          </Form.Item>
          <Form.Item name="email" label="Email" rules={[{ required: true, type: 'email' }]}>
            <Input placeholder="Enter email" />
          </Form.Item>
        </Form>
      </Modal>
    </>
  );
};
```

## Custom Footer Buttons

```tsx
<Modal
  title="Custom Footer"
  open={open}
  onCancel={() => setOpen(false)}
  footer={[
    <Button key="back" onClick={() => setOpen(false)}>
      Return
    </Button>,
    <Button key="submit" type="primary" loading={loading} onClick={handleSubmit}>
      Submit
    </Button>,
  ]}
>
  <p>Some contents...</p>
</Modal>

// Or hide footer
<Modal
  title="No Footer"
  open={open}
  footer={null}
  onCancel={() => setOpen(false)}
>
  <p>Some contents...</p>
</Modal>
```

## Async Operations

```tsx
const handleOk = () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      console.log('Async operation completed');
      resolve(true);
    }, 2000);
  });
};

<Modal
  open={open}
  onOk={handleOk}
  onCancel={() => setOpen(false)}
>
  <p>This modal will close after async operation completes.</p>
</Modal>
```

## Modal.useModal() Hook

```tsx
import { Modal } from 'antd';

const ModalWithHook = () => {
  const [modal, contextHolder] = Modal.useModal();

  React.useEffect(() => {
    modal.confirm({
      title: 'Confirm',
      content: 'Are you sure?',
      onOk() {
        console.log('OK');
      },
    });
  }, []);

  return <div>{contextHolder}</div>;
};
```

## Confirmation Dialog Types

### confirm

```tsx
modal.confirm({
  title: 'Confirm',
  content: 'Are you sure you want to delete this item?',
  okText: 'Yes',
  cancelText: 'No',
  onOk() {
    // Delete operation
  },
});
```

### info

```tsx
modal.info({
  title: 'Information',
  content: 'This is an informational message.',
});
```

### success

```tsx
modal.success({
  title: 'Success',
  content: 'Operation completed successfully.',
});
```

### error

```tsx
modal.error({
  title: 'Error',
  content: 'Something went wrong. Please try again.',
});
```

### warning

```tsx
modal.warning({
  title: 'Warning',
  content: 'This action may have consequences.',
});
```

## Best Practices

1. **Use App.useApp()** - Use hook to get modal instance in functional components, supports context
2. **Handle async operations** - Return Promise in onOk to handle async operations
3. **Form validation** - When using Form in Modal, ensure proper validation and reset handling
4. **Performance optimization** - Use destroyOnClose to destroy unnecessary content on close
5. **User experience** - Use confirmLoading to show loading state
6. **Accessibility** - Ensure Modal has appropriate title and focus management

<!--
Source references:
- https://ant.design/components/modal-cn
- https://github.com/ant-design/ant-design/blob/master/components/modal/index.en-US.md
-->
