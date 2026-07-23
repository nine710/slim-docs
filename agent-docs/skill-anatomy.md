# Skill 解剖：合规目录与职责

## 一句话

Skill = **可版本管理的文件夹**；核心是 `SKILL.md`（YAML 门禁 + Markdown 规程），可选捆绑脚本与按需文档。

## 标准目录（开源规范 + 官方实践）

```
skill-name/                 # kebab-case，必须与 frontmatter name 一致
├── SKILL.md                # 必填：name + description + 正文指令
├── scripts/                # 可选：确定性/脆弱操作的可执行脚本（当黑盒 CLI 用）
├── references/             # 可选：长文档、schema、领域细则（触发后再读）
└── assets/                 # 可选：输出模板、字体、静态资源（写入产物，不默认进上下文）
```

来源对齐：

- 开放格式说明：[agentskills/agentskills](https://github.com/agentskills/agentskills)
- 官方示例仓：[anthropics/skills](https://github.com/anthropics/skills)（`skills/pdf`、`docx`、`mcp-builder`、`skill-creator` 等）
- 社区浓缩清单：[mgechev/skills-best-practices](https://github.com/mgechev/skills-best-practices)

## 各层职责

| 部件 | 进上下文的时机 | 写什么 | 不写什么 |
|------|----------------|--------|----------|
| **name + description** | 几乎始终（发现/路由） | 能力 + 触发场景 + 可选负向触发 | 完整工作流摘要（易导致只跟 description 不读正文） |
| **SKILL.md 正文** | description 命中后 | 步骤、决策树、硬门禁、何时读哪个 reference | 大段 API 表、多语言重复示例 |
| **references/** | 正文点名再读 | 深参考、分域文档 | 嵌套再指第三层细节文件 |
| **scripts/** | 执行时（优先 `--help`，勿先整文件 Read） | 解析、校验、脚手架 | 大型库代码（应放项目 CLI） |
| **assets/** | 生成产物时复制/套用 | 模板、schema 样例 | 当说明书塞进主上下文 |

## Frontmatter 硬约束（实务）

| 字段 | 约束 |
|------|------|
| `name` | 1–64 字符；小写字母/数字/连字符；与目录名一致；避免空泛名（helper/utils） |
| `description` | ≤1024 字符；**第三人称**；含 what + when；宜含关键词与「Do NOT use for…」 |
| 可选 | `license` 等（官方部分 skill 有） |

命名偏好：动名词/能力向（processing-pdfs、writing-skills）；与 folder 严格一致。

## 安装位置（Claude Code / 生态）

| 范围 | 典型路径 |
|------|----------|
| 个人 | `~/.claude/skills/<name>/` |
| 项目 | `.claude/skills/<name>/` |
| 插件 | 插件自带 skills（缓存目录只读，改了会丢） |

Codex 等客户端可能用 `~/.agents/skills/` 等路径，**格式仍是同一套 SKILL.md 包**。

## 与相近概念的边界

| 概念 | 角色 |
|------|------|
| **Skill** | 按需加载的「任务菜谱 / 领域流程」 |
| **CLAUDE.md / AGENTS.md** | 仓库级常驻指令入口（应薄） |
| **MCP** | 工具与外部系统连接（厨房） |
| **Hooks** | 确定性门禁（格式化、禁目录），不靠模型记 |
| **Slash command** | 用户显式触发的命令文案；不等同自动发现 skill |

## 官方 skill 结构快照（anthropics/skills）

| Skill | 结构要点 |
|-------|----------|
| `pdf` | 薄 SKILL.md + `forms.md` / `reference.md` + `scripts/` |
| `docx` | 正文以 gotchas/决策表为主，细节脚本化 |
| `mcp-builder` | 分阶段流程 + `reference/` + `scripts/` |
| `skill-creator` | 元 skill：起草→eval→迭代；含 `references/`、`scripts/`、eval 工具 |
| `webapp-testing` | 决策树 + 「先 `--help` 再读脚本源码」防污染上下文 |
| `claude-api` | 超大参考型：强 TRIGGER/SKIP + 分子目录按语言加载 |

## 设计推论（写我们自己的 skill 时）

1. 一个 skill ≈ **一个原子任务**（可组合，不要巨型万能包）。  
2. SKILL.md 是导航 + 主流程；胖内容下沉 references/assets/scripts。  
3. 脚本优先于「让模型每次重写脆弱逻辑」。  
4. 不要在 skill 目录里塞给人看的 README/CHANGELOG 当运行时依赖（规范建议：面向 agent 的包保持干净）。
