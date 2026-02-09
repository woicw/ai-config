---
name: react-webapp-builder
description: Guidelines and patterns for React business web application development. This skill should be used when developing features with React + TypeScript + Vite + Zustand + Tailwind CSS + ahooks + axios + React Router stack, using antd or shadcn/ui components. Provides code patterns, best practices, and examples for common business scenarios like forms, tables, CRUD operations, and state management.
---

# React Webapp Builder

Code patterns and best practices for business web application development.

## Tech Stack

| Category | Technology | Purpose |
|----------|-----------|---------|
| Framework | React 19+ | Functional components + Hooks |
| Language | TypeScript | Type safety |
| Build | Vite | Dev & build |
| State | Zustand | Global state management |
| Styling | Tailwind CSS | Atomic CSS |
| Hooks | ahooks | Common hooks library |
| HTTP | axios | Request client |
| Components | antd / shadcn/ui | UI components |
| Data Fetching | useRequest |
| Routing | React Router |

## Directory Structure

```
src/
├── components/             # Shared components
│   ├── custom-component
│   │   └── index.tsx       # Custom component implementation
│   └── ui/                 # shadcn/ui UI components
├── hooks/                  # Custom hooks
├── constants/              # Constants
├── routes/                 # Route configuration
├── stores/                 # Zustand stores
├── pages/                  # Page components
│   └── custom-page
│        ├── components/         # Page-specific components
│        ├── hooks/              # Page-specific hooks
│        ├── helpers.ts(x)       # Page helper functions
│        ├── types.ts(x)         # Page type definitions
│        └── index.tsx           # Page entry point
├── services/               # API services
├── styles/                 # Style files
├── utils/                  # Utility functions
└── types/                  # Type definitions
```

## Capability Rules

| Rule | Keywords | Description |
|------|----------|-------------|
| patterns-component | component, hook, utility, type, cn | 组件结构、自定义 Hooks、工具函数、类型定义 |
| patterns-data-fetching | useRequest, fetch, api, request, loading | 数据请求模式（useRequest、分页、轮询） |
| patterns-modal | modal, dialog, AntdModal, showModal, useAntModal | Modal 封装（AntdModal 完整实现 + 表单弹窗用例） |
| patterns-zustand | zustand, store, state, userInfo, permission | Zustand Store 模式（用户状态、权限、拦截器） |
| scenarios-crud | crud, table, form, list, create, edit, delete | CRUD 业务场景（列表 + 搜索 + 表单提交） |

## External References

- **shadcn/ui**: <https://ui.shadcn.com/docs/components>
- **antd**: <https://ant.design/components/overview-cn>
- **ahooks**: <https://ahooks.js.org/zh-CN>
- **Zustand**: <https://zustand-demo.pmnd.rs/>
- **axios**: <https://axios-http.com/>
- **react-router**: <https://reactrouter.com/>
