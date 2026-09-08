# 用真实质量结果决定去留

**简体中文** | [English](en/quality-evaluation.md)

冒烟能回答“改动是否跑通、局部错误是否消失”，不能回答“整体规划是否变好”。例如额外预约缓冲可能通过所有冲突检查，却让更多列车等待；固定原版动作的回放即使完全正常，也没有测到新版规划器的选择。**质量提升必须来自候选算法实际参与决策的运行，以及当前 evaluator 的真实目标结果。**

## 三种检查各自回答一个问题

1. **冒烟：实现是否可信？** 检查受影响的约束、状态转换或重规划路径。通过后继续质量检查，不以此结束优化或宣布成功。
2. **代表性质量筛选：目标是否改善，代价在哪里？** 从已定位的主要损失选择实例，同时放入可能受该改动伤害的实例。例如针对拥堵增加保守等待，也要观察稀疏交通的延迟。运行候选自己的决策过程，记录目标、失败/超时、硬约束和耗时。规模由本次机制的影响范围决定，不固定要求庞大套件或只跑一个方便实例。
3. **独立确认：选出的方向能否离开调试实例仍成立？** 候选选定后，用尚未用于选择候选的保留实例或新实例确认；对目标涉及完整 episode 的任务，应真的运行相应 episode。官方目标的达成必须以相应官方结果为依据。若只拿到了局部筛选结果，应继续确认或交代真实缺口，不把缺少证据改写成“已无值得尝试的方向”。

这三层无需每轮重跑全部内容。版本、输入、evaluator、环境和预算绑定一致的现有 baseline 可以复用。局部修复通过后，先做能区分得失的质量筛选；有希望的候选再使用独立确认资源。对随机波动影响判断的结果，只追加能解决这个不确定性的重复或实例，避免盲目扫描。分开保留“实现通过”“筛选有收益”“独立确认有收益”“官方已验证”的状态。

比较同一目标的原生数值，不把平均完成率、速度、局部等待次数等代理随意替换成官方分数。先核对官方公式的分母、惩罚、权重和聚合方式；直接报告真实失败，不能删掉失败实例后求平均。保留受损场景，即使总量上升也要解释取舍。服务端变差时先核对版本、口径、输入分布和具体失败；“过拟合”只是可能解释，不能由一张下降截图证明。

## 一个可运行的结果比较器

从仓库根目录运行：

```text
python scripts/quality_compare.py examples/synthetic_quality_baseline.json examples/synthetic_quality_candidate.json
python scripts/quality_compare.py path/to/baseline.json path/to/candidate.json --limit 8 --output quality-report.json
```

[比较器](../scripts/quality_compare.py)只读取当前项目原生 evaluator 导出的归一化结果，不运行求解器、不制造官方分数、不自动替换最好版本。随包的两份 `synthetic_quality_*.json` 使用虚构数值和声明，展示总量改善同时一个场景退步；它们不是执行过的 Flatland 实验。`synthetic: true` 会保留在报告中。

如果 evaluator 只给整体报告，或原生公式无法表示为逐实例标量的 `sum` / `mean`，保留原报告并按其公式比较；不要伪造实例、把整体值复制给每个实例、先平均再平均，或为了适配工具改变目标。此时可以不使用比较器。将不支持的真实公式名称写入 `aggregation` 时，工具返回 `inconclusive` 和空 aggregate。

## 输入：`rail-quality/v1`

两份文件使用同一结构，完整范例见[基线](../examples/synthetic_quality_baseline.json)和[候选](../examples/synthetic_quality_candidate.json)。

| 字段 | 内容与约束 |
| --- | --- |
| `schema` | 固定 `rail-quality/v1`。 |
| `synthetic` | 必填布尔值。真实项目结果使用 `false`；随包虚构示例使用 `true`。 |
| `solver_version` | 实際被运行的代码版本、提交或内容哈希；未提交改动不能仅标记旧 HEAD。两边相同会提示无法据此建立代码改进。 |
| `role` | `screen` 或 `validation`，说明本次结果用途。 |
| `evidence.kind` / `evidence.reference` | `server`、`local` 或 `proxy`；以及可定位的原生运行日志/结果标识。不同证据种类不混算。 |
| `comparison.suite` | 预先选定的实例集合/选择清单标识；不能看到结果后删掉坏实例。 |
| `comparison.evaluator` | 真实 evaluator、规则和计分版本/哈希。 |
| `comparison.environment` | 绑定运行器、依赖、硬件/线程等会影响比较的条件。 |
| `comparison.budget` | 两边同一资源限制，包括规划时间、调用数、线程等本任务实际约束。 |
| `objective` | `name` 原生目标名称；`direction` 为 `min` 或 `max`；`aggregation` 为原生 `sum` / `mean`，其他公式不能被该工具计算。 |
| `execution` | `kind` 为 `episode`、`planning` 或 `fixed_action_replay`；`solver_invoked` 为布尔值，记录候选是否实际参与了决策。 |
| `expected_cases` | 非空数组，每项包含唯一 `id`、`scenario` 描述、`input_fingerprint`。指纹应覆盖地图、起终点、故障/随机输入、初始状态等影响该运行的输入。 |
| `records` | 每个实际运行一条，包含 `id`、实际 `input_fingerprint`、`status`、`objective`、`constraints_passed`、`runtime_seconds`。没有结果就保留缺失，不伪造成功。 |
| `validation` | 验证用途附 `selection: held_back` / `fresh` / `reused_for_tuning` / `unknown` 和可定位选择过程的 `reference`。只有前两种允许 `validation_gain`；两边应引用相同选择范围。 |

