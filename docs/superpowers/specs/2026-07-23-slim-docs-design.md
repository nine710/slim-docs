# slim-docs 设计文档

**日期：** 2026-07-23  
**状态：** 已批准（brainstorming）  
**Skill 名：** `slim-docs`  
**形态：** 方案 2 — 模板 + 校验脚本  

## 1. 问题

复杂项目把大量说明写进编程智能体的**项目指令入口**（Claude Code 的 `CLAUDE.md`、Codex 等的 `AGENTS.md` 等，职责相同、文件名不同）。入口常被会话级注入 → **每轮常驻税高**，关键规则被淹没。过度精简入口又会导致任务时**缺少必要上下文**。

## 2. 目标与成功标准

| ID | 标准 | 度量 |
|----|------|------|
| **A** | 省上下文 | 入口行数落在分档上限内；专题正文不在入口 |
| **B** | 行为可路由 | 存在可解析的 `agent-docs/index.md`；入口含 load-protocol；index 无断链、无孤儿文 |

**非目标（v1）：**

- 全会话 runtime 监督「是否读了文档」的独立 skill  
- 向量知识库 / RAG  
- 无确认的全自动语义切片并静默提交  
- 强制为每个包生成局部 `CLAUDE.md`  
- 给人浏览优化的文档站信息架构  

## 3. 核心概念

### 3.1 本地项目文档库

- 路径：仓库一级目录 **`agent-docs/`**（不套 `docs/` 或 `.xxx/`）  
- 性质：供 **agent 按需 Read** 的 Markdown 文件集合，**不是** RAG 知识库  
- 人基本不读；写法服务检索与约束，不服务叙事  

### 3.2 薄入口

- 文件：`CLAUDE.md` 与/或 `AGENTS.md`（存在则都处理，专题只存一份）  
- 内容：项目一句话、常用命令、硬约束、极简地图、**load-protocol**、指向 index  
- 禁止：长专题、多域细节堆回入口  

### 3.3 文档分类（主轴 A）

- **按任务/领域槽位**：一篇 ≈ 一类 agent 工作或一个域（如 `auth.md`、`commands-and-verify.md`）  
- **不按**人文类（教程/指南/ADR/参考）做主文件夹结构  
- **`agent-docs/index.md` 是路由真源**：触发词（+ 可选 path glob）→ 文件 → 读完应知道什么  
- 文件名用检索词；篇首 `Read when` / `Out of scope`  

### 3.4 分档 low / medium / high

| 档 | 入口行数 | 专题数（不含 index） | 选题倾向 |
|----|----------|----------------------|----------|
| low | ≲80 | 2–3 | map、commands-and-verify、conventions |
| medium | ≲100 | 4–8 | + 域槽位、testing、gotchas |
| high | ≲120 | 8–20 | 更多域；子目录仅存储，路由仍靠 index |

单篇建议约 80–200 行；过长再按任务拆。  
升档：入口反复超标、重复踩坑、index 对不上任务。  
降档：大量无触发引用的死文档。

## 4. 架构

### 4.1 Skill 包结构

```
slim-docs/
├── SKILL.md
├── references/
│   ├── tiers.md
│   ├── migration-checklist.md
│   ├── entry-template.md
│   ├── index-template.md
│   ├── load-protocol.md
│   └── topic-outlines.md
└── scripts/
    ├── measure_entry.py
    └── check_agent_docs.py
```

- `name` / 目录名：`slim-docs`  
- SKILL.md 目标 &lt;500 行；references **一层深**  
- 安装：`~/.claude/skills/slim-docs/` 或项目 `.claude/skills/slim-docs/` 或本仓库 `skills/slim-docs/`  

### 4.2 目标仓库产物

```
<project-root>/
├── CLAUDE.md              # 若使用 Claude Code：薄
├── AGENTS.md              # 若使用 Codex 等：薄；与上同构协议
└── agent-docs/
    ├── index.md           # 必填路由表
    ├── commands-and-verify.md
    ├── architecture-map.md
    └── <task-or-domain>.md
```

### 4.3 数据流

```
探查入口与仓库 → 定档 → 读 templates
    → 拆分计划（歧义/high 须确认）
    → 写 agent-docs + 瘦入口
    → measure_entry + check_agent_docs
    → 双绿才可宣称完成
```

## 5. 行为设计

### 5.1 主流程步骤

1. **探查** — 入口文件、是否已有 `agent-docs/`、顶层结构（high 加深包边界）  
2. **定档** — 用户指定优先；否则建议一档并一句话确认  
3. **读 references** — tiers、entry、index、load-protocol；按需 outlines、checklist  
4. **规划拆分** — 入口保留项 vs 专题清单；每篇路径 + 触发行；high **必须**先确认计划  
5. **落库** — index + 专题；缺信息 `TODO`，禁止臆造业务规则  
6. **瘦身入口** — 每个存在的入口文件；粘贴 load-protocol  
7. **验收** — 两脚本 exit 0；输出变更列表与结果摘要  
8. **收尾建议** — 维护时改专题与 index，禁止入口回胖  

