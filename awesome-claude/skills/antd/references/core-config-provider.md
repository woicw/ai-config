---
name: antd-config-provider
description: Ant Design ConfigProvider component for global configuration of themes, locales, component sizes, and other settings. Use when configuring global Ant Design settings for your application.
---

# ConfigProvider Global Configuration

ConfigProvider is a component in Ant Design for global configuration, providing unified configuration to all child components through Context API, including themes, locales, component sizes, and more.

## Basic Usage

```tsx
import { ConfigProvider } from 'antd';

const App = () => (
  <ConfigProvider>
    <YourApp />
  </ConfigProvider>
);
```

## Theme Configuration

### Basic Theme

```tsx
import { ConfigProvider, theme } from 'antd';

const App = () => (
  <ConfigProvider
    theme={{
      token: {
        colorPrimary: '#1890ff',
        borderRadius: 8,
        fontSize: 14,
      },
    }}
  >
    <YourApp />
  </ConfigProvider>
);
```

### Dark Theme

```tsx
import { ConfigProvider, theme } from 'antd';

const App = () => (
  <ConfigProvider
    theme={{
      algorithm: theme.darkAlgorithm,
    }}
  >
    <YourApp />
  </ConfigProvider>
);
```

### Compact Theme

```tsx
import { ConfigProvider, theme } from 'antd';

const App = () => (
  <ConfigProvider
    theme={{
      algorithm: theme.compactAlgorithm,
    }}
  >
    <YourApp />
  </ConfigProvider>
);
```

### Combined Algorithms

```tsx
import { ConfigProvider, theme } from 'antd';

const App = () => (
  <ConfigProvider
    theme={{
      algorithm: [theme.darkAlgorithm, theme.compactAlgorithm],
    }}
  >
    <YourApp />
  </ConfigProvider>
);
```

### Custom Theme Tokens

```tsx
import { ConfigProvider } from 'antd';
import type { ThemeConfig } from 'antd';

const customTheme: ThemeConfig = {
  token: {
    // Seed tokens (base values)
    colorPrimary: '#1677ff',
    colorSuccess: '#52c41a',
    colorWarning: '#faad14',
    colorError: '#ff4d4f',
    colorInfo: '#1677ff',
    
    // Shared tokens
    borderRadius: 6,
    fontSize: 14,
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    
    // Layout tokens
    sizeUnit: 4,
    sizeStep: 4,
    
    // Motion tokens
    motionDurationFast: '0.1s',
    motionDurationMid: '0.2s',
    motionDurationSlow: '0.3s',
  },
  components: {
    Button: {
      colorPrimary: '#722ed1',
      borderRadius: 20,
      controlHeight: 40,
    },
    Card: {
      headerBg: '#fafafa',
      borderRadiusLG: 12,
    },
    Input: {
      activeBorderColor: '#722ed1',
      hoverBorderColor: '#9254de',
    },
  },
};

const App = () => (
  <ConfigProvider theme={customTheme}>
    <YourApp />
  </ConfigProvider>
);
```

## Internationalization Configuration

### Set Locale

```tsx
import { ConfigProvider } from 'antd';
import zhCN from 'antd/locale/zh_CN';
import enUS from 'antd/locale/en_US';

// Chinese
const AppCN = () => (
  <ConfigProvider locale={zhCN}>
    <YourApp />
  </ConfigProvider>
);

// English
const AppEN = () => (
  <ConfigProvider locale={enUS}>
    <YourApp />
  </ConfigProvider>
);
```

### Dynamic Locale Switching

```tsx
import { useState } from 'react';
import { ConfigProvider } from 'antd';
import zhCN from 'antd/locale/zh_CN';
import enUS from 'antd/locale/en_US';

const App = () => {
  const [locale, setLocale] = useState(zhCN);

  return (
    <ConfigProvider locale={locale}>
      <Button onClick={() => setLocale(locale === zhCN ? enUS : zhCN)}>
        Toggle Language
      </Button>
      <YourApp />
    </ConfigProvider>
  );
};
```

## Component Size Configuration

```tsx
import { ConfigProvider } from 'antd';

// Set component size globally
const App = () => (
  <ConfigProvider componentSize="large">
    <YourApp />
  </ConfigProvider>
);

// Options: 'small' | 'middle' | 'large'
```

## Direction Configuration (RTL)

```tsx
import { ConfigProvider } from 'antd';

// Right-to-left layout
const App = () => (
  <ConfigProvider direction="rtl">
    <YourApp />
  </ConfigProvider>
);

// Options: 'ltr' | 'rtl'
```

