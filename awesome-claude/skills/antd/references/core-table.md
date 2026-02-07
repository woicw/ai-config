---
name: antd-table
description: Ant Design Table component for displaying structured data with sorting, filtering, pagination, and selection. Use when building data tables, data grids, or any tabular data display.
---

# Table Component

Table is a core component in Ant Design for displaying structured data, providing rich features including sorting, filtering, pagination, and selection.

## Basic Usage

```tsx
import { Table } from 'antd';
import type { TableColumnsType } from 'antd';

interface DataType {
  key: string;
  name: string;
  age: number;
  address: string;
}

const columns: TableColumnsType<DataType> = [
  {
    title: 'Name',
    dataIndex: 'name',
    key: 'name',
  },
  {
    title: 'Age',
    dataIndex: 'age',
    key: 'age',
  },
  {
    title: 'Address',
    dataIndex: 'address',
    key: 'address',
  },
];

const dataSource: DataType[] = [
  {
    key: '1',
    name: 'John Brown',
    age: 32,
    address: 'New York No. 1 Lake Park',
  },
  {
    key: '2',
    name: 'Jim Green',
    age: 42,
    address: 'London No. 1 Lake Park',
  },
];

const BasicTable = () => {
  return <Table dataSource={dataSource} columns={columns} />;
};
```

## Column Configuration (Columns)

### Basic Column Properties

```tsx
const columns: TableColumnsType<DataType> = [
  {
    title: 'Name',           // Column title
    dataIndex: 'name',        // Data field name, supports nested paths like ['user', 'name']
    key: 'name',              // React key, can be omitted if dataIndex is unique
    width: 150,               // Column width
    align: 'left',            // Alignment: 'left' | 'right' | 'center'
    fixed: 'left',            // Fixed column: 'left' | 'right' | true
    ellipsis: true,           // Auto ellipsis when exceeding width
    className: 'custom-class', // Custom class name
  },
];
```

### Custom Rendering

```tsx
const columns: TableColumnsType<DataType> = [
  {
    title: 'Name',
    dataIndex: 'name',
    key: 'name',
    render: (text: string, record: DataType, index: number) => {
      return <a>{text}</a>;
    },
  },
  {
    title: 'Tags',
    dataIndex: 'tags',
    key: 'tags',
    render: (tags: string[]) => (
      <>
        {tags.map(tag => (
          <Tag color="blue" key={tag}>{tag}</Tag>
        ))}
      </>
    ),
  },
  {
    title: 'Action',
    key: 'action',
    render: (_, record) => (
      <Space size="middle">
        <a>Edit</a>
        <a>Delete</a>
      </Space>
    ),
  },
];
```

## Sorting

### Local Sorting

```tsx
const columns: TableColumnsType<DataType> = [
  {
    title: 'Age',
    dataIndex: 'age',
    key: 'age',
    sorter: (a, b) => a.age - b.age,
    sortDirections: ['ascend', 'descend'], // Sort directions
    defaultSortOrder: 'ascend',             // Default sort order
  },
  {
    title: 'Name',
    dataIndex: 'name',
    key: 'name',
    sorter: (a, b, sortOrder) => {
      // sortOrder: 'ascend' | 'descend' | null
      if (sortOrder === 'ascend') {
        return a.name.localeCompare(b.name);
      } else {
        return b.name.localeCompare(a.name);
      }
    },
  },
];
```

### Server-side Sorting

```tsx
const [sortedInfo, setSortedInfo] = useState<{
  order: 'ascend' | 'descend' | null;
  columnKey: string;
} | null>(null);

const handleChange = (pagination: any, filters: any, sorter: any) => {
  setSortedInfo(sorter);
  // Call API to get sorted data
  fetchData({ sortField: sorter.field, sortOrder: sorter.order });
};

const columns: TableColumnsType<DataType> = [
  {
    title: 'Age',
    dataIndex: 'age',
    key: 'age',
    sorter: true, // Enable server-side sorting
    sortOrder: sortedInfo?.columnKey === 'age' ? sortedInfo.order : null,
  },
];

<Table
  columns={columns}
  dataSource={dataSource}
  onChange={handleChange}
/>
```

### Multi-column Sorting

