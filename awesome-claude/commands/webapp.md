---
allowed-tools: ReadFile, WriteFile, EditFile, CreateFile, Bash, CodebaseSearch, Grep, ListFiles
description: Understand user requirements and build React webapp using react-webapp-builder skill
---

# Webapp Builder Command

## User Requirements

$ARGUMENTS

## Your Task

使用 **react-webapp-builder** skill 设计开发 React Web 应用。

### 执行流程

#### 1. 需求理解与分析

首先深入理解用户需求：

- **功能拆解**：将需求拆分为具体功能点
- **页面识别**：确定需要哪些页面/组件
- **数据模型**：识别核心数据实体及其关系
- **交互流程**：梳理用户操作流程
- **边界情况**：考虑异常和边界场景

#### 2. 需求优化与确认

基于分析，输出优化后的需求文档：

```markdown
## 功能需求
- [ ] 功能点1
- [ ] 功能点2

## 页面结构
- 页面A: 描述
- 页面B: 描述

## 数据模型
- Entity1: 字段列表
- Entity2: 字段列表

## 技术方案
- 状态管理: 方案
- API 设计: 接口列表
- 组件规划: 组件树
```

#### 3. 代码实现

按照 react-webapp-builder skill 规范进行开发：

1. **项目结构**：遵循目录规范 (components, hooks, stores, pages, services, utils, types)
2. **状态管理**：使用 Zustand，注意选择器优化
3. **数据请求**：使用 ahooks + axios 封装
4. **UI 组件**：使用 antd 或 shadcn/ui
5. **样式**：使用 Tailwind CSS
6. **类型安全**：完整的 TypeScript 类型定义

#### 4. 实现顺序

1. 类型定义 (`types/`)
2. API 服务 (`services/`)
3. 状态管理 (`stores/`)
4. 自定义 Hooks (`hooks/`)
5. UI 组件 (`components/`)
6. 页面组件 (`pages/`)

### 输出要求

- 代码遵循函数式编程风格
- 组件保持单一职责
- 提供必要的注释说明
- 确保类型完整无 any