## Component Global Configuration

### Set Global Properties for Specific Components

```tsx
import { ConfigProvider } from 'antd';

const App = () => (
  <ConfigProvider
    button={{
      autoInsertSpace: true, // Button component auto insert space
    }}
    input={{
      allowClear: true, // Input component default show clear button
    }}
    form={{
      requiredMark: 'optional', // Form required mark style
    }}
    table={{
      size: 'middle', // Table default size
    }}
  >
    <YourApp />
  </ConfigProvider>
);
```

### Supported Component Configurations

- **button** - Button 组件配置
- **input** - Input 组件配置
- **form** - Form 组件配置
- **table** - Table 组件配置
- **card** - Card 组件配置
- **modal** - Modal 组件配置
- **message** - Message 组件配置
- **notification** - Notification 组件配置

## StyleProvider 与 Tailwind CSS 集成

当项目中同时使用 Ant Design 和 Tailwind CSS 时，可能会遇到 CSS 优先级冲突问题。`StyleProvider` 配合 CSS 层（CSS Layers）可以帮助控制样式优先级，确保 Tailwind CSS 的 utilities 类能够正确覆盖 Ant Design 的样式。

### 基本用法

```tsx
import { createRoot } from 'react-dom/client';
import App from './App';
import { ConfigProvider, App as AntdApp } from 'antd';
import { StyleProvider } from '@ant-design/cssinjs';
import zhCN from 'antd/locale/zh_CN';

import './styles/global.css';

const root = createRoot(document.getElementById('root')!);

root.render(
  <StyleProvider layer>
    <ConfigProvider
      locale={zhCN}
      prefixCls="iflytek"
      theme={{
        token: {
          // Seed Token，影响范围大
          colorPrimary: '#275EFF',
          colorLink: '#275EFF',
          borderRadius: 6,
        },
        components: {
          Alert: {
            colorInfoBorder: '#275EFF',
            colorInfoBg: 'rgba(39, 94, 255, 0.08)',
          },
        },
      }}>
      <AntdApp>
        <App />
      </AntdApp>
    </ConfigProvider>
  </StyleProvider>,
);
```

### CSS 层顺序配置

In the entry CSS file, you need to explicitly declare CSS layer order. Through the `@layer` directive, ensure the `utilities` layer comes after the `antd` layer, so Tailwind CSS class names can correctly override Ant Design styles:

```css
/* Global styles */
/* Explicitly declare CSS layer order: later declared layers have higher priority */
/* Ensure utilities comes after antd, so Tailwind class names can override Ant Design styles */
@layer theme,
base,
antd,
components,
utilities;

@import 'tailwindcss';
```

### Component Nesting Order

The correct component nesting order should be:

1. **StyleProvider** (outermost, using `layer` property)
2. **ConfigProvider** (configure theme, locale, etc.)
3. **AntdApp** (provide context for static methods)
4. **App** (your application component)

```tsx
<StyleProvider layer>
  <ConfigProvider locale={zhCN} theme={theme}>
    <AntdApp>
      <App />
    </AntdApp>
  </ConfigProvider>
</StyleProvider>
```

### How It Works

1. **StyleProvider's `layer` property**: Enables CSS layers feature, placing Ant Design styles into the `antd` layer
2. **CSS layer order**: Declare layer order through `@layer`, later declared layers have higher priority
3. **Style override**: Tailwind CSS's `utilities` layer comes after `antd` layer, so it can correctly override Ant Design styles

### 完整示例

**main.tsx / index.tsx**

```tsx
import { createRoot } from 'react-dom/client';
import App from './App';
import { ConfigProvider, App as AntdApp } from 'antd';
import { StyleProvider } from '@ant-design/cssinjs';
import zhCN from 'antd/locale/zh_CN';

import './styles/global.css';

const root = createRoot(document.getElementById('root')!);

root.render(
  <StyleProvider layer>
    <ConfigProvider
      locale={zhCN}
      theme={{
        token: {
          colorPrimary: '#275EFF',
          borderRadius: 6,
        },
      }}>
      <AntdApp>
        <App />
      </AntdApp>
    </ConfigProvider>
  </StyleProvider>,
);
```

**styles/global.css**

```css
/* 明确声明 CSS 层顺序 */
@layer theme,
base,
antd,
components,
utilities;

@import 'tailwindcss';
```

### StyleProvider 属性

