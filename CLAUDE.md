# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 仓库定位

本仓库用于**开发、迭代与验证 Claude Code Skills**（流程/技巧/参考文档），不是常规应用业务代码仓库。

技能可以写在本仓库 `skills/` 内，也可以安装/同步到本机个人技能目录。优先以用户指定路径为准。

## 本地项目文档库（按需加载）

详细参考在 **`agent-docs/`**，**不要**把专题全文粘进本文件。

| 何时 | 先读 |
|------|------|
| 任何写/改 skill、评价 skill 质量 | [agent-docs/index.md](agent-docs/index.md) → 只打开相关 1–2 篇 |
| 合规目录 / 渐进披露 / description | `skill-anatomy` · `progressive-disclosure` · `description-and-triggers` |
| 正文写法 / 测试 / 检查表 | `writing-patterns` · `testing-and-evals` · `quality-checklist` |
| 本仓库正在设计的「薄入口+文档库」skill | [agent-docs/target-skill-context.md](agent-docs/target-skill-context.md) |

加载纪律：先 index，再专题；禁止整库通读。

## Skill 存放位置

| 范围 | 路径 | 说明 |
|------|------|------|
| 个人（全项目可用） | `~/.claude/skills/<skill-name>/` | Windows 上即 `C:\Users\<user>\.claude\skills\` |
| 项目（仅本仓库） | `.claude/skills/<skill-name>/` | 随仓库共享，适合项目专属流程 |
| 插件缓存（只读参考） | `~/.claude/plugins/cache/.../skills/` | 已安装插件技能；改这里无效，应复制后改 |

**命名空间扁平**：每个 skill 一个目录，目录名 = skill 名（字母、数字、连字符）。

## 目录结构

```
skills/                         # 或 ~/.claude/skills/、.claude/skills/
  skill-name/
    SKILL.md                    # 必填：主说明（含 YAML frontmatter）
    references/                 # 可选：长参考文档（100+ 行）
    assets/                     # 可选：模板、CSS、图片等静态资源
    scripts/                    # 可选：可执行工具脚本
    examples/                   # 可选：完整可运行示例
```

- 原则、短代码模式（<50 行）、检查表：写在 `SKILL.md` 内
- 重型 API/语法参考、可复用工具：拆到独立文件，由 `SKILL.md` 按需链接
- **不要**用 `@path` 强制预加载大文件（会提前烧掉上下文）；用相对链接 + 明确「需要时再读」

## SKILL.md 规范

### Frontmatter（必填）

```yaml
---
name: skill-name-with-hyphens
description: Use when [具体触发条件与症状]
---
```

- `name`：仅字母、数字、连字符；与目录名一致
- `description`：**第三人称**，只写**何时使用**，不要写流程摘要
  - 推荐以 `Use when...` 开头
  - 写触发场景/症状，不写「先做 A 再做 B」
  - 原因：Claude 可能只读 description 就开干，跳过正文流程
- frontmatter 总长建议 ≤1024 字符；description 尽量 <500 字符

```yaml
# 差：摘要了工作流 → 模型可能只跟摘要走
description: Use when executing plans - dispatches subagent per task with code review between tasks

# 好：只有触发条件
description: Use when executing implementation plans with independent tasks in the current session
```

### 推荐正文骨架

```markdown
# Skill 名称

## Overview
1–2 句：是什么 + 核心原则

## When to Use
症状/场景列表；以及何时不要用

## Core Pattern / 步骤
可复制的步骤或 before/after

## Quick Reference
表或短列表，便于扫描

## Implementation
短示例内联；重参考链到文件

