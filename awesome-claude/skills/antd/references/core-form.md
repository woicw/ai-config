---
name: antd-form
description: Ant Design Form component for collecting and validating user input. Use when building forms with validation rules, dynamic fields, and form state management.
---

# Form Component

Form is a core component in Ant Design for data collection and validation, providing comprehensive form management capabilities including field validation, dynamic forms, and form dependencies.

## Basic Usage

```tsx
import { Form, Input, Button } from 'antd';

const BasicForm = () => {
  const [form] = Form.useForm();

  const onFinish = (values: any) => {
    console.log('Success:', values);
  };

  const onFinishFailed = (errorInfo: any) => {
    console.log('Failed:', errorInfo);
  };

  return (
    <Form
      form={form}
      name="basic"
      layout="vertical"
      onFinish={onFinish}
      onFinishFailed={onFinishFailed}
      autoComplete="off"
    >
      <Form.Item
        label="Username"
        name="username"
        rules={[{ required: true, message: 'Please input your username!' }]}
      >
        <Input />
      </Form.Item>

      <Form.Item
        label="Password"
        name="password"
        rules={[{ required: true, message: 'Please input your password!' }]}
      >
        <Input.Password />
      </Form.Item>

      <Form.Item>
        <Button type="primary" htmlType="submit">
          Submit
        </Button>
      </Form.Item>
    </Form>
  );
};
```

## Form Instance Methods (FormInstance)

Get a form instance through `Form.useForm()` to programmatically manipulate the form:

### Get Field Values

```tsx
const [form] = Form.useForm();

// Get single field value
const username = form.getFieldValue('username');

// Get multiple field values
const values = form.getFieldsValue(['username', 'password']);

// Get all field values (including unmounted fields)
const allValues = form.getFieldsValue(true);
```

### Set Field Values

```tsx
// Set single field value
form.setFieldValue('username', 'new value');

// Set multiple field values
form.setFieldsValue({
  username: 'john',
  password: '123456',
});
```

### Validate Fields

```tsx
// Validate all fields
form.validateFields()
  .then((values) => {
    console.log('Validation passed:', values);
  })
  .catch((errorInfo) => {
    console.log('Validation failed:', errorInfo);
  });

// Validate specified fields
form.validateFields(['username', 'password']);

// Validate content only, don't show error messages
form.validateFields(['username'], { validateOnly: true });

// Recursive validation (including sub-paths)
form.validateFields(['address'], { recursive: true });

// Validate only modified fields
form.validateFields(['username'], { dirty: true });
```

### Reset Form

```tsx
// Reset all fields
form.resetFields();

// Reset specified fields
form.resetFields(['username', 'password']);
```

### Submit Form

```tsx
// Programmatically submit form (same as clicking submit button)
form.submit();
```

### Check Field Status

```tsx
// Check if field has been touched
const isTouched = form.isFieldTouched('username');

// Check if multiple fields have all been touched
const allTouched = form.isFieldsTouched(['username', 'password'], true);

// Get field error messages
const errors = form.getFieldError('username');
const allErrors = form.getFieldsError(['username', 'password']);

// Check if field is validating
const isValidating = form.isFieldValidating('username');
```

### Scroll to Field

```tsx
// Scroll to specified field position
form.scrollToField('username');

// Scroll and focus
form.scrollToField('username', { focus: true });
```

## Validation Rules

### Built-in Validation Rules

```tsx
<Form.Item
  name="email"
  rules={[
    { required: true, message: 'Email is required' },
    { type: 'email', message: 'Please enter a valid email' },
    { min: 5, message: 'Minimum 5 characters' },
    { max: 20, message: 'Maximum 20 characters' },
    { pattern: /^[A-Z]/, message: 'Must start with uppercase' },
  ]}
>
  <Input />
</Form.Item>
```

### Custom Validator

```tsx
<Form.Item
  name="password"
  rules={[
    { required: true, message: 'Please input your password!' },
    { min: 8, message: 'Password must be at least 8 characters' },
  ]}
>
  <Input.Password />
</Form.Item>

<Form.Item
  name="confirm"
  dependencies={['password']}
  rules={[
    { required: true, message: 'Please confirm your password!' },
    ({ getFieldValue }) => ({
      validator(_, value) {
        if (!value || getFieldValue('password') === value) {
          return Promise.resolve();
        }
        return Promise.reject(new Error('Passwords do not match!'));
      },
    }),
  ]}
>
  <Input.Password />
</Form.Item>
```

### Async Validation

```tsx
<Form.Item
  name="username"
  rules={[
    {
      validator: async (_, value) => {
        if (!value) {
          return Promise.reject('Username is required');
        }
        // Simulate API call
        const exists = await checkUsernameExists(value);
        if (exists) {
          return Promise.reject('Username already exists');
        }
        return Promise.resolve();
      },
    },
  ]}
>
  <Input />
</Form.Item>
```

## Form Layout

### Layout Types

```tsx
// Horizontal layout (default)
<Form layout="horizontal">
  <Form.Item label="Username" name="username">
    <Input />
  </Form.Item>
</Form>

// Vertical layout
<Form layout="vertical">
  <Form.Item label="Username" name="username">
    <Input />
  </Form.Item>
</Form>

// Inline layout
<Form layout="inline">
  <Form.Item name="username">
    <Input placeholder="Username" />
  </Form.Item>
  <Form.Item>
    <Button type="primary" htmlType="submit">Submit</Button>
  </Form.Item>
</Form>
```

### Label Alignment

```tsx
<Form labelAlign="left">  {/* left | right */}
  <Form.Item label="Username" name="username">
    <Input />
  </Form.Item>
</Form>
```

### Label Width