- **layer** (boolean) - 启用 CSS 层功能，将 Ant Design 样式放入 `antd` 层
- **container** (() => HTMLElement) - 自定义样式插入的容器元素
- **cache** (Cache) - 自定义样式缓存实例
- **ssrInline** (boolean) - 是否在 SSR 时内联样式，默认 false
- **transformers** (Transformer[]) - 样式转换器数组

### Recommended Configuration

For projects using Tailwind CSS, the following configuration is recommended:

1. **Use StyleProvider in entry file**:
```tsx
<StyleProvider layer>
  <ConfigProvider>
    <AntdApp>
      <App />
    </AntdApp>
  </ConfigProvider>
</StyleProvider>
```

2. **Declare layer order in entry CSS**:
```css
@layer theme, base, antd, components, utilities;
@import 'tailwindcss';
```

This ensures Tailwind CSS utilities classes can correctly override Ant Design styles while maintaining code maintainability.

## Nested Usage

ConfigProvider supports nested usage, inner configuration will override outer configuration:

```tsx
const OuterProvider = () => (
  <ConfigProvider theme={{ token: { colorPrimary: '#1890ff' } }}>
    <InnerProvider />
  </ConfigProvider>
);

const InnerProvider = () => (
  <ConfigProvider theme={{ token: { colorPrimary: '#722ed1' } }}>
    <YourApp />
    {/* Components here will use #722ed1 as primary color */}
  </ConfigProvider>
);
```

## Static Configuration Method

ConfigProvider also provides static configuration method for configuring global Modal, Message, Notification:

```tsx
import { ConfigProvider } from 'antd';

ConfigProvider.config({
  holderRender: (children) => (
    <ConfigProvider
      prefixCls="ant"
      theme={{ token: { colorPrimary: '#1890ff' } }}
    >
      {children}
    </ConfigProvider>
  ),
});
```

## ConfigProvider Properties

### Basic Properties

- **theme** (ThemeConfig) - Theme configuration
- **locale** (Locale) - Locale configuration
- **componentSize** ('small' | 'middle' | 'large') - Component size
- **direction** ('ltr' | 'rtl') - Text direction
- **space** ({ size: 'small' | 'middle' | 'large' | number }) - Spacing configuration
- **virtual** (boolean) - Virtual scrolling configuration (Table, Select, etc.)

### Component Configuration

- **button** (ButtonConfig) - Button component global configuration
- **input** (InputConfig) - Input component global configuration
- **form** (FormConfig) - Form component global configuration
- **table** (TableConfig) - Table component global configuration
- **card** (CardConfig) - Card component global configuration
- **modal** (ModalConfig) - Modal component global configuration
- **message** (MessageConfig) - Message component global configuration
- **notification** (NotificationConfig) - Notification component global configuration

### Other Properties

- **prefixCls** (string) - Set unified style prefix, default 'ant'
- **iconPrefixCls** (string) - Set unified icon style prefix, default 'anticon'
- **csp** ({ nonce?: string }) - Set Content Security Policy
- **autoInsertSpaceInButton** (boolean) - Auto insert space in button (deprecated, use button.autoInsertSpace)
- **renderEmpty** ((componentName: string) => ReactNode) - Custom empty state rendering
- **dropdownMatchSelectWidth** (boolean) - Dropdown menu and selector same width

## Using theme.useToken() Hook

Get current theme configuration in components:

```tsx
import { theme } from 'antd';

const { token } = theme.useToken();

const MyComponent = () => {
  return (
    <div style={{ color: token.colorPrimary }}>
      Primary Color: {token.colorPrimary}
    </div>
  );
};
```

## Best Practices

1. **Use at application root** - Place ConfigProvider at the root of your application
2. **Theme configuration** - Use token and components to configure custom themes
3. **Internationalization** - Use locale property to configure language
4. **Component configuration** - Use component configuration properties to uniformly set component default behavior
5. **Nested usage** - Leverage nesting feature to set different configurations for different areas
6. **Performance optimization** - Avoid frequently switching theme and locale configurations
7. **Integration with Tailwind CSS** - Use StyleProvider's `layer` property and declare layer order in CSS through `@layer`, ensuring `utilities` layer comes after `antd` layer
8. **Component nesting order** - Nest components in the order: StyleProvider -> ConfigProvider -> AntdApp -> App

<!--
Source references:
- https://ant.design/components/config-provider-cn
- https://github.com/ant-design/ant-design/blob/master/components/config-provider/index.en-US.md
-->