### 5.2 双入口

| 现状 | 行为 |
|------|------|
| 仅 CLAUDE 或仅 AGENTS | 瘦身该文件，库共用 |
| 两者都有 | 都瘦，协议相同，专题不双份 |
| 都无 | 询问主工具；若需默认可建 `CLAUDE.md` 并说明 |
| 内容冲突 | 入口不各写长套；冲突进专题或 TODO |

### 5.3 拆分启发式（建议式，非静默）

- **迁出：** 长架构、多子系统细节、风格长文、历史决策、大段示例  
- **保留：** 精确命令、安全硬规则、一句话地图、文档库用法  
- **可代码推断：** index/专题指针到路径，不抄源码  

### 5.4 停止条件

- 用户拒绝 `agent-docs/` → 停止  
- 脚本红 → 未完成  
- 已合格瘦身 → 可只校验/小幅升档，不强制打散  

## 6. 模板要点

### 6.1 index 表

列：`triggers (keywords / globs)` | `path` | `read when / get`  

每个非 index 的 md 至少一行；禁止孤儿文件。

### 6.2 专题骨架

```markdown
# <slug>
Read when: ...
Out of scope: ...
## Invariants / hard rules
## Key paths
## Do / Don't
## Verify
## Notes
```

### 6.3 Load protocol（写入入口）

- 任务可能匹配某域时：先读 `agent-docs/index.md`，再只 Read 匹配文件  
- 禁止整库通读 `agent-docs/`  
- 完成前按 commands/verify 验证  

### 6.4 topic-outlines 槽位（可裁剪，非强制文件名）

- low：architecture-map、commands-and-verify、conventions  
- medium：+ 域 ×2–4、testing、gotchas  
- high：更多域槽位  

## 7. 脚本规格

工作目录：目标项目根。Python 3 + 标准库 + pathlib；Windows 可跑。

### 7.1 `measure_entry.py`

```
python measure_entry.py [--tier low|medium|high] [--root .]
```

- 统计 CLAUDE.md / AGENTS.md 行数  
- 对照 80 / 100 / 120  
- exit 0 当存在的入口均 ≤ 上限；否则 1  
- 可对「入口仍像长专题」发警告（非唯一失败条件，除非超行数）  

### 7.2 `check_agent_docs.py`

```
python check_agent_docs.py [--tier low|medium|high] [--root .]
```

- `agent-docs/index.md` 存在且可解析表格行  
- 行内 path 可解析为文件  
- 无孤儿专题 md  
- 专题数 ∈ 档位区间  
- 缺 `Read when` 可警告  
- exit 0/1，stdout 可操作错误列表  

### 7.3 完成定义

**migration-checklist 完成且两脚本 exit 0** → 才可宣称迁移完成。

## 8. SKILL.md 写作约束（实现时）

- **description：** 第三人称；触发含过长 CLAUDE.md/AGENTS.md、拆 agent-docs、瘦身入口、slim agent docs；可含 Do NOT use（例如「不要用于实现业务功能本身」）；**禁止**在 description 写完整迁移流水线  
- **正文：** 步骤 + 硬门禁（脚本）+ 何时读哪个 reference  
- 遵循本仓库 `agent-docs/` 中 skill 写作规范（解剖、渐进披露、测试）  

## 9. 测试计划

| 类 | 用例 |
|----|------|
| 正触发 | 入口太长 / 建 agent-docs / 瘦身 AGENTS.md |
| 负触发 | 纯写功能、无关 markdown 问题 |
| 功能夹具 | 人造超长 CLAUDE.md → 入口≤档、index 通、脚本绿 |
| 双入口 | 两文件都瘦、一份库 |
| 已合格 | 不无故打散 |

实现阶段用 writing-skills / eval 对照「无 skill」基线。

## 10. 风险与缓解

| 风险 | 缓解 |
|------|------|
| 拆分丢规则 | 计划确认；TODO；禁止编造 |
| index 与文件漂移 | check 脚本；完成门禁 |
| 入口再次回胖 | load-protocol + 行数门禁；skill 说明维护纪律 |
| 脚本解析表失败 | 固定简单 markdown 表；错误示例 |
| 误触发 skill | description 负向触发 + 负例 eval |

## 11. 实现范围（供 writing-plans）

1. 创建 `skills/slim-docs/` 包骨架与 SKILL.md  
2. 编写全部 references  
3. 实现并手工跑通两脚本  
4. 用夹具项目做一次端到端迁移  
5. 正/负触发与完成门禁检查  
6. 按需更新本仓库 CLAUDE.md 指向该 skill  

## 12. 决策记录（摘要）

- 成功标准 A+B  
- 主任务：建库/迁移，非 runtime 纪律包  
- 目录：`agent-docs/` 一级  
- 三档 low/medium/high  
- 方案 2：模板 + 脚本  
- 名：`slim-docs`  
- 分类主轴 A：任务/领域槽位  
- 双入口同构支持  
