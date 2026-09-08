**简体中文** | [English](README.en.md)

![Flatland Research Loop：从目标差距到实测质量](assets/cover.svg)

# Flatland Research Loop

**面向实测质量提升的 Flatland 自动优化**

让 agent 从你的目标和现成求解器出发，找出主要损失，用算法思想改变规划、搜索或执行决策，再运行候选求解器，检验质量是否真正提高。核心循环是：**目标差距 → 算法机制 → 实现 → 正确性检查 → 质量比较 → 验证与继续。**

这是一个不同 agent 都可读取的 Markdown skill，配有标准库 Python 工具、中英两版材料，以及从真实研究中提炼的成功经验与失败案例。默认自动优化；学习问答是可选模式。它不提供原作者的满分代码、精确参数或可复刻的最终组合。

## 你会得到什么

- **明确的目标与差距**：实际主指标、硬约束、最好已验证版本，以及剩余主要损失。
- **改变决策的算法理由**：当前方法缺少什么能力、改哪个函数、为什么可能改善目标。
- **真实质量反馈**：候选求解器实际参与运行后的目标变化、逐例退步、失败和计算成本。
- **可恢复的最好版本**：区分正确性通过、筛选有效、独立验证和官方确认。
- **失败后的下一步**：更新损失解释、换机制或换目标实例；拒绝一个候选不会自动终止整个优化任务。

适用于合法但低质量的计划、搜索停滞、故障后损失扩大、代理指标变好而官方分数下降等问题。只需提供项目、已有结果、评价规则、目标与资源边界。agent 先读取材料，不反复让你填表。

## 从算法中提炼可迁移的思想

[算法机制指南](references/algorithm-playbook.md) 将研究复盘与公开算法原理连接起来，按当前损失选择，而不是要求安装一套固定架构：

| 当前问题 | 值得检查的思想 |
| --- | --- |
| 空间上很短的路线，时间上却不可行或搜索开销很大 | 有方向的 A*、时空约束和 SIPP：状态要表达真正影响可达性的条件。 |
| 先规划者占据瓶颈，后规划者长期吃亏 | 优先级规划中的顺序分配，以及联合处理相关列车的 LNS 邻域。 |
| 计划不错，故障后执行损失很大 | 依赖关系协调与局部修复：检查承诺、真实状态和影响边界。 |
| 同样时间总在检查同几个候选 | 公平覆盖与可继续的搜索；增量维护减少重复工作，并把节省的计算用于有价值的候选。 |

例如，一个合成瓶颈中，列车 A 的更优路线被 B 的预约挡住；只反复重算 A，可能永远没有改善。联合释放相关决策、重排这个小组，才改变了搜索能够到达的解。另一个合成例中，每次有改善就从队首重新扫描，会让后面的阻塞分量始终没有被处理。**要改变的是搜索能表达什么、实际访问了什么，而不只是“多跑一点”。**

这些是机制解释，合成例不代表比赛结果。真实案例保留失败和条件性收益；源代码存在某个机制，也不能单独证明它造成了成绩提升。

## 默认流程：正确性与质量分别验证

1. **建立目标并解释差距。** 对齐评价规则、运行约束和最好版本，查看主要损失及未解释部分。服务器退步先记为原因待查，不凭一次退步断言过拟合。
2. **选择一个有依据的机制。** 将算法思想落实到当前项目代码，提出预期质量变化及可能代价，避免只围着参数微调。
3. **短冒烟淘汰坏实现。** 检查受影响的接口、冲突或恢复行为。优化任务通过后继续质量评估；只修一个明确错误时可按该范围结束。
4. **代表性实例筛选。** 用原生入口真实运行候选求解器，兼顾目标损失和可能退步的场景。复用条件一致的基线，不只看有利案例。
5. **验证有希望的候选。** 使用未参与方案选择的相关实例或预先保留的独立运行条件；重复筛选案例只检查稳定性。官方分数目标需要对应官方证据。更新最好版本，再处理剩余差距。

不默认参数矩阵、多种子扫描、全组合消融或每轮完整 A/B；质量比较是优化主流程。固定动作回放不证明新规划策略有效。完整评测用于有希望的版本、具体回归风险或达标确认。详见 [自动研究流程](references/autonomous-research.md) 和 [质量评估](references/quality-evaluation.md)。

目标尚未达到时，单个方向失败不是任务终点。明确资源用尽或必要外部条件缺失时，保存状态、说明未达目标与下一步所需条件。若认为当前可行机制已研究排除，须列明已试证据、剩余替代方向及各自缺少的条件，才能据此暂停；不空泛宣布“没有值得的下一步”，也不无限消耗预算。宿主提供执行能力与授权，skill 本身不是后台服务。

## 质量与轨迹工具

