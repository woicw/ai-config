---
name: ahooks-use-antd-table
description: useAntdTable hook for integrating with Ant Design Table component. Use when building tables with pagination, sorting, filtering, and data fetching.
---

# useAntdTable

`useAntdTable` is a hook specifically designed for Ant Design Table component, providing out-of-the-box pagination, sorting, filtering, and deep integration with `useRequest`.

## Basic Usage

```tsx
import { useAntdTable } from 'ahooks';
import { Table } from 'antd';

function UserTable() {
  const { tableProps } = useAntdTable(getUserList);

  return (
    <Table {...tableProps} rowKey="id">
      <Table.Column dataIndex="name" title="Name" />
      <Table.Column dataIndex="email" title="Email" />
    </Table>
  );
}
```

## Return Values

```tsx
const {
  tableProps,      // Props to pass to Table component
  search,          // Form search object
  loading,         // Loading state
  data,            // Table data
  pagination,      // Pagination object
  refresh,         // Refresh data
  reset,           // Reset search and pagination
} = useAntdTable(service, options);
```

## Service Function

The service function receives an object parameter containing pagination and search parameters:

```tsx
interface Params {
  current: number;      // Current page number
  pageSize: number;     // Items per page
  [key: string]: any;  // Other search parameters
}

async function getUserList(params: Params) {
  const { current, pageSize, ...filters } = params;
  const response = await fetch(`/api/users?page=${current}&size=${pageSize}`, {
    method: 'POST',
    body: JSON.stringify(filters),
  });
  const result = await response.json();
  return {
    list: result.data,
    total: result.total,
  };
}
```

## Return Format

The service function must return an object containing `list` and `total`:

```tsx
async function getUserList(params: Params) {
  // ...
  return {
    list: [...],  // Current page data list
    total: 100,   // Total record count
  };
}
```

## Search Functionality

### Basic Search

Use `search` object to manage search parameters:

```tsx
function UserTable() {
  const { tableProps, search } = useAntdTable(getUserList);

  return (
    <div>
      <Input
        value={search.type}
        onChange={(e) => search.submit({ type: e.target.value })}
        placeholder="Search"
      />
      <Table {...tableProps} rowKey="id">
        {/* columns */}
      </Table>
    </div>
  );
}
```

### Form Search

Use with Ant Design Form:

```tsx
function UserTable() {
  const [form] = Form.useForm();
  const { tableProps, search } = useAntdTable(
    async ({ current, pageSize, ...filters }) => {
      return getUserList({ current, pageSize, ...filters });
    },
    {
      form,
    }
  );

  return (
    <div>
      <Form form={form}>
        <Form.Item name="name">
          <Input placeholder="Name" />
        </Form.Item>
        <Form.Item name="email">
          <Input placeholder="Email" />
        </Form.Item>
        <Button onClick={search.submit}>Search</Button>
        <Button onClick={search.reset}>Reset</Button>
      </Form>
      <Table {...tableProps} rowKey="id">
        {/* columns */}
      </Table>
    </div>
  );
}
```

### search Object Methods

```tsx
const { search } = useAntdTable(getUserList);

search.submit({ name: 'John' });  // Submit search, reset to first page
search.reset();                    // Reset search conditions
search.change({ name: 'John' });   // Change search conditions without submitting
```

## Sorting

Add `sorter: true` to Table.Column to enable sorting:

```tsx
function UserTable() {
  const { tableProps } = useAntdTable(getUserList);

  return (
    <Table {...tableProps} rowKey="id">
      <Table.Column
        dataIndex="name"
        title="Name"
        sorter={true}  // Enable sorting
      />
      <Table.Column
        dataIndex="createdAt"
        title="Created At"
        sorter={true}
      />
    </Table>
  );
}
```

The service function receives sorting parameters:

```tsx
async function getUserList(params: Params) {
  const { current, pageSize, sorter } = params;
  // sorter: { field: 'name', order: 'ascend' | 'descend' }
  
  const orderBy = sorter?.field;
  const order = sorter?.order === 'ascend' ? 'ASC' : 'DESC';
  
  return getUserList({ current, pageSize, orderBy, order });
}
```

## Filtering

Use `filters` and `onFilter` on Table.Column:

```tsx
function UserTable() {
  const { tableProps } = useAntdTable(getUserList);

  return (
    <Table {...tableProps} rowKey="id">
      <Table.Column
        dataIndex="status"
        title="Status"
        filters={[
          { text: 'Active', value: 'active' },
          { text: 'Inactive', value: 'inactive' },
        ]}
        onFilter={(value, record) => record.status === value}
      />
    </Table>
  );
}
```

## Pagination Configuration

### Default Pagination

```tsx
const { tableProps } = useAntdTable(getUserList, {
  defaultPageSize: 20,
  defaultCurrent: 1,
});
```

### Disable Pagination

```tsx
const { tableProps } = useAntdTable(getUserList, {
  hasPagination: false,
});
```

