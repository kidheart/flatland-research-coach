[简体中文](README.md) | **English**

![Flatland Research Loop: from observations to testable judgments](assets/cover.svg)

# Flatland Research Loop

**Evidence-guided Flatland Optimization**

An **autonomous Flatland optimization workflow informed by anonymized cases from real experiments**, delivered as an agent-agnostic Markdown skill. Starting from your existing project, an agent reviews evidence, proposes changes, runs evaluations, and preserves the best verified version within defined objectives, constraints, and budgets. Interactive coaching is an optional mode for explicit requests to learn or work through questions.

The repository and skill use the identifier `flatland-research-loop`. Loop refers to the research cycle of observation, hypothesis, experiment, validation, and revision.

The general way to use it is to give an agent the Markdown instructions to read. You can use local files with an agent that supports file access, or upload or paste the text into a chat tool. Automatic discovery, installation, and persistence depend on the host platform; this repository does not assume every agent recognizes a skill format automatically.

This is a portable way to provide guidance, not a claim that every model or agent product has been tested. Actual behavior also depends on the host's context limits, file access, and available tools.

## When to use it

- You have an existing project and want an agent to optimize it within a defined budget and constraints while preserving the best verified version.
- You have results and need to identify what caused an improvement or regression.
- A plan looks reasonable, yet execution stalls, arrives late, or needs repeated repairs.
- A new method helps from a simple starting point but adds little to the complete system.
- Internal metrics, full execution results, and the final evaluation do not agree.
- You want to review a research effort: which judgments have evidence, which remain hypotheses, and whether another experiment is worth the investment.

Provide your own code, logs, evaluation rules, objective, and resource budget. The agent reads existing materials first, reuses verifiable historical results, and addresses only critical missing information that affects effective progress.

## Default workflow: autonomous optimization

An existing project or a clear request for optimization, implementation, or experiments defaults to autonomous research. The agent proceeds directly to reviewing evidence and running bounded experiments. Interactive coaching is used only when you explicitly ask to learn, practice judgment, or work through questions.

**Reuse existing evidence → Identify the problem and make the change → Run targeted smoke checks → Retain, revise, or roll back based on evidence**

First establish the objective, hard constraints, evaluation rules, and available resources. Reuse valid existing results and default to fast, targeted smoke checks on the paths affected by the change. A budget is a ceiling, not a spending target. Do not default to experiment matrices, full A/B evaluations, random-seed sweeps, repeated baselines, or a full evaluation each round. Expand checks or experiments only for a specific unresolved question whose result would change the decision to retain, revise, or roll back. Performance gains require relevant, comparable measurements; passing a smoke check supports conclusions only within the scope checked.

Tie actual checks and results to the version and briefly record failures, timeouts, resource use, retention status, and evidence limits. Roll back the current round's changes if they cause a regression or violate constraints, and preserve the previously verified best version. Summarize and stop when the objective is verified, a budget limit is reached, or no feasible hypothesis remains worth testing.

Within the authorized local scope and budget, the agent can carry out these steps continuously without waiting for a user response or repeated approval each round. It asks only about critical missing information that cannot reasonably be inferred from the available materials and prevents effective progress.

For small changes, the current agent implements and briefly reviews its work. Delegate independent research, review, or execution only when real host tools are available and the task justifies its context and coordination costs; do not create multiple roles every round by default. Collaboration uses actual outputs and evidence. A single agent's role-play dialogue is not independent review.

This skill supplies a Markdown workflow. The host supplies file access, command execution, evaluation, agent delegation, and the permissions for those capabilities. The skill is not a persistent program and does not guarantee continuous or background execution on any platform. Without execution tools, the agent should state its limitations and unfinished work, and must not present expected results as observed experiments. See the [autonomous research guide](references/en/autonomous-research.md) for the detailed workflow.

## Cases retained from real experiments

The [anonymized experiment cases](references/en/reasoning-cases.md) are organized around **what was tried → what was actually observed → how to choose the next branch**. They retain failures, limited gains, and judgments worth testing further. They do not supply a recipe of winning modules or disclose the original code, parameters, or complete configurations.