```tsx
const columns: TableColumnsType<DataType> = [
  {
    title: 'Name',
    dataIndex: 'name',
    key: 'name',
    sorter: {
      compare: (a, b) => a.name.localeCompare(b.name),
      multiple: 1, // Sort priority
    },
  },
  {
    title: 'Age',
    dataIndex: 'age',
    key: 'age',
    sorter: {
      compare: (a, b) => a.age - b.age,
      multiple: 2,
    },
  },
];

<Table
  columns={columns}
  dataSource={dataSource}
  sortDirections={['ascend', 'descend', 'ascend']} // Prevent returning to unsorted state
/>
```

## Filtering

### Basic Filtering

```tsx
const columns: TableColumnsType<DataType> = [
  {
    title: 'Status',
    dataIndex: 'status',
    key: 'status',
    filters: [
      { text: 'Active', value: 'active' },
      { text: 'Inactive', value: 'inactive' },
      { text: 'Pending', value: 'pending' },
    ],
    onFilter: (value: string, record: DataType) => record.status === value,
    filterMultiple: true, // Whether to support multiple selection
  },
];
```

### Custom Filter Menu

```tsx
import { Input, Button, Space } from 'antd';

const columns: TableColumnsType<DataType> = [
  {
    title: 'Name',
    dataIndex: 'name',
    key: 'name',
    filterDropdown: ({
      setSelectedKeys,
      selectedKeys,
      confirm,
      clearFilters,
    }) => (
      <div style={{ padding: 8 }}>
        <Input
          placeholder="Search name"
          value={selectedKeys[0]}
          onChange={(e) => setSelectedKeys(e.target.value ? [e.target.value] : [])}
          onPressEnter={() => confirm()}
          style={{ marginBottom: 8, display: 'block' }}
        />
        <Space>
          <Button type="primary" onClick={() => confirm()} size="small">
            Search
          </Button>
          <Button onClick={() => clearFilters?.()} size="small">
            Reset
          </Button>
        </Space>
      </div>
    ),
    onFilter: (value: string, record: DataType) =>
      record.name.toLowerCase().includes(value.toLowerCase()),
  },
];
```

### Controlled Filtering

```tsx
const [filteredInfo, setFilteredInfo] = useState<Record<string, FilterValue | null>>({});

const handleChange = (pagination: any, filters: any, sorter: any) => {
  setFilteredInfo(filters);
};

const columns: TableColumnsType<DataType> = [
  {
    title: 'Status',
    dataIndex: 'status',
    key: 'status',
    filters: [
      { text: 'Active', value: 'active' },
      { text: 'Inactive', value: 'inactive' },
    ],
    filteredValue: filteredInfo.status || null,
    onFilter: (value: string, record: DataType) => record.status === value,
  },
];
```

## Pagination

### Basic Pagination

```tsx
<Table
  dataSource={dataSource}
  columns={columns}
  pagination={{
    current: 1,
    pageSize: 10,
    total: 100,
    showSizeChanger: true,
    showQuickJumper: true,
    showTotal: (total) => `Total ${total} items`,
  }}
/>
```

### Server-side Pagination

```tsx
const [pagination, setPagination] = useState({
  current: 1,
  pageSize: 10,
  total: 0,
});

const handleTableChange = (newPagination: any) => {
  setPagination({
    current: newPagination.current,
    pageSize: newPagination.pageSize,
    total: newPagination.total,
  });
  // Call API to get new page data
  fetchData({
    page: newPagination.current,
    pageSize: newPagination.pageSize,
  });
};

<Table
  dataSource={dataSource}
  columns={columns}
  pagination={pagination}
  onChange={handleTableChange}
/>
```

### Hide Pagination

```tsx
<Table
  dataSource={dataSource}
  columns={columns}
  pagination={false}
/>
```

## Row Selection

### Basic Selection

```tsx
import { useState } from 'react';
import type { TableRowSelection } from 'antd/es/table/interface';

const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([]);

const rowSelection: TableRowSelection<DataType> = {
  selectedRowKeys,
  onChange: (keys: React.Key[], rows: DataType[]) => {
    setSelectedRowKeys(keys);
    console.log('Selected rows:', rows);
  },
};

<Table
  rowSelection={rowSelection}
  dataSource={dataSource}
  columns={columns}
/>
```

