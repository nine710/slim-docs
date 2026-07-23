# 优秀 SKILL.md 正文写法

## 总原则

1. **写给 agent 的规程**，不是给人的博客：短句、祈使语气、可执行。  
2. **默认模型很强**：只写它不知道的项目/流程/坑；删正确但无增量的段落。  
3. **解释 why 优于堆 MUST**（官方 skill-creator）：说明「为何重要」比空洞强调更抗合理化。  
4. **一种术语一条线**：同一概念固定用词（如始终说 template 不混 view/html）。

## 高价值章节（按需组合）

| 章节 | 作用 |
|------|------|
| Overview / 核心原则 | 1–2 句北极星 |
| When to use / When not | 边界（可与 description 互补，更细） |
| HARD-GATE / Iron Law | 未满足不得进入下一阶段（brainstorming、TDD、verification） |
| 有序步骤 / Checklist | 可勾选；复杂流程让 agent 抄到回复里逐项打勾 |
| Decision tree | 分支任务（webapp-testing） |
| 输出模板 | 固定交付结构，便于组合 skill |
| Gotchas / Common mistakes | 真踩坑 + 正确做法（docx 几乎整篇是 footguns） |
| Red flags / 借口表 | 纪律类 skill：压力下的自我否决 |
| 何时读 reference | 显式路径 + 条件 |
| Acceptance | 完成定义 / 证据要求 |

## 推荐模式

### 顺序工作流

编号步骤 → 每步期望 I/O → 失败回滚或停止条件。

### 反馈环

生成 → 用脚本/命令验证 → 根据错误修 → 再验（文档编辑、表单填充类）。

### 模板模式

`assets/` 放骨架；正文写「复制并填空」，少用散文描述格式。

### 示例模式

**一个**精品端到端示例 > 五门语言的半成品。选与领域最相关的语言即可。

### 决策树

静态 vs 动态、服务是否已启动等；每个叶节点落到具体命令/脚本。

## 引用与分包

- 从 SKILL.md **直接**链到 `references/foo.md`  
- 分域内容按文件拆，不按「再深一层目录迷宫」拆  
- 长 reference 顶部 Contents  

## 脚本协作文案

```markdown
**Helper scripts**
- `scripts/with_server.py` — 管理服务生命周期

Always run with `--help` first. Do NOT read the full script source unless
customization is required; scripts exist to be executed as black boxes.
```

## 风格清单

| 做 | 不做 |
|----|------|
| 祈使：Extract…、Run…、Read… | 第一人称叙事、一次排障故事 |
| 明确停止条件 | 「尽量」「适当」无标准 |
| 与 hooks/测试衔接的完成证据 | 「觉得好了就算完成」 |
| 与其他 skill 按 **name** 交叉引用 | `@` 强制预加载大文件烧上下文 |

## 体量目标（经验值）

| 类型 | SKILL.md |
|------|----------|
| 常加载纪律/流程 | 尽量短；关键门禁醒目 |
| 一般技巧 | 常 &lt;500 行；超了就拆 reference |
| 纯参考（API） | 正文做路由 + 强 TRIGGER；细节分语言/主题文件 |

## 自由度再强调

- 可变策略 → 启发式  
- 必须字节级一致 → 脚本或逐字模板  
- 中间态 → 伪代码 + 可调参数