| 工具 | 实际用途 | 边界 |
| --- | --- | --- |
| [quality_compare.py](scripts/quality_compare.py) | 对齐原生评测导出的版本、实例、环境、资源和目标，报告质量变化与主要退步。 | 不运行 solver、不自造分数；缺失或不可比数据不能证明提升，也不自动晋级。 |
| `rail_trace.py diagnose` | 定位计划与实际首处分歧、显式等待及声明语义下的冲突。 | 是诊断线索，不直接证明根因或性能损失。 |
| `rail_trace.py slice` | 提取相关时间窗口。 | 日志切片，不是仿真或完整 checkpoint。 |
| `rail_trace.py replay` | 通过项目 adapter 真实执行给定检查点与动作。 | 需要项目适配；固定动作回放不能替代候选规划器评测。 |
| `rail_trace.py reservations` | 核对预约事件、释放、回滚与提供的快照。 | 只覆盖给定事件模型与观察。 |

从仓库根目录体验公开合成数据：

```text
python scripts/quality_compare.py examples/synthetic_quality_baseline.json examples/synthetic_quality_candidate.json
python scripts/rail_trace.py diagnose examples/synthetic_trace.json
python scripts/rail_trace.py replay examples/synthetic_replay.json --adapter scripts/synthetic_rail_runner.py
```

第一条比较预先制作的合成评测数据，没有运行 Flatland；第三条实际执行合成微型 runner。它们只演示工具，不代表原比赛或真实性能。实际项目使用自己的评测器、状态语义和适配器。格式与用法见 [质量评估](references/quality-evaluation.md) 和 [轨迹工具说明](references/tooling.md)。

## 从症状进入真实案例

[六个脱敏实验案例](references/reasoning-cases.md) 保留真实记录中的观察与判断边界。先根据当前证据选择相关案例，再决定是否需要改动。

| 当前症状 | 案例入口与保留的观察 |
| --- | --- |
| 搜索在探索，但最终返回结果没有改善 | **C1 · 接受规则**：等成本横移持平且更慢；历史成本接受产生了探索，但返回的最好解仍较弱，未集成。先核对当前解与最好解。 |
| 新方法在弱起点有效，接入成熟系统后收益很小 | **C2 · 基线依赖**：联合冲突搜索在弱起点上多数改善，成熟基线边际收益很小。检查是否补充了当前系统缺少的能力。 |
| 预约表维护耗时较多 | **C3 · 增量维护**：固定工作量下多项状态一致、耗时下降；伴随效率改动使归因受限，整局收益尚不能由此推定。 |
| 完成数、按时数或总代价改善，最终分数反而下降 | **C4 · 评价关系**：两份实际评测表出现这种分歧，调查转向逐例结果；不能据此推定评分公式。 |
| 故障后计划变好，实际执行却更差 | **C5 · 重排与执行**：扩大重排范围后经历收紧、重测与回滚；当时的测试调用和测量摘要报告惩罚与耗时增加，此处依据不是原始运行输出，且存在伴随改动。 |
| 扩大候选范围有小幅收益，却更费时 | **C6 · 覆盖与预算**：保存计划和完整执行有限改善，完成数与按时数不降；覆盖与额外计算的作用未被因果分离。 |

这些入口用于提出和缩小当前项目中的解释。原始实验材料没有公开供独立复核，案例本身不能证明当前项目会获得相同收益，也不构成公开性能比较或最优性证据。

## 安装与使用

核心内容是 Markdown。能读取文件的 agent 可以直接读取仓库；只能对话的工具可以接收上传或粘贴的 skill 及相关参考文件。自动发现、持久加载和命令执行由各自宿主决定。

下载仓库到普通目录：

```bash
git clone https://github.com/kidheart/flatland-research-loop.git
```

向 agent 提供实际目录，然后发送下面的提示词。无需使用平台专属调用语法。

```text
请读取 <skill目录>/SKILL.md，将它作为本次工作的指南，按需读取链接的参考材料。
我的项目：<实际路径>
当前问题或目标：<症状、要改善的指标>
已有材料：<代码、评价规则、轨迹或结果的位置>
允许修改的范围与时间预算：<范围、预算>

先明确实际主指标、目标、硬约束与最好版本，解释主要质量差距。
结合算法机制与真实案例选择改动；冒烟后运行候选求解器做代表性质量比较，
对有希望的候选继续验证。复用匹配的基线，不默认参数矩阵或每轮完整 A/B。
一个方向失败就更新解释并选择下一项，不能把冒烟通过当成优化完成。
在授权与资源边界内自动推进，报告实际质量变化、退步、最好版本及剩余目标。
请用中文回应；只有我明确要求学习或问答时才切换到交互教练。
```

英文入口为 [SKILL.en.md](SKILL.en.md)，对应参考材料在 `references/en/`。只提供文件名或链接不意味着 agent 能读取内容；无法读取时，需要把相应内容提供给它。