### Custom Pagination

```tsx
const { tableProps } = useAntdTable(getUserList);

<Table
  {...tableProps}
  pagination={{
    ...tableProps.pagination,
    showSizeChanger: true,
    showQuickJumper: true,
    showTotal: (total) => `Total ${total} items`,
  }}
/>
```

## URL Synchronization

Use `syncWithLocation` to sync search, pagination, and sorting state to URL:

```tsx
import { useAntdTable } from 'ahooks';
import { useLocation, useNavigate } from 'react-router-dom';

function UserTable() {
  const location = useLocation();
  const navigate = useNavigate();
  
  const { tableProps } = useAntdTable(getUserList, {
    syncWithLocation: {
      location,
      navigate,
    },
  });

  // Pagination, search, sorting state automatically syncs to URL
  // URL: /users?current=1&pageSize=20&name=John
}
```

## Caching

Use `cacheKey` to cache table data:

```tsx
const { tableProps } = useAntdTable(getUserList, {
  cacheKey: 'user-table',
});
```

## Refresh and Reset

```tsx
function UserTable() {
  const { tableProps, refresh, reset } = useAntdTable(getUserList);

  return (
    <div>
      <Button onClick={refresh}>Refresh</Button>
      <Button onClick={reset}>Reset</Button>
      <Table {...tableProps} rowKey="id">
        {/* columns */}
      </Table>
    </div>
  );
}
```

## Complete Example

```tsx
import { useAntdTable } from 'ahooks';
import { Table, Form, Input, Button, Select } from 'antd';

interface User {
  id: string;
  name: string;
  email: string;
  status: 'active' | 'inactive';
}

async function getUserList(params: {
  current: number;
  pageSize: number;
  name?: string;
  status?: string;
  sorter?: { field: string; order: 'ascend' | 'descend' };
}) {
  const { current, pageSize, name, status, sorter } = params;
  
  const queryParams = new URLSearchParams({
    page: current.toString(),
    size: pageSize.toString(),
  });
  
  if (name) queryParams.append('name', name);
  if (status) queryParams.append('status', status);
  if (sorter) {
    queryParams.append('orderBy', sorter.field);
    queryParams.append('order', sorter.order === 'ascend' ? 'ASC' : 'DESC');
  }
  
  const response = await fetch(`/api/users?${queryParams}`);
  const result = await response.json();
  
  return {
    list: result.data,
    total: result.total,
  };
}

function UserTable() {
  const [form] = Form.useForm();
  
  const { tableProps, search, refresh } = useAntdTable<User>(
    getUserList,
    {
      form,
      defaultPageSize: 20,
    }
  );

  return (
    <div>
      <Form form={form} layout="inline" style={{ marginBottom: 16 }}>
        <Form.Item name="name">
          <Input placeholder="Name" allowClear />
        </Form.Item>
        <Form.Item name="status">
          <Select placeholder="Status" allowClear style={{ width: 120 }}>
            <Select.Option value="active">Active</Select.Option>
            <Select.Option value="inactive">Inactive</Select.Option>
          </Select>
        </Form.Item>
        <Form.Item>
          <Button type="primary" onClick={search.submit}>
            Search
          </Button>
        </Form.Item>
        <Form.Item>
          <Button onClick={search.reset}>Reset</Button>
        </Form.Item>
        <Form.Item>
          <Button onClick={refresh}>Refresh</Button>
        </Form.Item>
      </Form>
      
      <Table {...tableProps} rowKey="id">
        <Table.Column
          dataIndex="name"
          title="Name"
          sorter={true}
        />
        <Table.Column
          dataIndex="email"
          title="Email"
        />
        <Table.Column
          dataIndex="status"
          title="Status"
          filters={[
            { text: 'Active', value: 'active' },
            { text: 'Inactive', value: 'inactive' },
          ]}
          onFilter={(value, record) => record.status === value}
        />
      </Table>
    </div>
  );
}
```

## TypeScript

```tsx
import { useAntdTable } from 'ahooks';

interface User {
  id: string;
  name: string;
  email: string;
}

interface Params {
  current: number;
  pageSize: number;
  name?: string;
}

const { tableProps } = useAntdTable<User, Params>(
  async (params: Params) => {
    return getUserList(params);
  }
);
```

## Key Points

- **Out-of-the-box** - Returns `tableProps` directly, no need to manually manage pagination state
- **Form integration** - Seamless integration with Ant Design Form
- **Sorting and filtering** - Automatically handles sorting and filtering parameters
- **URL synchronization** - Supports syncing state to URL
- **Caching support** - Use `cacheKey` to cache table data
- **Type safety** - Full TypeScript support
- **Service function format** - Must return `{ list, total }` format

<!--
Source references:
- https://ahooks.js.org/zh-CN/hooks/use-antd-table/index
- https://ahooks.js.org/hooks/use-antd-table/index
-->
