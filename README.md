**简体中文** | [English](README.en.md)

![Flatland Research Coach：从观察到可检验的判断](assets/cover.svg)

# Flatland Research Coach

**用你自己的证据，形成你自己的研究判断。**

一个面向 **Flatland 与铁路多智能体规划实验**的通用 Markdown skill，可作为不同 AI agent 的教练指南。通过少量、连续的问答，帮助你解释现象、提出可检验的假设、设计对照实验，并说清结论适用于什么条件。材料包含脱敏思考案例、提问与提示库，以及一张按需使用的实验记录卡。

*An agent-agnostic Markdown coaching skill for evidence-led research in Flatland and railway multi-agent planning.*

介绍页、skill 正文及配套材料均提供中英两版。它们是同一份指南的两种语言，无需安装两套。教练按你当前的语言偏好回应，也可以随时要求切换语言。

## 适合什么时候使用

- 有了运行结果，却说不清一次改善究竟来自哪里。
- 计划看起来合理，实际执行却停住、晚到或反复修复。
- 新方法在简单起点上有效，加入完整系统后收益有限。
- 内部指标、完整执行结果与最终评价对不上。
- 想复盘一次研究：哪些判断有证据，哪些仍是假设，下一步是否值得投入。

你可以带来自己的代码、日志、评测规则或一个具体困惑。尚无实验材料时，也可以从明确标注的虚构小例开始。教练会先利用已经提供的信息，再追问最影响下一步的一至两个问题。

## 一轮思考怎样推进

**观察 → 区分解释 → 形成实验 → 解释结果 → 更新判断**

| 环节 | 希望说清的事 |
| --- | --- |
| 观察 | 实际发生了什么？从哪里开始偏离预期？ |
| 区分解释 | 哪些原因都可能产生这个现象？什么观察能区分它们？ |
| 形成实验 | 改变什么、固定什么？不同解释分别预测什么结果？ |
| 解释结果 | 证据支持哪句话？还不能排除什么？付出了什么代价？ |
| 更新判断 | 保留、修改还是放弃当前解释？下一步为何值得做？ |

通常，一轮对话留下一个有依据的判断、一个仍待检验的问题，以及一个你能解释其目的的实验。已有记录就复用，短实验只记几行即可；不必每轮填满表格。

帮助深度可以随需要变化：你卡住时，教练会逐步缩小问题并给出提示；你要求直接讲解、分析自己的代码或执行已授权的实验时，也可以直接开展。

### 一段虚构的问答

> **以下是虚构教学例，不对应真实实验结果，也不提供建议参数。**
>
> **使用者：** 我加了一个步骤，计划成本下降了，所以最终评价应该也会更好。
>
> **教练：** 这个成本是在计划生成后记录的，还是完整执行后记录的？你的评价规则直接使用它吗？
>
> **使用者：** 只是计划生成后。实际执行还有扰动，我还没核对评分规则。
>
> **教练：** 目前的证据支持“计划阶段改善”。你准备怎样检验，这个收益能否保留到执行结束？
>
> **使用者：** 从相同输入开始，对照运行到结束，分别记录计划、执行结果和实际资源消耗，再按已核实的规则比较。
>
> **教练：** 这能帮助区分几个层次。你会用什么结果决定修改原来的判断？

## 在你的 agent 中使用

核心内容是 Markdown，不依赖特定模型、API、插件或求解器。各平台是否自动发现 skill、放在哪个目录、怎样注册指令并不相同；下面的“读取指南”是通用方式，不表示克隆后会自动生效。

### 能读取文件的 agent

将仓库下载到你选定的目录，或执行：

```bash
git clone https://github.com/kidheart/flatland-research-coach.git
```

在该目录启动 agent，或把目录的实际路径提供给它，然后发送：

```text
请读取 flatland-research-coach 目录中的 SKILL.md，
将它作为本次 Flatland 研究的教练指南，按需读取它链接的参考材料。
请用中文回应。先利用我已提供的信息，
围绕最关键的不确定性问一至两个问题，再共同设计实验。
```

英文使用者读取 [SKILL.en.md](SKILL.en.md)，英文参考材料位于 `references/en/`。如果你的平台有原生 skill 或自定义指令功能，可以按它自己的文档注册这份指南；`$flatland-research-coach` 等调用语法并非所有平台通用。

### 只能对话或上传附件的 agent

上传或粘贴 [SKILL.md](SKILL.md) 的完整内容，并说明希望按此指南讨论 Flatland。需要案例、提问库或实验卡时，再提供对应文件。只发送文件名或链接不意味着 agent 能读取内容；无法读取时，应由它说明还缺少哪些材料。

这些说明提供可移植的使用方式，不代表已对每个模型或 agent 产品逐一验证；具体表现还取决于宿主的上下文长度、文件访问和工具能力。

<details>
<summary>可选：在 Codex 中安装为原生 skill</summary>

可以在 Codex 中输入：

```text
使用 $skill-installer，从 https://github.com/kidheart/flatland-research-coach
安装仓库根目录的 skill，名称为 flatland-research-coach。
如果同名安装目录已经存在，请先说明情况，不要覆盖。
```

也可以使用 PowerShell 克隆到 Codex 的用户级 skill 目录。以下命令会在目标目录已存在时停止：

