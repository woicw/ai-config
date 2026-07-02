---
name: react-webapp-builder
description: Woic's coding patterns and conventions for React web applications. MUST use when writing, modifying, or reviewing any React application code — components, hooks, pages, forms, tables, modals, CRUD flows, data fetching (useRequest/axios), state management (Zustand stores), routing (React Router), file organization and naming. Applies to any React webapp project; preferred stack is React + TypeScript + Vite + Tailwind CSS + ahooks + antd/shadcn-ui. Load BEFORE writing React feature code.
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
| patterns-files | file, folder, naming, export, kebab-case, index.tsx | 文件/目录命名与导出规范（连字符命名、组件目录约定、统一命名导出） |
| patterns-component | component, hook, state, event, utility, type, cn | 组件结构、组件级 hooks（逻辑与视图分离）、自定义 Hooks、工具函数、类型定义 |
| patterns-data-fetching | useRequest, fetch, api, request, loading | 数据请求模式（useRequest、分页、轮询） |
| patterns-modal | modal, dialog, AntdModal, showModal, useAntModal | Modal 封装（AntdModal 完整实现 + 表单弹窗用例）**[需要 antd]** |
| patterns-zustand | zustand, store, state, userInfo, permission | Zustand Store 模式（用户状态、权限、拦截器） |
| scenarios-crud | crud, table, form, list, create, edit, delete | CRUD 业务场景（列表 + 搜索 + 表单提交）**[示例基于 antd]** |

**UI 库适配**：先检查项目实际使用的 UI 库（看 `package.json`）。标注 **[需要 antd]** / **[示例基于 antd]** 的规则，其代码示例基于 antd 编写：

- 项目用 antd → 直接套用。
- 项目用 shadcn/ui 或其他 UI 库 → 只借鉴其中的封装思路（API 设计、状态流转），组件实现改用项目现有 UI 库。**严禁**为套用示例而向项目引入 antd。
- 其余未标注的规则与 UI 库无关，任何 React 项目均适用。

对应规则文件：

- `patterns-files` -> `rules/patterns-files.md`
- `patterns-component` -> `rules/patterns-component.md`
- `patterns-data-fetching` -> `rules/patterns-data-fetching.md`
- `patterns-modal` -> `rules/patterns-modal.md`
- `patterns-zustand` -> `rules/patterns-zustand.md`
- `scenarios-crud` -> `rules/scenarios-crud.md`

## External References

- **shadcn/ui**: <https://ui.shadcn.com/docs/components>
- **antd**: <https://ant.design/components/overview-cn>
- **ahooks**: <https://ahooks.js.org/zh-CN>
- **Zustand**: <https://zustand-demo.pmnd.rs/>
- **axios**: <https://axios-http.com/>
- **react-router**: <https://reactrouter.com/>