```tsx
<Form labelCol={{ span: 4 }} wrapperCol={{ span: 20 }}>
  <Form.Item label="Username" name="username">
    <Input />
  </Form.Item>
</Form>
```

## Dynamic Forms

### Dynamically Add/Remove Fields

```tsx
import { Form, Input, Button, Space } from 'antd';
import { MinusCircleOutlined, PlusOutlined } from '@ant-design/icons';

const DynamicForm = () => {
  return (
    <Form name="dynamic_form">
      <Form.List name="users">
        {(fields, { add, remove }) => (
          <>
            {fields.map(({ key, name, ...restField }) => (
              <Space key={key} style={{ display: 'flex', marginBottom: 8 }} align="baseline">
                <Form.Item
                  {...restField}
                  name={[name, 'first']}
                  rules={[{ required: true, message: 'Missing first name' }]}
                >
                  <Input placeholder="First Name" />
                </Form.Item>
                <Form.Item
                  {...restField}
                  name={[name, 'last']}
                  rules={[{ required: true, message: 'Missing last name' }]}
                >
                  <Input placeholder="Last Name" />
                </Form.Item>
                <MinusCircleOutlined onClick={() => remove(name)} />
              </Space>
            ))}
            <Form.Item>
              <Button type="dashed" onClick={() => add()} block icon={<PlusOutlined />}>
                Add field
              </Button>
            </Form.Item>
          </>
        )}
      </Form.List>
    </Form>
  );
};
```

### Conditional Field Rendering

```tsx
const ConditionalForm = () => {
  const [form] = Form.useForm();
  const type = Form.useWatch('type', form);

  return (
    <Form form={form}>
      <Form.Item name="type" label="Type">
        <Select>
          <Select.Option value="personal">Personal</Select.Option>
          <Select.Option value="company">Company</Select.Option>
        </Select>
      </Form.Item>

      {type === 'company' && (
        <Form.Item name="companyName" label="Company Name">
          <Input />
        </Form.Item>
      )}
    </Form>
  );
};
```

## Form.Item Properties

### Basic Properties

- **name** (NamePath) - Field name, supports nested paths like `['user', 'name']`
- **label** (ReactNode) - Label text
- **rules** (Rule[]) - Validation rules array
- **required** (boolean) - Whether field is required (displays red asterisk next to label)
- **tooltip** (ReactNode) - Tooltip information next to label
- **extra** (ReactNode) - Additional help text displayed below form control
- **help** (ReactNode) - Help text displayed below form control
- **validateStatus** ('success' | 'warning' | 'error' | 'validating') - Validation status
- **hasFeedback** (boolean) - Whether to show validation feedback icon

### Value Properties

- **valuePropName** (string) - Property name for child node value, e.g., `checked` for Checkbox
- **getValueFromEvent** ((...args: any[]) => any) - How to get value from event
- **getValueProps** ((value: any) => any) - Customize how to get value from form store
- **normalize** ((value: any, prevValue: any, prevValues: any) => any) - Normalize value
- **preserve** (boolean) - Whether to preserve field value when field is removed

### Dependencies

- **dependencies** (NamePath[]) - Dependent fields, re-validate when dependencies change
- **shouldUpdate** (boolean | (prevValues, currentValues) => boolean) - Whether to re-render when field values change

### Examples

```tsx
<Form.Item
  name="agreement"
  valuePropName="checked"
  rules={[{ validator: (_, value) => value ? Promise.resolve() : Promise.reject('Please accept') }]}
>
  <Checkbox>I agree to the terms</Checkbox>
</Form.Item>

<Form.Item
  name="upload"
  valuePropName="fileList"
  getValueFromEvent={(e) => {
    if (Array.isArray(e)) {
      return e;
    }
    return e?.fileList;
  }}
>
  <Upload>
    <Button>Upload</Button>
  </Upload>
</Form.Item>
```

## Form Properties

### Basic Properties

- **form** (FormInstance) - Form instance, created via `Form.useForm()`
- **name** (string) - Form name, used to distinguish multiple forms
- **layout** ('horizontal' | 'vertical' | 'inline') - Form layout
- **labelAlign** ('left' | 'right') - Label alignment
- **labelCol** (ColProps) - Label column configuration
- **wrapperCol** (ColProps) - Input control column configuration
- **colon** (boolean) - Whether to show colon after label
- **requiredMark** (boolean | ReactNode) - Required mark style

### Initial Values

- **initialValues** (object) - Form initial values
- **preserve** (boolean) - Whether to preserve field values when fields are removed

### Event Callbacks

- **onFinish** ((values: any) => void) - Triggered when form is submitted and validation passes
- **onFinishFailed** ((errorInfo: ValidateErrorEntity) => void) - Triggered when form submission fails validation
- **onValuesChange** ((changedValues: any, allValues: any) => void) - Triggered when field values change

### Others

- **scrollToFirstError** (boolean | Options) - Whether to scroll to first error field after submission fails
- **validateTrigger** ('onChange' | 'onBlur' | 'onSubmit') - Validation trigger timing
- **autoComplete** (string) - Autocomplete attribute

## Best Practices

1. **Use Form.useForm()** - Use hook to create form instance in functional components
2. **Use validation rules appropriately** - Combine built-in rules with custom validators
3. **Handle async validation** - Use Promise to handle async validation logic
4. **Field dependencies** - Use `dependencies` to handle field dependencies
5. **Dynamic forms** - Use `Form.List` to handle dynamic field lists
6. **Performance optimization** - Use `shouldUpdate` to control unnecessary re-renders

<!--
Source references:
- https://ant.design/components/form-cn
- https://github.com/ant-design/ant-design/blob/master/components/form/index.en-US.md
-->
