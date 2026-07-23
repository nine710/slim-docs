# 渐进披露（Progressive Disclosure）

## 核心机制

Agent Skills 用**三层加载**控制上下文：

| 层 | 内容 | 何时加载 | 成本特征 |
|----|------|----------|----------|
| **L1 Metadata** | `name` + `description` | 启动/技能列表，用于是否激活 | 每个 skill 约几十～上百 token，可常驻很多 skill |
| **L2 Instructions** | `SKILL.md` 正文 | 任务与 description 匹配后 | 建议 **&lt;500 行** |
| **L3 Resources** | `references/`、`assets/`、按需读的 md；`scripts/` 以执行主 | 正文明确指示，或工具调用需要时 | 可很大；脚本宜当黑盒执行 |

开放标准说明见 [agentskills README](https://github.com/agentskills/agentskills)：Discovery → Activation → Execution。

## 为何有效

- **常驻税**：只有 L1 付「目录税」；L2/L3 按任务付。  
- **相关密度**：未激活的 skill 不占满窗口。  
- **同一模式可映射到项目文档**：薄 `CLAUDE.md`/`AGENTS.md`（L1/L2 内核）+ `agent-docs/` 专题（L3）。

## 三种官方推荐组织法

### 1. 高层指南 + 参考链接

`SKILL.md`：Quick start + 「高级见 FORMS.md / REFERENCE.md」。  
示例：`anthropics/skills` 的 `pdf`（`forms.md`、`reference.md`、`scripts/`）。

### 2. 分域组织

```
skill/
├── SKILL.md          # 路由：领域 → 文件
└── references/
    ├── finance.md
    ├── sales.md
    └── product.md
```

只读当前任务域，不加载其他域。

### 3. 条件细节

正文写默认路径；「tracked changes → REDLINING.md」「OOXML → OOXML.md」仅在需要时读。

## 硬规则

1. **SKILL.md 指向 reference 只一层深**  
   - 坏：`SKILL.md` → `advanced.md` → `details.md`  
   - 好：全部从 `SKILL.md` 直接链到目标文件  
   原因：深层引用时模型常用 `head` 预览，读不全。

2. **&gt;100 行的参考文件开头放 Contents（目录）**  
   方便部分读取时仍知道全貌。

3. **&gt;300 行参考务必 TOC；SKILL.md 近 500 行就再拆一层指针**。

4. **路径**：相对路径 + 正斜杠 `/`（避免 Windows 风格路径写进 skill）。

5. **脚本**：先 `--help` 再考虑 Read 源码（`webapp-testing` 模式），防止大脚本污染上下文。

## 自由度匹配（写指令时）

| 自由度 | 适用 | 形态 |
|--------|------|------|
| 高 | 多种合法做法 | 启发式文字 |
| 中 | 有偏好模式 | 带参模板 |
| 低 | 脆弱、必须一致 | 固定脚本 / 逐步命令 |

脆弱步骤 → `scripts/`；判断步骤 → 正文决策树。

## 与「项目文档库」的同构

| Skills 生态 | 本仓库/目标项目 |
|-------------|-----------------|
| L1 description | 入口文件里「何时读 agent-docs」+ index 一行摘要 |
| L2 SKILL.md | 薄 `CLAUDE.md` / `AGENTS.md` + `agent-docs/index.md` |
| L3 references | `agent-docs/*.md` 专题正文 |

**原则相同**：索引常驻要短；正文按任务加载；禁止把 L3 全塞进 L1。
