# 来源与范例

调研日期：2026-07-23。链接便于复查；正文以本库其他篇的归纳为准。

## 规范与文档

| 资源 | 用途 |
|------|------|
| [github.com/agentskills/agentskills](https://github.com/agentskills/agentskills) | 开放 Agent Skills 格式：文件夹 + SKILL.md；Discovery→Activation→Execution |
| [agentskills.io](https://agentskills.io) | 规范站点与客户端列表（网络策略下可能需直打开） |
| [platform.claude.com … agent-skills/best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | Anthropic 官方写作：简洁、description、渐进披露、工作流 |
| [github.com/mgechev/skills-best-practices](https://github.com/mgechev/skills-best-practices) | 结构、description、验证话术、反 README-in-skill 等浓缩实践 |

## 官方 / 示例仓库

| 资源 | 用途 |
|------|------|
| [github.com/anthropics/skills](https://github.com/anthropics/skills) | 官方示例 skill 集 |
| `skills/pdf` | 薄正文 + forms/reference + scripts |
| `skills/docx` | gotchas 驱动、验证输出 |
| `skills/mcp-builder` | 分阶段流程 + reference/scripts |
| `skills/skill-creator` | 元 skill：起草、eval、description 优化 |
| `skills/webapp-testing` | 决策树 + 脚本黑盒 |
| `skills/claude-api` | 超大参考 + TRIGGER/SKIP + 分语言加载 |

## 本地可对照（本机已装）

路径前缀因版本而异，以插件缓存为准：

| Skill | 观察点 |
|-------|--------|
| `superpowers/.../writing-skills` | TDD 写 skill、CSO、测试子代理 |
| `superpowers/.../brainstorming` | HARD-GATE、检查表、流程图 |
| `superpowers/.../test-driven-development` | Iron Law、Red flags、借口表 |
| `superpowers/.../verification-before-completion` | 完成前证据门禁 |
| `~/.claude/skills/console-design` | Required reading order + references + assets |

随附深读：

- `writing-skills/anthropic-best-practices.md`（官方最佳实践全文拷贝向）  
- `writing-skills/testing-skills-with-subagents.md`

## 社区讨论中的稳定共识（2025–2026）

- Skill 包 = 便携 procedural knowledge，跨 Claude Code / 其他兼容客户端  
- 渐进披露是默认架构；description 质量决定「隐形 skill」  
- 仓库入口文件应薄；细则 docs / 局部说明 / skills  
- 第三方 skill 需审 scripts（注入与供应链）  

X/社区线索仅作旁证，以仓库与官方文档为准。

## 本仓库如何用这些来源

1. 写 skill 前：`index.md` → `skill-anatomy` + `progressive-disclosure` + `description-and-triggers`  
2. 写正文时：`writing-patterns` + `quality-checklist`  
3. 发布前：`testing-and-evals`  
4. 设计「文档库迁移」skill：`target-skill-context.md`