## Common Mistakes
常见翻车点 + 修法
```

### 搜索优化（CSO）

- description 与正文覆盖：错误信息、症状词、同义词、真实命令/库名
- 名字用**动名词/动词优先**：`creating-skills`、`condition-based-waiting`，避免空洞名词堆叠
- 简洁：高频 skill 争取 <200 词；一般 skill <500 词。Claude 默认很强——只写它不知道的

### 自由度

- **高**：多种做法都对 → 启发式文字
- **中**：有偏好模式 → 带参数的模板/伪代码
- **低**：脆弱且必须一致 → 固定脚本/逐步命令，少可选参数

## 何时写 Skill / 何时写进 CLAUDE.md

| 写入 Skill | 写入 CLAUDE.md / 项目约定 |
|------------|---------------------------|
| 跨项目可复用的技巧、模式、工具参考 | 仅本仓库的目录约定、命令、架构 |
| 非显而易见、需要反复查阅 | 标准实践、一次性方案 |
| 需要「压力场景」验证纪律的规则 | 可用 lint/脚本强制的机械约束 |

Skill **是**可复用参考；**不是**某次排障故事叙述。

## 开发流程（TDD 式写 Skill）

核心原则：**没有先看到失败基线，就不要写/改 skill。**

```
RED   → 不挂 skill，用子代理跑压力场景，记录真实违规与借口原文
GREEN → 只针对这些违规写最小 SKILL.md，再跑同一场景，确认遵从
REFACTOR → 堵新漏洞（借口表、红旗列表），再验
```

### 创建/修改清单

1. **RED**：设计 ≥1 个（纪律类建议 ≥3 种压力叠加）场景；无 skill 跑通，记下基线
2. **GREEN**：写 frontmatter + 正文；有 skill 复跑；确认行为改变
3. **REFACTOR**：针对新借口加明确禁止项；纪律类技能写「借口 vs 现实」表与 Red Flags
4. **质量**：描述不泄流程；无叙事流水账；流程图仅用于非显然分支；示例一个精品即可
5. **部署**：放到目标 `skills/<name>/`；需要版本管理则 commit；逐个 skill 测完再做下一个

### 测试类型速查

| Skill 类型 | 怎么验 | 成功标准 |
|------------|--------|----------|
| 纪律/规则 | 压力场景（时间/沉没成本/权威/疲劳） | 高压下仍遵从 |
| 技巧 | 新场景能否正确套用 | 能落地执行 |
| 模式 | 识别何时用/不用 | 判断准确 |
| 参考 | 能否检索并正确应用 | 找得到、用得对 |

**改 skill 与新建同等对待**：改了也要再测。借口「太简单不用测」「先写后测」一律否决。

编写时优先调用 **`superpowers:writing-skills`**；需要 TDD 背景时用 **`superpowers:test-driven-development`**。

## 本机已有参考

- 个人 skill 示例：`~/.claude/skills/console-design/`（`SKILL.md` + `references/` + `assets/`）
- 写作与测试方法论：`superpowers` 插件中的 `writing-skills`（含 `anthropic-best-practices.md`、`testing-skills-with-subagents.md`）
- 斜杠命令与 skill 不同：`~/.claude/commands/*.md` 是命令；skill 是可被自动发现的 `SKILL.md` 包

## 在本仓库落地时的建议布局

若在本仓库维护可发布的 skills（而非只写到个人目录），推荐：

```
.
├── CLAUDE.md
├── skills/
│   └── <skill-name>/
│       ├── SKILL.md
│       ├── references/    # 可选
│       ├── assets/        # 可选
│       └── scripts/       # 可选
└── tests/                 # 可选：压力场景说明、基线记录
    └── <skill-name>/
```

个人安装：将 `skills/<name>` 复制或链接到 `~/.claude/skills/<name>`（或项目 `.claude/skills/<name>`）。

## 常用操作

本仓库以文档/脚本为主，无统一 build。按需：

```bash
# 检查 skill 体积（写作技能建议控制词数）
wc -w skills/<name>/SKILL.md

# 校验 frontmatter 与目录名一致后，安装到个人 skills
cp -r skills/<name> ~/.claude/skills/

# Windows Git Bash 示例
cp -r skills/<name> "/c/Users/$USER/.claude/skills/"
```

验证方式：新开 Claude Code 会话，用会触发该 skill 的真实任务提问，确认 skill 被加载且流程被遵守；纪律类 skill 应用「高压场景」而不是友好问答。

## 给后续 Claude 的硬约束

- 新建/修改 skill **必须**走 RED→GREEN→REFACTOR，禁止先写长文档再「有空再测」
- `description` **禁止**概括正文工作流
- 项目专属约定写本文件；可复用能力写 skill
- 不要批量连写多个 skill 却每个都不测

## slim-docs skill (this repo)

Implementation path: `skills/slim-docs/`.
Validate scripts:

```bash
python skills/slim-docs/scripts/measure_entry.py --root <project> --tier low|medium|high
python skills/slim-docs/scripts/check_agent_docs.py --root <project> --tier low|medium|high
python -m unittest discover -s skills/slim-docs/tests -v
```
