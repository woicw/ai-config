# AI Config

个人 AI 助手配置仓库，包含 Claude Skills、Commands 和 MCP Servers 配置。

## 📁 项目结构

```
ai-config/
├── awesome-claude/          # Claude Skills 和 Commands
│   ├── skills/             # Skills 集合
│   ├── commands/           # Commands 集合
│   └── .mcp.json          # MCP Servers 配置
└── package.json
```

## 🎯 功能特性

### Skills

Skills 是模块化的知识包，为 Claude 提供专业领域的知识和工作流。

#### 前端开发 Skills

- **React** - React 核心概念、Hooks、模式和实践
- **Vue** - Vue 3 组件、组合式 API、TypeScript 支持
- **Vue Best Practices** - Vue 类型检查、Volar 配置、最佳实践
- **VueUse Functions** - VueUse 函数库完整参考
- **Next.js** - Next.js 路由、布局、元数据生成
- **React Router** - React Router v6+ 数据加载、导航
- **Vite** - Vite 配置、插件开发、构建优化
- **Turborepo** - Monorepo 任务编排、缓存、CI/CD
- **Zustand** - 状态管理最佳实践
- **Ant Design** - Ant Design 组件使用指南
- **ahooks** - ahooks 核心 Hook 使用

#### 工具开发 Skills

- **tsdown** - TypeScript 库打包工具
- **MCP Builder** - MCP Server 开发指南
- **Code Review** - 代码审查最佳实践

#### Skill 创建工具

- **skill-creator** - 创建新 Skill 的指南和工具
- **skill-from-github** - 从 GitHub 项目学习创建 Skill
- **skill-from-masters** - 从专家方法论创建 Skill
- **skill-from-notebook** - 从文档/笔记提取 Skill
- **search-skill** - 搜索和推荐 Skills

#### 自定义 Skills

- **woic** - 个人开发规范和最佳实践
  - Monorepo 配置
  - ESLint 配置（Antfu）
  - Git 工作流
  - GitHub Actions
  - 应用和库开发规范

### Commands

Commands 是标准化的可重复工作流。

- **commit** - Git 提交和推送工作流（遵循 Conventional Commits）

### MCP Servers

配置的 MCP (Model Context Protocol) Servers：

- **sequential-thinking** - 顺序思考工具
- **console-ninja** - 运行时日志和错误监控
- **API-Doc** - Apifox API 文档查询
- **@21st-dev/magic** - UI 组件生成和搜索
- **shadcn-ui-server** - shadcn/ui 组件管理
- **context7** - 文档查询和代码示例检索
- **chrome-devtools** - Chrome DevTools 自动化

## 🚀 快速开始

### 安装依赖

```bash
pnpm install
```

### 使用 Skills

Skills 会根据你的任务描述自动触发，也可以手动引用：

```
@vue-best-practices 帮我检查这个 Vue 组件的类型问题
```

### 使用 Commands

Commands 通过 `/` 命令触发：

```
/commit
```

## 📝 添加新 Skill

1. 在 `awesome-claude/skills/` 目录下创建新目录
2. 创建 `SKILL.md` 文件，包含：
   - YAML frontmatter（name, description）
   - Markdown 指令内容
3. 可选：添加 `references/`、`scripts/`、`assets/` 目录

参考 `skill-creator` skill 获取详细指南。

## 📝 添加新 Command

1. 在 `awesome-claude/commands/` 目录下创建 `.md` 文件
2. 包含 YAML frontmatter：
   - `allowed-tools`: 允许使用的工具
   - `description`: 命令描述
3. 定义工作流程和步骤

参考 `commit.md` 作为示例。

## 🔧 配置 MCP Servers

编辑 `awesome-claude/.mcp.json` 添加或修改 MCP Server 配置。

**注意**: 配置中的敏感信息（如 token）应使用占位符 `<your-token>`，不要提交真实凭证。

## 🙏 致谢与参考来源

本项目中的 Skills 参考和集成了以下优秀的开源项目和社区资源：

### 社区开源 Skills

部分 Skills 来自社区开源项目，通过同步机制集成：

- **turborepo** - 来自 `vendor/turborepo/skills/turborepo`
- **vueuse-functions** - 来自 `vendor/vueuse/skills/vueuse-functions`
- **vue-best-practices** - 来自社区 Vue 最佳实践
- **web-design-guidelines** - 来自社区 Web 设计指南

### Anthony Fu (antfu) 开源实现

skill 中大量参考了 [Anthony Fu](https://github.com/antfu) 的开源项目和最佳实践：

- **[@antfu/eslint-config](https://github.com/antfu/eslint-config)** - ESLint 扁平配置，替代 Prettier
- **[@antfu/ni](https://github.com/antfu/ni)** - 统一的包管理器命令工具
- **Anthony Fu 的开发规范** - 包括：
  - `.gitignore` 配置偏好
  - 库开发最佳实践
  - GitHub Actions 工作流（使用 `sxzz/workflows`）
  - 应用开发规范（Vue、Vite/Nuxt、UnoCSS）

### 社区资源

Skills 的创建和优化参考了以下社区资源：

- [anthropics/skills](https://github.com/anthropics/skills) - Claude 官方 Skills 示例
- [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) - 精选的 Claude Skills 集合
- [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) - 社区整理的 Skills 集合

### 同步信息

部分 Skills 包含 `SYNC.md` 文件，记录了同步来源和版本信息，便于追踪和更新。

## 📚 相关资源

- [Claude Skills 文档](https://docs.anthropic.com/claude/docs/skills)
- [MCP 协议文档](https://modelcontextprotocol.io/)
- [Awesome Claude Skills](https://github.com/anthropics/skills)
- [Anthony Fu's GitHub](https://github.com/antfu)

## 📄 License

MIT

## 👤 Author

woic
