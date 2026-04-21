# AI Config

个人 AI 助手配置仓库，主要维护 [awesome-claude](/Users/woic/woicw/ai-config/awesome-claude) 下的：

- `skills/`：本地自写技能
- `commands/`：可复用命令工作流
- `.mcp.json`：MCP Server 配置

## 项目结构

```text
ai-config/
├── awesome-claude/
│   ├── skills/            # 本地自写 skill
│   ├── commands/          # 可复用命令
│   ├── mcp/               # MCP server 配置
│   └── skills.manifest.json
├── docs/plans/            # 设计 / 实施计划文档
└── package.json
```

## 常用方式

### 使用 Skills

Skills 会按任务自动触发，也可以手动引用：

```text
@vue-best-practices 帮我检查这个 Vue 组件的类型问题
```

### 使用 Commands

Commands 通过 `/` 命令触发：

```text
/commit
```

## 远程 Skills 同步

远程 skill 分发由 [`wrs`](https://github.com/woicw/wr-ai) 管理。使用 `skills.manifest.json` 来声明需要同步的远程 skill。

快速开始：

```bash
pnpm add -g wrs
wrs set github woicw/ai-config
wrs sync            # 首次交互选择；之后会记住
wrs sync --refresh  # 强制从上游重新拉取所有远程 skill
wrs cache clean     # 清空本地 skill 缓存
```

### Manifest 格式

本地自写 skill 标记为 `source: "local"`：

```json
{
  "name": "my-local-skill",
  "source": "local"
}
```

远程 skill 指定 `source` (GitHub 仓库标识) 和 `skillId`：

```json
{
  "name": "vercel-react-best-practices",
  "source": "vercel-labs/agent-skills",
  "skillId": "vercel-react-best-practices"
}
```

如果本地目录名和远程 skillId 不一致，可以加 `installName`：

```json
{
  "name": "skill-creator-anthropics",
  "source": "anthropics/skills",
  "skillId": "skill-creator",
  "installName": "skill-creator-anthropics"
}
```

## 添加本地 Skill

本地 skill 直接在 `awesome-claude/skills/` 下手写即可，然后在 manifest 里登记为：

```json
{
  "name": "my-local-skill",
  "source": "local"
}
```

## 添加 Command

在 `awesome-claude/commands/` 下创建 `.md` 文件，并包含 YAML frontmatter：

- `allowed-tools`
- `description`

可参考：

- [commit.md](/Users/woic/woicw/ai-config/awesome-claude/commands/commit.md)

## MCP 配置

编辑 [awesome-claude/.mcp.json](/Users/woic/woicw/ai-config/awesome-claude/.mcp.json) 添加或修改 MCP Server 配置。

注意：

- 配置中的敏感信息使用占位符
- 不要提交真实 token / 密钥

## 参考来源

- [anthropics/skills](https://github.com/anthropics/skills)
- [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)
- [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills)
- [Anthony Fu](https://github.com/antfu)
- [Claude Skills 文档](https://docs.anthropic.com/claude/docs/skills)
- [MCP 协议文档](https://modelcontextprotocol.io/)