| Case direction | Actual observations and evidence limits | What to test in your own project |
| --- | --- | --- |
| **C1 · Negative results: equal-cost sideways moves and history-based cost acceptance** | Equal-cost sideways moves produced a tie and took longer. History-based cost acceptance did produce exploration, but the best solution returned was still worse than the control, so it was not integrated. | Record the current and best solutions separately. Compare the final returned result and time under comparable budgets; exploration alone does not establish a benefit. |
| **C2 · Baseline dependence: joint conflict search for a small group of trains** | Small-map results matched the control, and most weak starting points improved. Marginal gains on the mature baseline were very small; these results did not lead to integration. | Run paired comparisons from both weak starting points and the mature baseline to test whether the candidate adds a capability the current system lacks. |
| **C3 · Efficiency: incrementally maintaining reservation and occupancy tables** | At fixed work, paths, cost, random state, and acceptance history matched while time decreased. The candidate included related efficiency changes, so the entire gain cannot be attributed to this one change or extrapolated to a full run. | Isolate incremental maintenance, then separately check consistency and efficiency at fixed work, and actual gains over a full run. |
| **C4 · Metrics: actual evaluation of added search and urgency handling** | After increasing search and urgency handling, the user's two actual evaluation tables showed improved completion counts, on-time counts, and aggregate cost, yet a lower final score. The investigation shifted to individual cases; this does not establish the scoring formula. | Bind each case to its version and evaluation conditions, check the evaluation rules and per-case changes, and leave unverified scoring relationships unresolved. |
| **C5 · Execution: broader rescheduling after a malfunction, selected by plan quality** | The attempt went through tighter conditions, retesting, and disabling with rollback. The assistant reported higher execution penalties and time. The evidence used here consists of test invocations and measurement summaries rather than raw run output; concurrent changes prevent attribution to a single cause. | Replay your own small cases and record actual execution. Isolate the rescheduling scope from concurrent changes and test whether plan quality predicts execution gains. |
| **C6 · Coverage: widening the range of candidate starting points** | Saved plans and full execution showed limited improvements, with no decrease in completion or on-time counts, but time increased. The effects of broader coverage and extra budget were not causally separated. | Design separate comparisons controlling budget or work to distinguish the value of coverage from the benefit of additional computation. |

The right column gives directions to test in your current project; it does not add claims about the original experiments. The bounded observations can help select an experiment. Whether they apply to your environment still depends on actual execution and evaluation.

## Getting the files and loading the guidance

Chinese and English are two editions of the same skill. **Load the edition you prefer; no separate installation is needed for each language.** The repository includes both, and you can ask the agent to respond in the language you use in conversation.

### 1. Download to an ordinary folder

Choose a folder you can give your agent access to. This PowerShell example requires Git and downloads the repository into your home directory without changing any agent's global configuration. It stops if the destination already exists:

```powershell
$researchLoopPath = Join-Path $HOME 'flatland-research-loop'

if (Test-Path -LiteralPath $researchLoopPath) {
    throw 'The destination already exists. Check the existing folder before making changes; do not overwrite it.'
}

git clone https://github.com/kidheart/flatland-research-loop.git "$researchLoopPath"

if ($LASTEXITCODE -ne 0) {
    throw 'Cloning did not complete. Check the Git output and destination directory before proceeding.'
}
```

