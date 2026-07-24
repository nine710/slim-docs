# slim-docs

[English](README.md) | [中文](README.zh-CN.md)

**Agent Skill（智能体技能）**：把过长的项目指令入口文件（`CLAUDE.md`、`AGENTS.md` 等）迁移为**薄入口** + 本地 **`agent-docs/`** 任务槽位文档库，并用索引做按需路由。

兼容 [Agent Skills](https://agentskills.io) 格式（`SKILL.md` + 可选 `references/` + `scripts/`）。

## 要解决什么问题

`CLAUDE.md` / `AGENTS.md` 写太长时，往往**每个会话都会整文件注入**，既占上下文，又容易淹没硬规则；若只靠「拼命删短」，又会出现 agent 该知道的项目事实找不到。

## 做法

| 层级 | 作用 |
|------|------|
| **薄入口** | 只保留命令、硬约束、极简地图、**加载协议** |
| **`agent-docs/index.md`** | 路由表：触发词 → 专题路径 → 何时读 |
| **专题文件** | **任务/领域槽位**（如 `auth.md`、`commands-and-verify.md`），不是给人看的「教程/ADR」分类 |
| **分档** | `low` / `medium` / `high` 控制入口行数上限与专题数量 |

**成功标准：**

- **A — 少占常驻上下文：** 入口行数落在分档上限内  
- **B — 能按需读到对的文档：** 健康 index + 入口内加载协议  

## 何时使用

- 入口文件过长或不断膨胀  
- 需要给编程 agent 的 `agent-docs/`（不是产品文档站 / 不是 RAG 向量库）  
- 同时使用 Claude Code（`CLAUDE.md`）与 Codex 类工具（`AGENTS.md`），共用**一份**文档库  

## 何时不要用

- 与「整理 agent 指令结构」无关的业务功能开发  
- 搭建向量检索 / RAG 知识库  
- 期望一个「全程监督 agent 每步必读文档」的运行时纪律 skill（v1 是**建库/迁移**，不是会话内监察）

## 安装

### Claude Code（个人 skills）

```bash
git clone https://github.com/nine710/slim-docs.git ~/.claude/skills/slim-docs
```

Windows（Git Bash）：

```bash
git clone https://github.com/nine710/slim-docs.git "$USERPROFILE/.claude/skills/slim-docs"
```

目录名需保持为 `slim-docs`（与 skill 的 `name` 一致）。

### 项目级 skill

```bash
git clone https://github.com/nine710/slim-docs.git .claude/skills/slim-docs
```

### 更新

```bash
cd ~/.claude/skills/slim-docs && git pull
```

新开 Claude Code 会话以便重新发现 skill。

## 使用

在入口过长的项目里，可以对 agent 说例如：

- 「`CLAUDE.md` 太长了，用 agent-docs 瘦身，档位 medium。」  
- 「建 `agent-docs/`，把 `CLAUDE.md` 和 `AGENTS.md` 都改成薄入口。」  
- 「把项目 agent 说明迁到渐进加载文档，档位 low。」  

流程概要：探查 → 定档 → 拆分计划 → 写文档库 → 瘦入口 → **脚本硬门禁**。

### 形态对比（示意）

**之前（每会话为全文付税）：**

```text
CLAUDE.md   （300+ 行：架构长文、鉴权、账单、风格……）
```

**之后：**

```text
CLAUDE.md                 # 薄：命令 + 硬规则 + 加载协议
AGENTS.md                 # 可选；协议相同、库共用
agent-docs/
  index.md                # 触发词 → 路径
  architecture-map.md
  commands-and-verify.md
  auth.md                 # 任务/领域槽位…
```

## 分档

| 档位 | 入口最大行数 | 专题数（不含 index） |
|------|--------------|----------------------|
| low | 80 | 2–3 |
| medium | 100 | 4–8 |
| high | 120 | 8–20 |

详见 [`references/tiers.md`](references/tiers.md)。

## 校验脚本（完成硬门禁）

在**目标项目根目录**（不是本 skill 仓库）迁移完成后执行：

```bash
python /path/to/slim-docs/scripts/measure_entry.py --root . --tier low|medium|high
python /path/to/slim-docs/scripts/check_agent_docs.py --root . --tier low|medium|high
```

两者都必须 exit `0`，才可宣称迁移完成。

| 脚本 | 检查内容 |
|------|----------|
| `measure_entry.py` | `CLAUDE.md` / `AGENTS.md` 行数是否超档 |
| `check_agent_docs.py` | index 表、链接、孤儿文、专题数是否在区间内 |

仅需 Python 3 标准库，无需 pip 安装。

## 包结构

```text
slim-docs/                 # 本仓库根目录 = skill 包
├── SKILL.md               # 给 agent 的运行时说明
├── README.md              # 给人（英文）
├── README.zh-CN.md        # 给人（中文）
├── LICENSE
├── references/            # 模板（skill 按需读取）
└── scripts/               # 校验 CLI
```

## 安全

- 安装前请审阅 `scripts/`（会在本机执行）。  
- 脚本设计为**读取**项目文件以统计行数/检查结构，不应改写你的项目内容。  
- 优先从本 GitHub 仓库或你信任的 tag 安装。  
- 第三方 fork 存在供应链风险，请当作代码审查。

## 兼容性

- **Claude Code：** `CLAUDE.md`  
- **Codex / AGENTS 类工具：** `AGENTS.md`  
- 共用同一 `agent-docs/`，专题正文不要复制两份  

格式说明：[agentskills.io](https://agentskills.io) · 官方示例：[anthropics/skills](https://github.com/anthropics/skills)

## 许可证

[MIT](LICENSE) © 2026 ninelie710
