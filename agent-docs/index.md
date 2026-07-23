# agent-docs 索引

本地**项目文档库**（供 agent 按需加载，不是 RAG 知识库）。  
写/改 skill、设计本仓库 skill 前，按任务读对应文件，**不要**整库一次性读入。

| 主题 | 路径 | 何时读 |
|------|------|--------|
| Skill 目录与文件解剖 | [skill-anatomy.md](./skill-anatomy.md) | 新建 skill 目录、选 scripts/references/assets 时 |
| 三层渐进披露 | [progressive-disclosure.md](./progressive-disclosure.md) | 控制体积、拆分 SKILL.md、设计加载顺序时 |
| description 与触发 | [description-and-triggers.md](./description-and-triggers.md) | 写/改 frontmatter、skill 不触发或误触发时 |
| 优秀正文写法 | [writing-patterns.md](./writing-patterns.md) | 写步骤、模板、自由度、gotchas 时 |
| 测试与迭代 | [testing-and-evals.md](./testing-and-evals.md) | 发布前验证、RED-GREEN、eval 设计时 |
| 反模式与检查表 | [quality-checklist.md](./quality-checklist.md) | 自检、code review skill 时 |
| 来源与范例 | [sources-and-examples.md](./sources-and-examples.md) | 需要对照官方仓库/本地已装 skill 时 |
| 本仓库目标 skill 约定 | [target-skill-context.md](./target-skill-context.md) | 继续设计「薄入口 + agent-docs 迁移」skill 时 |

## 加载纪律（给 agent）

1. 先读本 index，只打开与当前任务相关的 1–2 篇。  
2. 参考文件从 SKILL.md **一层**链出；不要嵌套「参考的参考」。  
3. 能跑脚本验证的不要只靠散文记忆。  
4. 项目专属约定写 `CLAUDE.md`；可复用流程写 skill；事实细节写 `agent-docs/` 专题。
