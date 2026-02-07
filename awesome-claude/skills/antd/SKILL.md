---
name: antd
description: Ant Design React UI component library. Use when building enterprise-level web applications with comprehensive UI components including forms, tables, modals, and more.
metadata:
  author: woic
  version: "2026.2.6"
  source: Generated from https://ant.design
---

# Ant Design

Ant Design is an enterprise-level UI design language and React UI library that provides comprehensive components for building high-quality enterprise web applications.

> The skill is based on antd v6.2.2+, generated at 2026-02-06.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Form | Form component for data collection and validation | [core-form](references/core-form.md) |
| Table | Table component for displaying structured data | [core-table](references/core-table.md) |
| Modal | Modal component for displaying dialogs and confirmations | [core-modal](references/core-modal.md) |
| Upload | Upload component for file upload functionality | [core-upload](references/core-upload.md) |
| App | Wrapper component providing context support for static methods | [core-app](references/core-app.md) |
| ConfigProvider | Global configuration component for themes, locales, and more | [core-config-provider](references/core-config-provider.md) |

## General Components

| Component | Description | Usage |
|-----------|-------------|-------|
| Button | Button component | `<Button type="primary">Click</Button>` - Props: `type`, `size`, `loading`, `disabled`, `icon`, `onClick` |
| FloatButton | Floating action button | `<FloatButton icon={<PlusOutlined />} />` - Props: `type`, `shape`, `icon`, `tooltip`, `onClick` |
| Icon | Icon component | `<Icon component={CustomIcon} />` - Props: `component`, `spin`, `rotate`, `style` |
| Typography | Typography component | `<Typography.Title>Title</Typography.Title>` - Props: `level`, `ellipsis`, `copyable`, `editable` |

## Layout Components

| Component | Description | Usage |
|-----------|-------------|-------|
| Divider | Divider line | `<Divider />` - Props: `type`, `orientation`, `plain`, `dashed` |
| Flex | Flexbox layout | `<Flex gap="middle">...</Flex>` - Props: `gap`, `vertical`, `wrap`, `justify`, `align` |
| Grid | Grid system | `<Row><Col span={12}>...</Col></Row>` - Props: `span`, `offset`, `gutter`, `flex` |
| Layout | Layout container | `<Layout><Header /><Content /><Footer /></Layout>` - Props: `hasSider`, `className` |
| Masonry | Masonry layout | `<Masonry columns={3}>...</Masonry>` - Props: `columns`, `gap`, `items` |
| Space | Spacing component | `<Space size="large">...</Space>` - Props: `size`, `direction`, `wrap`, `align` |
| Splitter | Split panel | `<Splitter>...</Splitter>` - Props: `defaultSize`, `min`, `max`, `resize` |

## Navigation Components

| Component | Description | Usage |
|-----------|-------------|-------|
| Anchor | Anchor navigation | `<Anchor><Anchor.Link href="#section1" title="Section 1" /></Anchor>` - Props: `affix`, `offsetTop`, `items` |
| Breadcrumb | Breadcrumb navigation | `<Breadcrumb items={[{title: 'Home'}, {title: 'Page'}]} />` - Props: `items`, `separator`, `itemRender` |
| Dropdown | Dropdown menu | `<Dropdown menu={{items}}><Button>Menu</Button></Dropdown>` - Props: `menu`, `trigger`, `placement`, `overlay` |
| Menu | Navigation menu | `<Menu items={items} />` - Props: `mode`, `theme`, `selectedKeys`, `onSelect`, `items` |
| Pagination | Pagination component | `<Pagination current={1} total={100} />` - Props: `current`, `pageSize`, `total`, `showSizeChanger`, `onChange` |
| Steps | Steps component | `<Steps current={1} items={items} />` - Props: `current`, `items`, `status`, `direction` |
| Tabs | Tabs component | `<Tabs items={items} />` - Props: `activeKey`, `items`, `type`, `onChange` |

## Data Entry Components

| Component | Description | Usage |
|-----------|-------------|-------|
| AutoComplete | Auto complete | `<AutoComplete options={options} />` - Props: `options`, `value`, `onChange`, `onSearch`, `filterOption` |
| Cascader | Cascader select | `<Cascader options={options} />` - Props: `options`, `value`, `onChange`, `multiple`, `showSearch` |
| Checkbox | Checkbox | `<Checkbox>Option</Checkbox>` - Props: `checked`, `onChange`, `disabled`, `indeterminate` |
| ColorPicker | Color picker | `<ColorPicker />` - Props: `value`, `onChange`, `format`, `showText` |
| DatePicker | Date picker | `<DatePicker />` - Props: `value`, `onChange`, `format`, `picker`, `showTime`, `disabledDate` |
| Input | Input field | `<Input placeholder="Enter text" />` - Props: `value`, `onChange`, `placeholder`, `allowClear`, `prefix`, `suffix` |
| InputNumber | Number input | `<InputNumber min={0} max={100} />` - Props: `value`, `onChange`, `min`, `max`, `step`, `precision` |
| Mentions | Mentions component | `<Mentions options={options} />` - Props: `value`, `onChange`, `options`, `onSelect` |
| Radio | Radio button | `<Radio.Group><Radio value="1">Option 1</Radio></Radio.Group>` - Props: `value`, `onChange`, `options` |
| Rate | Rate component | `<Rate value={3} />` - Props: `value`, `onChange`, `count`, `allowHalf`, `disabled` |
| Select | Select component | `<Select options={options} />` - Props: `value`, `onChange`, `options`, `mode`, `showSearch`, `filterOption` |
| Slider | Slider input | `<Slider min={0} max={100} />` - Props: `value`, `onChange`, `min`, `max`, `step`, `range` |
| Switch | Switch component | `<Switch checked={true} />` - Props: `checked`, `onChange`, `disabled`, `size` |
| TimePicker | Time picker | `<TimePicker />` - Props: `value`, `onChange`, `format`, `minuteStep` |
| Transfer | Transfer component | `<Transfer dataSource={data} />` - Props: `dataSource`, `targetKeys`, `onChange`, `render` |
| TreeSelect | Tree select | `<TreeSelect treeData={treeData} />` - Props: `treeData`, `value`, `onChange`, `multiple`, `showSearch` |