You can also download the repository files from [GitHub](https://github.com/kidheart/flatland-research-loop) and keep them in an ordinary folder of your choice.

### 2. Give an agent the instructions

For an agent that can read local files, replace `<path-to-repository>` with the full path to your downloaded folder, then enter:

```text
Read <path-to-repository>/SKILL.en.md and follow its optimization workflow
for this conversation. Read relevant files under
<path-to-repository>/references/en/ when the current question calls for them.
Use the environment description and experiment records I provide,
and default to autonomous research for an existing project or optimization request,
respecting the project's constraints and resource budget.
Switch to interactive coaching only if I explicitly ask to learn or work through questions.
Respond in English.
```

If your chat tool cannot read local files, upload or paste the contents of `SKILL.en.md` and ask it to follow those instructions. Provide the relevant reference files as the discussion needs them. A filename or link inside pasted text does not mean the tool has read the linked document; supply its contents if the tool cannot retrieve it.

An agent needs access to the actual guidance to use it. Whether that guidance is automatically loaded again in another conversation depends on your platform.

<details>
<summary>Optional Codex integration</summary>

Codex users can install this same repository as a discoverable skill. This is an optional host-specific integration; the general file-reading workflow above also applies.

Ask Codex to install it:

```text
Use $skill-installer to install the skill at the root of
https://github.com/kidheart/flatland-research-loop
with the name flatland-research-loop.
If an installation directory with that name already exists,
explain the situation before proceeding and do not overwrite it.
```

Alternatively, with Git installed, clone it into Codex's user-level skill directory using PowerShell. These commands stop if the destination already exists:

```powershell
$skillPath = Join-Path $HOME '.agents/skills/flatland-research-loop'

if (Test-Path -LiteralPath $skillPath) {
    throw 'The destination already exists. Check the current installation before making changes; do not overwrite it.'
}

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $skillPath) | Out-Null
git clone https://github.com/kidheart/flatland-research-loop.git "$skillPath"

if ($LASTEXITCODE -ne 0) {
    throw 'Cloning did not complete. Check the Git output and destination directory before proceeding.'
}
```

After installation, start a new conversation; restart Codex if it has not discovered the skill. You can then begin with:

```text
Use $flatland-research-loop and respond in English.
First read the environment description and experiment records I provide,
then carry out autonomous research for my project or optimization request
within the stated constraints and resource budget.
```

See [OpenAI's skills documentation](https://learn.chatgpt.com/docs/build-skills) for skill directories and installation guidance. The `agents/openai.yaml` file supplies optional Codex UI metadata and is not required for reading or using the Markdown guidance.

</details>

## Get started

After loading the guidance, use the following prompt to start autonomous optimization with project materials you have permission to use. It does not depend on platform-specific invocation syntax. Make the referenced files available through their full paths, uploads, or pasted contents.

**Autonomous optimization: start from your project and actual evidence**

Replace the placeholders with your actual paths and requirements:

```text
Read <skill-directory>/SKILL.en.md and
<skill-directory>/references/en/autonomous-research.md, and optimize in autonomous research mode.
Read <skill-directory>/references/en/reasoning-cases.md as needed to select testable hypotheses from relevant anonymized cases.

My project path: <actual project path>
Objective: <primary metric to improve and stopping conditions>
Hard constraints: <correctness, interfaces, permitted scope of changes, and required limits>
Resource budget: <total time, maximum experiment rounds, compute resources, or API cost limit>

First review the existing code, rules, logs, and verifiable historical results,
and identify and preserve the best verified version so far.
Reuse valid evidence, make bounded small changes, and default to fast, targeted smoke checks
on affected paths. Use the evidence to continue, revise, or roll back the current round's changes.
A budget is a ceiling, not a spending target. Do not default to experiment matrices,
full A/B evaluations, random-seed sweeps, repeated baselines, or a full evaluation each round.
Expand checks or experiments only for a specific unresolved question whose result would change the next decision.
Performance gains require relevant, comparable measurements; passing a smoke check does not establish a gain.
Preserve the best verified version without waiting for my response or repeated approval each round.
If real multi-agent tools are available, you may delegate research, review, and execution.
Otherwise, review your own work and state that there was no independent agent review.
Ask only about critical missing information that cannot reasonably be inferred
from the available materials and prevents effective progress.
Report the best version, actual results, failures or timeouts, resource use,
and the limits of the evidence. Clearly identify anything that was not run.
Stop when a stopping condition or budget limit is reached.
```

## Optional: interactive coaching

Use this mode only when you explicitly want to learn or work through questions. The coach asks one or two questions about the key uncertainty at a time, then uses your answers to offer progressive hints and design an experiment together. Without project materials, you can use a clearly labeled fictional example; this exercise does not count as actual optimization or evaluation.

<details>
<summary>Expand learning prompts and a fictional exchange</summary>

**Start with a research question**

```text
Read SKILL.en.md and use interactive coaching mode.
First read the environment description and experiment records I provide,
then restate the facts you already know.
Ask one or two questions at a time about the most important uncertainty.
Help me form a hypothesis that could be disproved and design the next experiment together.
```

**Trace a mismatch between planning and execution**

```text
Read SKILL.en.md and use interactive coaching mode.
I have provided my planned trajectory, actual trajectory, and action interface description.
First identify the earliest divergence and separate known facts from possible explanations.
Then help me design a small check to locate the cause.
```

**Assess what an improvement actually shows**

```text
Read SKILL.en.md and use interactive coaching mode.
Review the before-and-after experiments I provide.
Did they start from comparable conditions? What resources did they use?
How much work actually finished? Were failures and timeouts included in the statistics?
Help me distinguish efficiency changes, strategy changes, and gains in full execution,
and state the limits of the evidence.
```

**Explore an idea before running experiments**

```text
Read SKILL.en.md and use interactive coaching mode.
I do not have run data yet. Use a small railway example clearly labeled as fictional
to help me practice separating observations from explanations
and designing an experiment that can distinguish two explanations.
Let me state my judgment first; give progressive hints when I get stuck.
```

### A fictional exchange

> **This demonstrates optional interactive coaching only. It is a fictional teaching example and does not describe real experiment results or recommend parameter values.**
>
> **Learner:** I added a step and the plan cost went down, so the final evaluation should improve too.
>
> **Coach:** Was that cost recorded after planning or after full execution? Does your evaluation rule use it directly?
>
> **Learner:** Just after planning. Execution still has disruptions, and I have not checked the scoring rule yet.
>
> **Coach:** So far, the evidence supports an improvement at the planning stage. How would you test whether that benefit survives through execution?
>
> **Learner:** I would run a controlled comparison from the same inputs through to completion, recording the plans, execution results, and actual resource use separately. Then I would compare them using the verified evaluation rules.
>
> **Coach:** That helps separate the different stages. What result would make you revise your original judgment?

</details>

## Contents

| File | Purpose |
| --- | --- |
| [SKILL.en.md](SKILL.en.md) | English research guidance: mode selection, workflows, judgment standards, and material boundaries. |
| [Autonomous research guide](references/en/autonomous-research.md) | Bounded experiment cycles, agent responsibilities, actual evaluations, and preserving the best version. |
| [Question and hint bank](references/en/question-bank.md) | Choose questions about objectives, interfaces, experiments, generalization, and interpreting results. |
| [Experiment card](references/en/experiment-card.md) | Record predictions, actual results, conditions that would challenge a hypothesis, and next steps. |
| [Anonymized experiment cases](references/en/reasoning-cases.md) | Attempts, actual observations, bounded conclusions, and next branches drawn from real records. |
| [agents/openai.yaml](agents/openai.yaml) | Optional Codex-specific UI metadata: display name, description, and default prompt. Not a requirement for using the Markdown guidance. |
| [LICENSE](LICENSE) | The repository's license terms. |

## Limits of the research conclusions

Flatland environments can differ in version, transition rules, speeds, malfunction visibility, goal handling, evaluation rules, and resource limits. Each discussion should begin with the conditions in your environment that matter to the question.

The anonymized cases preserve qualitative observations and reasoning. The underlying experiment materials have not been published for independent verification. These cases help generate hypotheses; they do not provide evidence for public performance comparisons or optimality claims. Their order does not prescribe an architecture or a research path to retrace.

Feasibility, meeting a defined objective, achieving a favorable evaluation, and theoretical optimality each require appropriate evidence. Local checks, local results, and full evaluations also support conclusions of different scope. This project does not promise a particular score, a perfect score, or optimality across all environments.

The repository does not include the source project's code, exact configurations, parameters, per-case scores, or implementation details that could reconstruct its solution. The agent uses materials that the current user provides or authorizes it to access, together with public sources. It does not proactively recover the source solution from past conversations or private projects.

If your explanation has stronger evidence, the judgments in the cases should be revised or overturned. Once you have verified the objective you defined, you can record the applicable conditions and remaining unknowns, then conclude that round of research.

## Contributing

Discuss improvements in an [Issue](https://github.com/kidheart/flatland-research-loop/issues), or submit a [Pull Request](https://github.com/kidheart/flatland-research-loop/pulls) with:

- Questions that distinguish explanations, and useful progressive hints for learners who are stuck.
- Clearly labeled fictional teaching examples, or sufficiently anonymized qualitative reasoning cases that you have permission to publish.
- Clearer experiment records, wording improvements, and translations.

For a new case, describe the observation, possible explanations, a distinguishing experiment, a bounded conclusion, and the conditions for reconsidering it. Check whether several cases together could reveal a distinctive combination from the source solution.

Do not submit private solutions, code, parameters, configurations, scores, logs, or commit identifiers from the source project or other people's work. Before contributing, confirm that you have the right to publish the material and are willing to release your contribution under the repository's license.

## License

© kidheart. This repository is licensed under [Creative Commons Attribution–NonCommercial 4.0 International (CC BY-NC 4.0)](LICENSE). You may share and adapt the material for noncommercial purposes under the license, provided you give appropriate credit, link to the license, indicate changes, and comply with its other terms. Commercial use requires separate permission.

Suggested attribution:

> Based on [Flatland Research Loop](https://github.com/kidheart/flatland-research-loop) by kidheart, licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). Describe any changes here.
