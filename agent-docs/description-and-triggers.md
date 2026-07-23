# description 与触发设计

## 地位

`description` 是 **路由逻辑**，不是营销文案。  
在加载完整 `SKILL.md` 之前，agent **几乎只靠它**决定是否激活该 skill。

## 写法公式

```text
[做什么 / 关键能力] + [何时用：触发词、症状、场景] + [可选：Do NOT use for …]
```

要求：

- **第三人称**（注入系统提示；I/you 会干扰发现）
- **具体可检索**：文件类型、错误症状、产品名、用户原话同义词
- **负向触发**：减少误激活（「不要用于 Vue」「不要用于写新功能」）
- 长度：规范上 ≤1024；尽量紧

## 好 / 坏对照

| 类型 | 示例 |
|------|------|
| 坏 | `Helps with documents` |
| 坏 | `React skills` |
| 好 | `Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.` |
| 好 | `Creates and builds React components using Tailwind CSS. Use when updating component styles or UI logic. Do NOT use for Vue, Svelte, or vanilla CSS-only projects.` |
| 好（纪律类） | `Use when implementing any feature or bugfix, before writing implementation code`（触发时机写清，不把 RED-GREEN 流程写进 description） |

## 关键陷阱：description 泄流程

若 description 写成「先 code review 再…」，模型可能**只执行 description 摘要**而跳过正文完整流程。

- description：**只写何时用**  
- 正文：写完整步骤 / 门禁 / 检查表  

（superpowers `writing-skills` 与实测结论一致。）

## 强触发写法（参考 claude-api skill）

大参考类 skill 可用：

- **TRIGGER** — 命中条件枚举（含别名、包名）
- **SKIP** — 明确否决条件（其他供应商、已 grep 到 openai 等）

适合「极易误答、必须先读文档」的领域；一般流程 skill 不必同样冗长。

## 发现性自检（无代码）

新开对话，只贴 frontmatter，问模型：

1. 给出 3 条**应触发**的真实用户原话  
2. 给出 3 条**相似但不应触发**的原话  
3. 批评 description 是否过宽/过窄并改写  

再在真实会话里看是否调用了 Skill 工具 / 是否读了 SKILL.md。

## 与入口文件（CLAUDE.md / AGENTS.md）的区别

| | Skill description | 仓库入口文件 |
|--|-------------------|--------------|
| 生命周期 | 多 skill 竞争路由 | 常驻项目级 |
| 目标 | 「要不要加载这个包」 | 「本仓库怎么工作」 |
| 膨胀后果 | 误触发/不触发 | **每会话税** + 指令稀释 |

因此：**流程可复用 → skill**；**仓库事实与硬命令 → 薄入口 + agent-docs**。
