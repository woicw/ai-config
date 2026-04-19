# AI Config

个人 AI 助手配置仓库，主要维护 [awesome-claude](/Users/woic/woicw/ai-config/awesome-claude) 下的：

- `skills/`：本地技能与远程同步技能
- `commands/`：可复用命令工作流
- `.mcp.json`：MCP Server 配置

## 项目结构

```text
ai-config/
├── awesome-claude/
│   ├── skills/
│   ├── commands/
│   ├── mcp/
│   ├── skills.manifest.json
│   └── scripts/sync_skills_from_manifest.py
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

远程 skill 使用 [skills.manifest.json](/Users/woic/woicw/ai-config/awesome-claude/skills.manifest.json) 作为单一事实源。

- 本地自写 skill：`source: "local"`
- 远程 skill：记录 `source` 和 `skillId`
- `source` 直接复用 `skills.sh` / 搜索 API 返回的仓库标识，例如 `vercel-labs/agent-skills`
- GitHub URL 不写死在 manifest 里，由同步脚本自动拼成 `https://github.com/<source>`

远程 skill 条目示例：

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

## 同步命令

推荐直接用根目录 `package.json` 的快捷命令：

```bash
pnpm run skills:add -- npx skills add https://github.com/vercel-labs/agent-skills --skill vercel-react-best-practices
pnpm run skills:list
pnpm run skills:check
pnpm run skills:sync
pnpm run skills:sync -- zustand
pnpm run skills:sync:existing
```

等价的脚本入口是：

```bash
python3 awesome-claude/scripts/sync_skills_from_manifest.py add npx skills add https://github.com/vercel-labs/agent-skills --skill vercel-react-best-practices
python3 awesome-claude/scripts/sync_skills_from_manifest.py list
python3 awesome-claude/scripts/sync_skills_from_manifest.py check
python3 awesome-claude/scripts/sync_skills_from_manifest.py sync
python3 awesome-claude/scripts/sync_skills_from_manifest.py sync zustand
```

### 新增远程 Skill

如果你从 `skills.sh` 复制到了这样的命令：

```bash
npx skills add https://github.com/vercel-labs/agent-skills --skill vercel-react-best-practices
```

直接执行：

```bash
pnpm run skills:add -- npx skills add https://github.com/vercel-labs/agent-skills --skill vercel-react-best-practices
```

它会自动：

1. 解析 repo URL
2. 提取 `--skill`
3. 写入 `awesome-claude/skills.manifest.json`

然后再同步：

```bash
pnpm run skills:sync -- vercel-react-best-practices
```

### 同步策略

- `skills:sync`：同步所有远程 skill
- `skills:sync -- <name>`：只同步一个 skill
- `skills:sync:existing`：只更新当前已经存在于 `awesome-claude/skills/` 的远程 skill

当前同步器把 manifest 中的远程 skill 视为上游权威版本；如果远程 skill 同名目录已存在，会以最新同步结果替换它。

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