### Selection Configuration

```tsx
const rowSelection: TableRowSelection<DataType> = {
  type: 'checkbox', // 'checkbox' | 'radio'
  selectedRowKeys,
  onChange: (keys, rows) => {
    setSelectedRowKeys(keys);
  },
  onSelect: (record, selected, selectedRows) => {
    console.log('Select:', record, selected, selectedRows);
  },
  onSelectAll: (selected, selectedRows, changeRows) => {
    console.log('Select All:', selected, selectedRows, changeRows);
  },
  getCheckboxProps: (record: DataType) => ({
    disabled: record.status === 'disabled', // Disable selection for certain rows
    name: record.name,
  }),
};
```

## Expandable Rows

### Basic Expand

```tsx
const columns: TableColumnsType<DataType> = [
  {
    title: 'Name',
    dataIndex: 'name',
    key: 'name',
  },
];

<Table
  columns={columns}
  dataSource={dataSource}
  expandable={{
    expandedRowRender: (record) => <p>{record.description}</p>,
    rowExpandable: (record) => record.name !== 'Not Expandable',
  }}
/>
```

### Controlled Expand

```tsx
const [expandedRowKeys, setExpandedRowKeys] = useState<React.Key[]>([]);

<Table
  columns={columns}
  dataSource={dataSource}
  expandable={{
    expandedRowKeys,
    onExpandedRowsChange: setExpandedRowKeys,
    expandedRowRender: (record) => <p>{record.description}</p>,
  }}
/>
```

## Table Properties

### Data Related

- **dataSource** (T[]) - Data source array
- **columns** (ColumnsType<T>[]) - Column configuration array
- **rowKey** (string | (record: T) => string) - Row key, defaults to 'key'
- **loading** (boolean | SpinProps) - Loading state

### Style Related

- **size** ('large' | 'middle' | 'small') - Table size
- **bordered** (boolean) - Whether to show border
- **scroll** ({ x?: number | string, y?: number | string }) - Horizontal or vertical scrolling
- **sticky** (boolean | Sticky) - Whether header is fixed

### Function Related

- **pagination** (false | PaginationProps) - Pagination configuration
- **rowSelection** (RowSelection<T>) - Row selection configuration
- **expandable** (ExpandableConfig<T>) - Expandable row configuration
- **onChange** ((pagination, filters, sorter, extra) => void) - Triggered when pagination, filtering, or sorting changes

### Event Callbacks

- **onRow** ((record, index) => object) - Set row properties
- **onHeaderRow** ((columns, index) => object) - Set header row properties

### Example: Row Click Event

```tsx
<Table
  dataSource={dataSource}
  columns={columns}
  onRow={(record) => ({
    onClick: () => {
      console.log('Row clicked:', record);
    },
    onDoubleClick: () => {
      console.log('Row double clicked:', record);
    },
  })}
/>
```

## Virtual Scrolling

For large datasets, use virtual scrolling to optimize performance:

```tsx
<Table
  dataSource={largeDataSource}
  columns={columns}
  scroll={{ y: 400 }}
  pagination={false}
/>
```

## Responsive Columns

```tsx
const columns: TableColumnsType<DataType> = [
  {
    title: 'Name',
    dataIndex: 'name',
    key: 'name',
  },
  {
    title: 'Email',
    dataIndex: 'email',
    key: 'email',
    responsive: ['md'], // Display on medium screens and above
  },
  {
    title: 'Phone',
    dataIndex: 'phone',
    key: 'phone',
    responsive: ['lg'], // Display on large screens and above
  },
];
```

## Best Practices

1. **Use TypeScript** - Define types for DataType and columns
2. **Use rowKey appropriately** - Ensure each row has a unique key
3. **Server-side data processing** - Use server-side pagination, sorting, and filtering for large datasets
4. **Performance optimization** - Use virtual scrolling for large datasets
5. **Responsive design** - Use responsive property to adapt to different screens
6. **Accessibility** - Ensure tables have appropriate titles and descriptions

<!--
Source references:
- https://ant.design/components/table-cn
- https://github.com/ant-design/ant-design/blob/master/components/table/index.en-US.md
-->
