# 测试与迭代

## 铁律

**没有失败基线，就不知道 skill 是否教对了东西。**  
（写 skill ≈ 对流程文档做 TDD：RED → GREEN → REFACTOR）

## 测什么：三条轴

| 轴 | 问题 | 方法 |
|----|------|------|
| **Trigger** | 该出时出、不该出时不出 | 正/负 prompt 集；只暴露 description 的盲测 |
| **Function** | 激活后步骤是否被遵守、产物是否对 | 同 prompt：有 skill vs 无 skill（或旧版） |
| **Performance** | 是否更少胡写/更少无效工具轮次 | 对比轮次、是否读对 reference、是否跑验证命令 |

官方 `skill-creator` 流程摘要：草稿 → 真实 test prompts → 有/无 skill 对照跑 → 定性+定量 → 改写 → 扩大集。

## RED-GREEN-REFACTOR（流程/纪律类）

1. **RED**：不挂 skill，压力场景（时间紧、已沉没成本、权威施压）下记录违规与借口原文  
2. **GREEN**：最小正文，只堵已出现的洞；复跑应遵从  
3. **REFACTOR**：新借口 → 借口表 / Red flags / 更硬门禁；再验  

详见本地 superpowers：`writing-skills`、`testing-skills-with-subagents`。

## 技巧/参考类

- 新场景能否套用  
- 边界：缺文件、错误格式、部分失败  
- 检索：能否根据 index 打开正确 reference  

## 最小 eval 集

每个 skill 至少：

- 2–3 条**真实用户口吻**正例  
- 2–3 条**易混淆**负例（trigger 测试）  
- 1 条「高压/抄近路」场景（纪律类必备）  

可选用 JSON（skill-creator 风格）保存 prompt 与期望描述；断言可后补。

## 发布前

- [ ] description 盲测通过  
- [ ] 正文流程在真实任务中被执行（不只「模型说会用」）  
- [ ] reference 一层深、路径可解析  
- [ ] 脚本 `--help` 可用，失败信息可读  
- [ ] 无密钥、无意外破坏性默认命令  
- [ ] 改动旧 skill 时有对照旧版的回归  

## 迭代信号

| 现象 | 动作 |
|------|------|
| 从不触发 | 加触发词/症状/负向边界收窄误竞争 |
| 乱触发 | 加 Do NOT use；收窄能力句 |
| 触发了但乱做 | 步骤编号化、硬门禁、输出模板 |
| 上下文爆炸 | 拆 reference；脚本黑盒化 |
| 回归 | 保留 eval 集，禁止只改文风不跑对照 |
