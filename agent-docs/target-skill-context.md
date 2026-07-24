# 目标 skill 设计上下文（进行中）

本文记录 brainstorming 已对齐的产品决策，供后续方案/规格引用。

**Status:** skill package at `skills/slim-docs/`; design at `docs/superpowers/specs/2026-07-23-slim-docs-design.md`; plan at `docs/superpowers/plans/2026-07-24-slim-docs.md`.

## 问题

复杂项目把大量说明塞进 `CLAUDE.md` / `AGENTS.md` 等**编程智能体项目指令入口** → 每会话常驻过长 → 上下文税高、关键规则易被淹没。  
过度删减入口又会导致「该知道的不知道」。

## 成功标准（用户）

- **A 省上下文**：入口显著变短，默认不注入专题长文  
- **B 行为正确**：做某子系统任务时，agent **稳定读到**对应本地文档  

## 解法骨架

1. 仓库一级目录 **`agent-docs/`** 作为**本地项目文档库**（供 agent 按需 Read，不是向量知识库）  
2. 入口文件（名因工具而异，职责相同）保持**薄内核**：命令、硬约束、地图、`agent-docs` 用法  
3. **`agent-docs/index.md`** 路由：主题 → 路径 → 何时读  
4. 迁移/建库时可选 **low / medium / high** 三档精细度（篇数与主题覆盖；入口仍设行数上限）

## 入口文件（同构）

| 工具/生态 | 典型入口文件 |
|-----------|----------------|
| Claude Code | `CLAUDE.md` |
| Codex 等 | `AGENTS.md` |

Skill 应**同时支持**：同一 `agent-docs/`，为存在的入口文件写入相同加载协议（可略调标题）。

## Skill 主任务范围（用户选定）

- **主：A 建库/迁移** — 拆长入口、生成/填充 `agent-docs/`、索引、入口模板  
- **非主：运行时全会话纪律**（可在入口留一小段加载协议；不做大型 runtime skill）

## 三档（已接受草案）

| 档 | 入口行数目标 | 专题数（不含 index） | 倾向 |
|----|----------------|----------------------|------|
| low | ≲80 | 2–3 | 地图 + 命令 +（可选）约定 |
| medium | ≲100 | 4–8 | + 边界、子系统、测试、坑 |
| high | ≲120 | 8–20 | 域槽位更多；存储可用子目录，**分类仍按任务路由** |

统一：必有 `agent-docs/index.md`；单篇建议约 80–200 行，过长再拆。

## 文档分类（已锁定）

- **主轴 A：任务/领域槽位** — 一篇 ≈ 一类 agent 工作或一个域（`auth.md`、`commands-and-verify.md`），**不是**教程/ADR/参考等人文类
- **index 为路由真源**：每行 = 触发词（+ 可选路径 glob）→ 文件 → 读完应知道什么
- 文件名用检索词；篇首 `Read when` / `Out of scope`；人基本不读，少散文
- high 若文件多，子目录仅作存储，不改「按任务路由」主轴

## 与 Skill 最佳实践的对齐方式

本 skill 自身应：

- 合规包结构：`SKILL.md` + `references/`（三档模板、入口模板）+ 可选 `scripts/`（统计行数/检查 index 链接）  
- description：触发「CLAUDE.md/AGENTS.md 过长、拆文档库、agent-docs 迁移」等，**不**在 description 里写完整迁移流水线  
- 正文：分步迁移检查表 + 何时读哪个 reference 模板  
- 用 eval：给定人造过长 CLAUDE.md → 产物入口变短且 index 可路由  

## 已锁定实现形态

- **方案 2**：模板 + 校验脚本  
- **name（已锁定）**：`slim-docs`（目录与 frontmatter 一致）  
- **v1 不做**：runtime 全会话纪律 skill、RAG、无确认的全自动语义切片、强制包级局部入口  

## 仍可在设计中敲定

- 旧内容拆分：启发式建议 + 用户/agent 确认边界（非全自动无审）  
- high 档是否「可选建议」包级局部入口（默认否或仅文档一句）  
- scripts 语言（Python vs bash）与 Windows 友好性
