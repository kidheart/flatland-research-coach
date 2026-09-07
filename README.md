**简体中文** | [English](README.en.md)

![Flatland Research Loop：从观察到可检验的判断](assets/cover.svg)

# Flatland Research Loop

**以诊断为中心的 Flatland 自动研究**

从你的现成系统出发，读懂代码与评价规则，从轨迹中定位损失或计划与执行的首处分歧，再选择有依据的修改位置，用短冒烟检查确认改动。真实实验提炼的脱敏案例帮助 agent 判断：**当前症状满足什么条件，应该检查哪里，什么改动值得尝试。**

这是一个不依赖特定 agent 的 Markdown skill，配有 Python 标准库轨迹工具和合成小例。默认自动开展诊断与修改；希望学习、练习判断或问答时，可以切换到交互教练。中英文是同一份指南的两种语言，无需安装两套。仓库与 skill 标识均为 `flatland-research-loop`。

## 你会得到什么

- **问题在哪里**：具体列车、时间、位置或代码路径，以及相关的可观察损失。
- **判断的依据**：轨迹窗口、指标或代码证据；分清首次偏离和后续连锁影响。
- **改哪里、为什么**：结合当前系统已有能力与相关案例的适用条件，选择修改位置。
- **最小检查结果**：对受影响路径实际做了什么检查，是否通过，是否超时。
- **尚未证实的部分**：例如局部修复是否改善整局评价，或候选解释是否仍有其他原因。

适合计划成本下降但最终分数变差、故障后重排反而更慢、列车停住或晚到、局部方法加入完整系统后收益消失等问题。提供项目路径、现有结果、评价规则和时间预算即可开始；agent 先读取已有材料，关键缺失才询问。

## 默认流程

**读懂系统与评价 → 找到损失与首处分歧 → 按条件选修改位置 → 有针对性修改 → 短冒烟确认**

1. **读懂当前系统。** 确认输入输出、计划与动作的关系、执行状态、评价方式，以及已有模块实际解决了什么。优先复用可信的现有结果。
2. **把症状落到证据上。** 从影响目标的损失入手，查看相关列车和时间窗口，追到最早可观察的分歧。区分路径质量、动作转换、状态同步、预约占用和计分关系等可能位置。
3. **用案例缩小修改范围。** 对照案例的前提与证据边界，判断当前系统是否真的缺少相应能力，形成一个可检查的解释。
4. **修改并检查受影响路径。** 保留当前最好已验证版本及可恢复检查点，实施有针对性的改动，运行足以检验当前解释的短冒烟；根据结果保留、修正或回滚。
5. **简要交付。** 说明发现、依据、修改、实际检查和未证实事项。只有更大检查会改变下一步决定时才扩展，达到目标或预算上限后停止。

预算是上限，不是消耗目标。常规小改动由当前 agent 完成；A/B、多 agent 协作和长评测按具体需要使用。冒烟通过只能支持检查范围内的结论；性能提升仍需要相关且可比的实际测量。

在已授权的本地范围内，agent 连续推进这些步骤，无需每轮重复批准。文件、命令和执行能力由宿主提供；这个 skill 本身不是后台运行服务。详细方法见 [诊断指南](references/diagnosis.md) 与 [自动研究指南](references/autonomous-research.md)。

## 轨迹工具

[scripts/rail_trace.py](scripts/rail_trace.py) 使用 Python 标准库处理约定格式的轨迹。它帮助把一次失败缩到可检查的证据窗口。数据格式、运行要求、adapter 接口和用法见 [工具说明](references/tooling.md)。

| 工具 | 用途 | 结果的边界 |
| --- | --- | --- |
| `diagnose` | 汇总可观察的轨迹问题，定位记录中计划与实际状态的首次可比差异。 | 提供定位线索；根因还需结合当前代码、状态与评价规则确认。 |
| `slice` | 提取指定时间窗口，保留邻近记录与列车元数据，减少阅读量。 | 是日志切片，不会推进环境，也不构成仿真。 |
| `replay` | 通过当前项目的 adapter 从 checkpoint 恢复并实际推进，受真实超时约束。 | 需要使用者提供适配当前环境的 adapter 与 checkpoint；只有实际执行才有运行结果。 |
| `reservations` | 审计预约事件中的引用计数、重叠、释放、回滚与观测快照。 | 仅检查给定事件与快照；不能单凭它证明增量实现等价于完整重建或计划可行。 |

在仓库根目录体验两个合成示例：

```text
python scripts/rail_trace.py diagnose examples/synthetic_trace.json
python scripts/rail_trace.py replay examples/synthetic_replay.json --adapter scripts/synthetic_rail_runner.py
```

[合成微型 runner](scripts/synthetic_rail_runner.py) 与 [examples/ 中的 fixtures](examples/) 用于演示工具行为；第二条命令实际执行该 runner，默认超时为 10 秒。它们不是 Flatland 环境，不对应原比赛实验，也不代表真实项目的性能。工具不声称自动兼容所有 Flatland 版本；接入项目时需要核对状态、动作、时间步和 checkpoint 的含义。

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

先读懂当前系统与评价，从已有证据定位损失或首处分歧。
按相关案例的适用条件选择修改位置，有针对性修改并做短冒烟。
在授权范围内自动推进，简要交付问题、依据、修改原因、实际检查和未证实事项。
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