`status` 为 `ok`、`failed` 或 `timeout`，表示本次求解/仿真运行是否正常完成、运行失败或达到执行时限。正常完成 episode 后仍有列车未到达，应由 evaluator 的目标/指标反映，不自动等同于运行 `failed`。`objective` 是有限数值或 `null`，不得把未知当成零；`constraints_passed` 为 `true`、`false` 或 `null`（未知）。`runtime_seconds` 为有限非负数。布尔值不当作数字。重复 case、重复 JSON 键、不合法数据会被拒绝。

失败/超时若有 evaluator **实际给出的**惩罚分，可把该分填入 `objective`，并添加 `penalty_source` 指向原生规则或运行记录。工具保留失败状态，绝不靠删除失败来提高均值。缺少惩罚分时 aggregate 保持未知；候选自身有罚分也不等于质量通过，候选约束未知同样阻止正向结论。若基线失败已有真实原生罚分，而候选运行正常且约束通过，可以承认修复带来的数值收益；基线的失败和约束疑点仍完整保留在报告中。

`fixed_action_replay` 或 `solver_invoked: false` 一律不产生规划质量提升数值。`planning` 的结论只属于声明的规划目标，不自动代表端到端 episode 或官方最终分数。上述来源、版本和选择信息由导出者负责如实绑定；工具检查字段一致性，无法认证用户声明或验证外部文件内容。

## 输出如何使用

输出为紧凑的 `rail-quality-report/v1` JSON。`--limit`（默认 8，正整数）只限制每个结果列表的显示数量，不截断计算；列表均有 `items`、`total_count`、`truncated`。

- `scope` 明确证据类别、用途、运行种类及比较绑定；`comparability_blockers` 给出不能计算提升的原因。环境、预算、目标、集合、指纹或覆盖不匹配，固定动作回放、未调用求解器、缺失分数、不支持聚合都会令 `aggregate: null`。先补正确证据，不把 `null` 当作平手。
- 两边摘要分别保留实际数量、缺失/多余实例、指纹错误、成功/失败/超时数量、硬约束状态、未评分数量和实际总耗时。耗时是诊断数据，不会偷偷替代目标。
- 同口径且完整时，`aggregate` 给出原生 sum/mean 和 `signed_improvement`；**正数始终表示候选更好**。`case_changes.regressions` 按损失从大到小列出退步实例；不能只读总量。
- `screen_gain` 仅表示本次筛选的目标数值改善且没有 `gain_blockers`；`validation_gain` 还要求双方独立选择声明成立且不是 proxy。它们都不证明统计显著、隐藏集泛化或官方目标达成。有真实退步实例仍可能出现总量 gain，必须结合场景权衡决定是否保留。
- `regression` 表示同口径 aggregate 变差；`tie` 表示精确数值相等；其余为 `inconclusive`。`quality_concerns` 保留双方的失败、超时和约束疑点；其中候选失败/超时、候选约束失败/未知，以及相同代码版本、不成立或不一致的验证选择、验证使用 proxy，会另外列入 `gain_blockers`，即使 aggregate 改善也不能正向通过。基线的历史失败/约束疑点不会永久阻止承认候选修复收益，但基线缺失分数仍阻止 aggregate，基线验证选择未建立仍阻止 `validation_gain`。
- `decision.automatically_promoted` 和 `decision.official_goal_verified` 始终为 `false`。是否保留候选由 agent 结合目标、约束、退步场景和原生结果作出；官方达成应另引用对应官方证据。

报告有发现或不确定性仍退出 0，表示完成比较；参数、读取、schema、写入错误退出 2，stderr 给出 JSON `error`。指定的不同输出文件可被覆盖，但输入本身、符号链接解析后的相同路径或硬链接别名不能被输出覆盖。

`python scripts/smoke_quality_compare.py` 只检验这个比较器的计算与拒绝行为。它没有运行 Flatland，更不替代使用者项目的质量筛选和独立确认。
