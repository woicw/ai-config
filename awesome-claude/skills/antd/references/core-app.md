---
name: antd-app
description: Ant Design App component for providing context to static methods like message, notification, and modal. Use when building applications that need context-aware static method calls.
---

# App Component

App is a wrapper component introduced in Ant Design 5.x to provide context support for static methods (message, notification, modal), ensuring these methods can correctly access context information such as theme and locale.

## Basic Usage

```tsx
import { App, Button } from 'antd';

const MyPage = () => {
  const { message, notification, modal } = App.useApp();

  const showMessage = () => {
    message.success('Operation successful!');
  };

  const showNotification = () => {
    notification.info({
      title: 'Notification',
      description: 'This is a notification message.',
    });
  };

  const showModal = () => {
    modal.confirm({
      title: 'Confirm',
      content: 'Are you sure?',
    });
  };

  return (
    <div>
      <Button onClick={showMessage}>Show Message</Button>
      <Button onClick={showNotification}>Show Notification</Button>
      <Button onClick={showModal}>Show Modal</Button>
    </div>
  );
};

const MyApp = () => (
  <App>
    <MyPage />
  </App>
);

export default MyApp;
```

## App.useApp() Hook

`App.useApp()` 返回一个对象，包含 `message`、`notification` 和 `modal` 三个实例：

```tsx
const { message, notification, modal } = App.useApp();
```

### message Instance

```tsx
const { message } = App.useApp();

// Success message
message.success('Operation completed successfully!');

// Error message
message.error('Something went wrong!');

// Warning message
message.warning('This action may have consequences');

// Info message
message.info('Here is some information');

// Loading message
const hide = message.loading('Processing...', 0);
setTimeout(() => {
  hide();
  message.success('Done!');
}, 2000);

// Configuration options
message.success({
  content: 'Success',
  duration: 3,
  onClose: () => console.log('Message closed'),
});
```

### notification Instance

```tsx
const { notification } = App.useApp();

// Basic notification
notification.open({
  title: 'New Message',
  description: 'You have received a new message from John Doe.',
  onClick: () => console.log('Notification clicked'),
});

// Success notification
notification.success({
  title: 'Payment Successful',
  description: 'Your payment of $99.00 has been processed successfully.',
  duration: 4.5,
});

// Error notification
notification.error({
  title: 'Upload Failed',
  description: 'Failed to upload file. Please try again.',
  duration: 0, // Don't auto close
});

// Warning notification
notification.warning({
  title: 'Low Storage',
  description: 'Your storage is running low.',
});

// Info notification
notification.info({
  title: 'Meeting Reminder',
  description: 'Your meeting starts in 15 minutes.',
});

// Notification with action button
notification.info({
  title: 'Meeting Reminder',
  description: 'Your meeting starts in 15 minutes.',
  btn: (
    <Button type="primary" size="small" onClick={() => notification.destroy()}>
      Join Now
    </Button>
  ),
  duration: 0,
});

// Notification with progress bar
notification.open({
  title: 'Upload Progress',
  description: 'Uploading your files...',
  showProgress: true,
  pauseOnHover: true,
});
```

### modal Instance

```tsx
const { modal } = App.useApp();

// Confirmation dialog
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

// Promise support
const confirmed = await modal.confirm({
  title: 'Confirm Action',
  content: 'Do you want to proceed?',
});

if (confirmed) {
  console.log('User confirmed');
} else {
  console.log('User cancelled');
}

// Info dialog
modal.info({
  title: 'Information',
  content: 'This is an informational message.',
});

// Success dialog
modal.success({
  title: 'Success',
  content: 'Operation completed successfully.',
});

// Error dialog
modal.error({
  title: 'Error',
  content: 'Something went wrong. Please try again.',
});

// Warning dialog
modal.warning({
  title: 'Warning',
  content: 'This action may have consequences.',
});
```

## Using with ConfigProvider

App component is usually used together with ConfigProvider to ensure static methods can access global configuration:

```tsx
import { App, ConfigProvider } from 'antd';
import zhCN from 'antd/locale/zh_CN';

const MyApp = () => (
  <ConfigProvider locale={zhCN}>
    <App>
      <MyPage />
    </App>
  </ConfigProvider>
);
```

## Nested Usage

App component supports nested usage, inner App will override outer configuration:

```tsx
const OuterApp = () => (
  <App>
    <InnerApp />
  </App>
);

const InnerApp = () => {
  const { message } = App.useApp();
  // message here will use inner App's configuration
  return <div>...</div>;
};
```

## App Properties

- **message** (ConfigProviderProps['message']) - Global message configuration
- **notification** (ConfigProviderProps['notification']) - Global notification configuration
- **component** (false | React.ComponentType) - Custom container component, set to false to not render container

### Global Configuration Example

```tsx
<App
  message={{
    maxCount: 3,
    duration: 2,
  }}
  notification={{
    placement: 'topRight',
    maxCount: 5,
  }}
>
  <MyPage />
</App>
```

## Best Practices

1. **Use at application root** - Place App component at the root of your application to ensure all child components can access context
2. **Use with ConfigProvider** - Place App inside ConfigProvider to access global configuration
3. **Use useApp Hook** - Use `App.useApp()` to get instances in functional components
4. **Avoid direct static method calls** - Prefer using instances returned by `App.useApp()` instead of calling static methods directly
5. **Handle Promises** - Use async/await to handle Promise return values from modal

## Migration Guide

If you previously used static methods, you can migrate like this:

### Before (Not Recommended)

```tsx
import { message, notification, Modal } from 'antd';

message.success('Success');
notification.info({ title: 'Info' });
Modal.confirm({ title: 'Confirm' });
```

### Now (Recommended)

```tsx
import { App } from 'antd';

const MyComponent = () => {
  const { message, notification, modal } = App.useApp();
  
  message.success('Success');
  notification.info({ title: 'Info' });
  modal.confirm({ title: 'Confirm' });
  
  return <div>...</div>;
};

const AppWrapper = () => (
  <App>
    <MyComponent />
  </App>
);
```

<!--
Source references:
- https://ant.design/components/app-cn
- https://github.com/ant-design/ant-design/blob/master/components/app/index.en-US.md
-->