```powershell
$skillPath = Join-Path $HOME '.agents/skills/flatland-research-coach'

if (Test-Path -LiteralPath $skillPath) {
    throw '目标目录已存在。请检查现有安装，不要直接覆盖。'
}

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $skillPath) | Out-Null
git clone https://github.com/kidheart/flatland-research-coach.git "$skillPath"

if ($LASTEXITCODE -ne 0) {
    throw '克隆未完成。请检查 Git 输出和目标目录后再处理。'
}
```

安装后在新会话中使用 `$flatland-research-coach`；如果尚未发现它，重启 Codex。关于 skill 目录和安装方式，参见 [OpenAI 的 skill 文档](https://learn.chatgpt.com/docs/build-skills)。`agents/openai.yaml` 仅为这一可选适配提供展示信息，其他 agent 不需要读取它。

</details>

## 直接开始

加载指南后，选择一个最接近当前困惑的提示词，附上你有权使用的相关材料即可。以下提示词不依赖平台专属调用语法。

**从一个研究问题开始**

```text
请按已加载的 Flatland Research Coach 指南开展讨论。
先阅读我提供的环境说明和实验记录，复述你已经知道的事实。
围绕当前最关键的不确定性，每次问我一至两个问题，
帮助我提出能被推翻的假设，并共同设计下一步实验。
```

**追查计划与执行的分歧**

```text
请按已加载的 Flatland Research Coach 指南开展讨论。
我提供了自己的计划轨迹、实际轨迹和动作接口说明。
请先找出第一次分歧，区分已知事实与可能解释，
再帮助我设计一个小检查来定位原因。
```

**判断一次改善说明了什么**

```text
请按已加载的 Flatland Research Coach 指南开展讨论。
请审视我提供的前后两次实验：它们是否从可比的起点开始，
使用了什么资源，实际完成了多少工作，失败或超时是否进入统计？
帮助我区分效率变化、策略变化和完整执行收益，并说清证据的边界。
```

**只有一个想法，还没有实验**

```text
请按已加载的 Flatland Research Coach 指南开展讨论。
我暂时没有运行数据。请用一个明确标注为虚构的铁路小例，
带我练习区分观察与解释，并设计能够区分两种解释的实验。
先让我表达判断；我卡住时再逐步给提示。
```

## 内容导航

| 文件 | 用途 |
| --- | --- |
| [中文 skill](SKILL.md) · [English skill](SKILL.en.md) | 教练的入口：问答流程、帮助深度、判断标准与资料边界。 |
| [提问与提示库](references/question-bank.md) · [English](references/en/question-bank.md) | 按目标、接口、实验、泛化和结果解释等困惑选择问题。 |
| [实验记录卡](references/experiment-card.md) · [English](references/en/experiment-card.md) | 记录预期、实际结果、反证条件及下一步选择。 |
| [脱敏思考案例](references/reasoning-cases.md) · [English](references/en/reasoning-cases.md) | 看定性观察如何改变判断，以及哪些新证据会使判断失效。 |
| [agents/openai.yaml](agents/openai.yaml) | 可选的 Codex 展示信息；通用使用不依赖此文件。 |
| [LICENSE](LICENSE) | 本仓库的许可条款。 |

## 研究结论的边界

Flatland 环境之间的版本、转移规则、速度、故障可见性、目标处理、评价方式和资源限制可能不同。每次讨论都应从使用者当前环境中与问题相关的条件出发。

脱敏案例保留定性观察与判断过程，未公开可独立复核的原始实验材料；它们用于启发假设，不能作为公开性能比较或最优性证据。案例的排列也不代表推荐架构或必须复走的研究路线。

可行性、达到既定目标、评价较好与理论最优，需要各自相应的证据。局部检查、本地结果与完整评测支持的结论范围也不同。本项目不承诺特定分数、满分或在所有环境中的最优性。

本仓库不包含来源项目的源码、精确配置、参数、逐例成绩或可重建其方案的实现细节。教练仅使用当前使用者提供或授权访问的材料与公开资料，不主动从历史对话或私有工程中找回来源方案。

如果你的解释得到更强的证据支持，就应更新甚至推翻案例中的判断。达到自己定义并已验证的目标后，可以总结适用条件与未知事项，结束本轮研究。

## 贡献

欢迎通过 [Issue](https://github.com/kidheart/flatland-research-coach/issues) 讨论改进，或通过 [Pull Request](https://github.com/kidheart/flatland-research-coach/pulls) 提交：

- 能区分不同解释的提问，以及使用者卡住时有效的渐进提示。
- 明确标注的虚构教学例，或有权公开并充分脱敏的定性思考案例。
- 更清晰的实验记录方式、措辞修正与翻译。

新增案例请说明观察、可能解释、区分实验、有限结论，以及重新考虑的条件。检查多个案例放在一起时，是否可能暴露来源方案的独特组合。

请勿提交来源项目或他人的私有解法、代码、参数、配置、成绩、日志或提交标识。提交前请确认你有权公开该内容，并愿意让贡献按本仓库相同许可发布。

## 许可

© kidheart。本仓库采用 [Creative Commons Attribution–NonCommercial 4.0 International（CC BY-NC 4.0）](LICENSE)。你可以按许可进行非商业性的分享与改编，但须适当署名、提供许可链接、标明改动，并遵守其他许可条件。商业使用须另行取得许可。

可参考的署名：

> 基于 kidheart 的 [Flatland Research Coach](https://github.com/kidheart/flatland-research-coach)，采用 [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)；如有改动，请在此说明。