<details>
<summary>可选：安装为 Codex 原生 skill</summary>

仓库根目录就是 skill 根目录，安装目录名称为 `flatland-research-loop`。在 Codex 中输入：

```text
使用 $skill-installer，从 https://github.com/kidheart/flatland-research-loop
安装仓库根目录的 skill，名称为 flatland-research-loop。
如果同名安装目录已经存在，请先说明情况，不要覆盖。
```

也可以使用 PowerShell 克隆到用户级 skill 目录；以下命令会在目标已存在时停止：

```powershell
$skillPath = Join-Path $HOME '.agents/skills/flatland-research-loop'

if (Test-Path -LiteralPath $skillPath) {
    throw '目标目录已存在。请检查现有安装，不要直接覆盖。'
}

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $skillPath) | Out-Null
git clone https://github.com/kidheart/flatland-research-loop.git "$skillPath"

if ($LASTEXITCODE -ne 0) {
    throw '克隆未完成。请检查 Git 输出和目标目录后再处理。'
}
```

安装后在新会话中使用 `$flatland-research-loop`；如果尚未发现它，重启 Codex。目录与安装方式见 [OpenAI 的 skill 文档](https://learn.chatgpt.com/docs/build-skills)。[agents/openai.yaml](agents/openai.yaml) 仅提供可选的 Codex 展示信息。

</details>

## 可选：交互教练

明确要求学习或问答时，agent 围绕当前最关键的不确定性，每次问一至两个问题，帮助你区分观察与解释、提出可被推翻的假设，再共同设计小检查。没有实际项目材料时，可以使用明确标注的虚构小例。

```text
请按已加载的指南，以交互教练模式带我分析这段轨迹。
先帮我找到计划与执行的第一次分歧，再让我判断可能原因。
我卡住时逐步给提示，最后一起设计一个能区分解释的小检查。
```

## 内容导航

| 文件 | 用途 |
| --- | --- |
| [中文 skill](SKILL.md) · [English skill](SKILL.en.md) | 轻量入口与按需阅读路线。 |
| [算法机制](references/algorithm-playbook.md) · [English](references/en/algorithm-playbook.md) | 从损失选择能改变搜索或执行决策的思想。 |
| [质量评估](references/quality-evaluation.md) · [English](references/en/quality-evaluation.md) | 代表性筛选、验证与质量比较器格式。 |
| [诊断指南](references/diagnosis.md) · [English](references/en/diagnosis.md) | 从系统、评价和轨迹定位问题，选择修改位置。 |
| [工具说明](references/tooling.md) · [English](references/en/tooling.md) | 轨迹格式、工具用法与 replay 接入边界。 |
| [轨迹工具](scripts/rail_trace.py) · [合成示例](examples/) | 本地证据检查工具与演示数据。 |
| [自动研究指南](references/autonomous-research.md) · [English](references/en/autonomous-research.md) | 有界推进、实际检查与版本保留。 |
| [脱敏实验案例](references/reasoning-cases.md) · [English](references/en/reasoning-cases.md) | 六个案例的条件、观察与有限结论。 |
| [提问与提示库](references/question-bank.md) · [English](references/en/question-bank.md) | 交互教练的按需提问。 |
| [实验记录卡](references/experiment-card.md) · [English](references/en/experiment-card.md) | 需要进一步实验时记录假设、结果与决定。 |

## 隐私与证据边界

agent 使用当前使用者提供或授权访问的项目材料与公开资料。仓库不包含来源项目的源码、精确配置、参数、逐例成绩或可重建其方案的实现细节，也不要求从历史对话或私有工程中找回来源方案。

环境版本、转移规则、速度、故障可见性、目标处理和评价方式可能不同。诊断与修改须依据当前环境；局部检查、本地执行和完整评测支持不同范围的结论。本项目不承诺特定分数或最优性，案例判断应随更强的证据修正。

## 贡献

欢迎通过 [Issue](https://github.com/kidheart/flatland-research-loop/issues) 或 [Pull Request](https://github.com/kidheart/flatland-research-loop/pulls) 改进诊断方法、工具、合成案例和翻译。新案例应说明观察、解释、区分它们的检查与结论边界。

仅提交有权公开且充分脱敏的材料。检查多个案例组合后是否暴露来源方案；请勿提交私有代码、参数、配置、成绩、日志或提交标识。贡献按本仓库相同许可发布。

## 许可

© kidheart。本仓库采用 [Creative Commons Attribution–NonCommercial 4.0 International（CC BY-NC 4.0）](LICENSE)。你可以按许可进行非商业性的分享与改编，但须适当署名、提供许可链接、标明改动，并遵守其他许可条件。商业使用须另行取得许可。

可参考的署名：

> 基于 kidheart 的 [Flatland Research Loop](https://github.com/kidheart/flatland-research-loop)，采用 [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)；如有改动，请在此说明。