## Data Display Components

| Component | Description | Usage |
|-----------|-------------|-------|
| Avatar | Avatar component | `<Avatar src="url" />` - Props: `src`, `icon`, `size`, `shape`, `alt` |
| Badge | Badge component | `<Badge count={5}><Avatar /></Badge>` - Props: `count`, `showZero`, `overflowCount`, `dot` |
| Calendar | Calendar component | `<Calendar />` - Props: `value`, `onChange`, `onSelect`, `fullscreen`, `mode` |
| Card | Card component | `<Card title="Title">Content</Card>` - Props: `title`, `extra`, `bordered`, `hoverable`, `loading` |
| Carousel | Carousel component | `<Carousel><div>Slide 1</div></Carousel>` - Props: `autoplay`, `dots`, `effect`, `afterChange` |
| Collapse | Collapse panel | `<Collapse items={items} />` - Props: `items`, `activeKey`, `onChange`, `accordion` |
| Descriptions | Descriptions list | `<Descriptions items={items} />` - Props: `items`, `column`, `bordered`, `layout` |
| Empty | Empty state | `<Empty description="No data" />` - Props: `description`, `image`, `imageStyle` |
| Image | Image component | `<Image src="url" />` - Props: `src`, `alt`, `width`, `height`, `preview`, `fallback` |
| List | List component | `<List dataSource={data} renderItem={item => <List.Item>{item}</List.Item>} />` - Props: `dataSource`, `renderItem`, `pagination`, `loading` |
| Popover | Popover component | `<Popover content="Content"><Button>Hover</Button></Popover>` - Props: `content`, `title`, `trigger`, `placement` |
| QRCode | QR Code component | `<QRCode value="text" />` - Props: `value`, `size`, `errorLevel`, `icon`, `status` |
| Segmented | Segmented control | `<Segmented options={['Option 1', 'Option 2']} />` - Props: `options`, `value`, `onChange`, `block` |
| Statistic | Statistic component | `<Statistic title="Total" value={1128} />` - Props: `title`, `value`, `prefix`, `suffix`, `precision` |
| Tag | Tag component | `<Tag color="blue">Tag</Tag>` - Props: `color`, `closable`, `onClose`, `icon` |
| Timeline | Timeline component | `<Timeline items={items} />` - Props: `items`, `mode`, `pending`, `reverse` |
| Tooltip | Tooltip component | `<Tooltip title="Tooltip"><Button>Hover</Button></Tooltip>` - Props: `title`, `placement`, `trigger`, `color` |
| Tour | Tour component | `<Tour open={true} steps={steps} />` - Props: `open`, `steps`, `onClose`, `current` |
| Tree | Tree component | `<Tree treeData={treeData} />` - Props: `treeData`, `defaultExpandAll`, `onSelect`, `checkable`, `checkedKeys` |

## Feedback Components

| Component | Description | Usage |
|-----------|-------------|-------|
| Alert | Alert component | `<Alert message="Success" type="success" />` - Props: `message`, `type`, `showIcon`, `closable`, `onClose` |
| Drawer | Drawer component | `<Drawer open={true} onClose={() => {}}>Content</Drawer>` - Props: `open`, `onClose`, `placement`, `width`, `title` |
| Message | Global message | `message.success('Success')` - Props: `content`, `duration`, `onClose`, `icon` |
| Notification | Notification component | `notification.open({title: 'Title', description: 'Description'})` - Props: `title`, `description`, `duration`, `placement` |
| Popconfirm | Popconfirm component | `<Popconfirm title="Confirm?" onConfirm={() => {}}><Button>Delete</Button></Popconfirm>` - Props: `title`, `onConfirm`, `okText`, `cancelText` |
| Progress | Progress bar | `<Progress percent={50} />` - Props: `percent`, `status`, `strokeColor`, `format`, `type` |
| Result | Result page | `<Result status="success" title="Success" />` - Props: `status`, `title`, `subTitle`, `extra` |
| Skeleton | Skeleton screen | `<Skeleton />` - Props: `active`, `avatar`, `paragraph`, `loading`, `title` |
| Spin | Loading spinner | `<Spin><YourComponent /></Spin>` - Props: `spinning`, `tip`, `size`, `delay` |
| Watermark | Watermark component | `<Watermark content="Watermark"><div>Content</div></Watermark>` - Props: `content`, `gap`, `offset`, `font` |

## Other Components

| Component | Description | Usage |
|-----------|-------------|-------|
| Affix | Affix component | `<Affix offsetTop={10}><Button>Fixed</Button></Affix>` - Props: `offsetTop`, `offsetBottom`, `target`, `onChange` |

## Key Recommendations

- **Use Form for form management** - Handle all form validation and data collection scenarios
- **Use Table for data display** - Handle table data display, sorting, filtering, and pagination
- **Use Modal for dialogs** - Handle confirmation dialogs, form popups, and other scenarios
- **Use Upload for file uploads** - Handle file uploads, image uploads, and other scenarios
- **Use App to wrap application** - Provide context support for static methods
- **Use ConfigProvider for global configuration** - Configure themes, locales, component sizes, and more globally

<!--
Source references:
- https://ant.design/components/overview-cn
- https://ant.design/components/overview
-->
