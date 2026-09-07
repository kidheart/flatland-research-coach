[简体中文](README.md) | **English**

![Flatland Research Loop: from observations to testable judgments](assets/cover.svg)

# Flatland Research Loop

**Autonomous Flatland research centered on diagnosis**

Start with your existing system, understand its code and evaluation rules, locate losses or the first divergence between plans and execution in its traces, then choose an evidence-based place to change and confirm it with a short smoke check. Anonymized cases drawn from real experiments help an agent decide: **which conditions fit the current symptom, where to look, and which change is worth trying.**

This is an agent-agnostic Markdown skill with Python standard-library trace tools and synthetic examples. Diagnosis and changes proceed autonomously by default; interactive coaching is available when you want to learn, practice reasoning, or work through questions. Chinese and English are two editions of the same guidance, with no separate installation needed. The repository and skill identifier is `flatland-research-loop`.

## What you get

- **Where the problem is:** the relevant train, time, location, or code path and the associated observable loss.
- **Evidence for the diagnosis:** a trace window, metrics, or code evidence, separating the first deviation from its downstream effects.
- **What to change and why:** a chosen location based on the current system's capabilities and the conditions of relevant cases.
- **The smallest useful check:** what actually ran on the affected path, whether it passed, and whether it timed out.
- **What remains unverified:** for example, whether a local fix improves full-run evaluation or whether another explanation remains possible.

Use it when plan cost falls but the final score worsens, rescheduling after a malfunction takes more time, trains stall or arrive late, or a local method loses its benefit inside the full system. Provide the project path, existing results, evaluation rules, and time budget to begin. The agent reads available material first and asks only about critical gaps.

## Default workflow

**Understand the system and evaluation → locate losses and the first divergence → choose where to change based on conditions → make a targeted change → confirm with a short smoke check**

1. **Understand the current system.** Establish inputs and outputs, how plans become actions, execution state, evaluation rules, and what existing modules actually solve. Reuse trustworthy results first.
2. **Ground the symptom in evidence.** Start with a loss that affects the objective, inspect relevant trains and time windows, and trace back to the earliest observable divergence. Consider locations such as path quality, action conversion, state synchronization, reservations and occupancy, or the relationship between metrics and scoring.
3. **Use cases to narrow the change.** Compare their conditions and evidence limits with the current system. Determine whether the system actually lacks the relevant capability and form an explanation that can be checked.
4. **Change and check the affected path.** Preserve the best verified version so far and a recoverable checkpoint, make a targeted change, and run a short smoke check sufficient to test the current explanation. Keep, revise, or roll back based on the result.
5. **Deliver a brief account.** State the finding, evidence, change, actual check, and unresolved points. Expand only when a larger check would change the next decision; stop at the objective or budget limit.

A budget is a ceiling, not a spending target. The current agent handles ordinary small changes; A/B evaluations, multiple agents, and long evaluations are used when specifically needed. A passing smoke check supports only its tested scope. Performance gains still require relevant, comparable measurements.

Within the authorized local scope, the agent continues without repeated approval each round. The host supplies file access, commands, and execution; this skill is not itself a background service. See the [diagnosis guide](references/en/diagnosis.md) and [autonomous research guide](references/en/autonomous-research.md) for details.

## Trace tools

[scripts/rail_trace.py](scripts/rail_trace.py) uses the Python standard library to process traces in a defined format. It helps reduce a failure to an inspectable evidence window. See the [tooling guide](references/en/tooling.md) for the data format, runtime requirements, adapter interface, and usage.

| Tool | Purpose | Limits of the result |
| --- | --- | --- |
| `diagnose` | Summarize observable trace problems and locate the first recorded comparable difference between planned and actual states. | Produces diagnostic leads; confirming the cause still requires the current code, state, and evaluation rules. |
| `slice` | Extract a time window, retaining neighboring records and agent metadata to reduce reading. | Slices logs without advancing an environment; it is not simulation. |
| `replay` | Restore a checkpoint through the current project's adapter and actually advance execution, with an enforced timeout. | Requires a user-provided adapter and checkpoint suitable for the current environment. Run results exist only when execution actually occurs. |
| `reservations` | Audit reference counts, overlaps, releases, rollbacks, and observed snapshots in reservation events. | Checks only the supplied events and snapshots; it cannot alone prove equivalence with a full rebuild or schedule feasibility. |

Try two synthetic examples from the repository root:

```text
python scripts/rail_trace.py diagnose examples/synthetic_trace.json
python scripts/rail_trace.py replay examples/synthetic_replay.json --adapter scripts/synthetic_rail_runner.py
```

The [synthetic miniature runner](scripts/synthetic_rail_runner.py) and [fixtures in examples/](examples/) demonstrate tool behavior. The second command actually executes that runner, with a default timeout of 10 seconds. They are not a Flatland environment, do not correspond to the original competition experiments, and do not establish real-project performance. The tools do not claim automatic compatibility with every Flatland version. Integration requires checking the meanings of state, actions, time steps, and checkpoints in your project.

## Find a real case from the symptom

The [six anonymized experiment cases](references/en/reasoning-cases.md) preserve observations and evidence limits from real records. Select a relevant case using current evidence, then decide whether a change is warranted.

| Current symptom | Case entry and retained observation |
| --- | --- |
| Search explores, but the final returned result does not improve | **C1 · Acceptance rules:** equal-cost sideways moves tied and took longer. History-based acceptance produced exploration, but the best returned solution remained weaker and was not integrated. Check the current and best solutions separately. |
| A method helps weak starting points but adds little to a mature system | **C2 · Baseline dependence:** joint conflict search improved most weak starting points, with very small marginal gains on the mature baseline. Check whether it supplies a capability the current system lacks. |
| Maintaining reservations consumes substantial time | **C3 · Incremental maintenance:** several states matched at fixed work while time fell. Related efficiency changes limit attribution, and full-run gains cannot be inferred. |
| Completion, on-time counts, or aggregate cost improve, but the final score falls | **C4 · Evaluation relationships:** two actual evaluation tables showed this mismatch, prompting a per-case investigation. This does not establish the scoring formula. |
| Plans improve after a malfunction, but execution worsens | **C5 · Rescheduling and execution:** broader rescheduling went through tighter conditions, retesting, and rollback. Test invocations and measurement summaries reported higher penalties and time; those are the evidence used here rather than raw run output, and other changes were present. |
| Broader candidate coverage brings small gains but takes more time | **C6 · Coverage and budget:** saved plans and full execution improved modestly, with no fall in completion or on-time counts. Coverage and additional computation were not causally separated. |

These entries help propose and narrow explanations in the current project. The original experiment materials are not public for independent verification. The cases cannot establish the same benefit in your project or support public performance comparisons or optimality claims.

## Install and use

The core guidance is Markdown. Agents with file access can read the repository directly; chat-only tools can receive the skill and relevant reference files as uploads or pasted text. Automatic discovery, persistent loading, and command execution depend on the host.

Download the repository into an ordinary folder:

```bash
git clone https://github.com/kidheart/flatland-research-loop.git
```

Give the agent the actual directory and send the following prompt. It does not require platform-specific invocation syntax.

```text
Read <skill-directory>/SKILL.en.md as the guidance for this task.
Read its linked references as needed.
My project: <actual path>
Current problem or objective: <symptom or metric to improve>
Available material: <locations of code, evaluation rules, traces, or results>
Permitted changes and time budget: <scope and budget>

First understand the current system and evaluation, then use existing evidence
to locate losses or the first divergence. Choose where to change based on
the conditions of relevant cases, make a targeted change, and run a short smoke check.
Proceed autonomously within the authorized scope. Briefly report the problem,
evidence, reason for the change, actual checks, and what remains unverified.
Respond in English. Switch to interactive coaching only when I explicitly ask
to learn or work through questions.
```

The Chinese entry is [SKILL.md](SKILL.md), with corresponding references under `references/`. A filename or link alone does not mean an agent can read its contents; supply those contents if it cannot.

<details>
<summary>Optional: install as a native Codex skill</summary>

The repository root is the skill root, and the installation directory is named `flatland-research-loop`. Enter this in Codex:

```text
Use $skill-installer to install the skill at the root of
https://github.com/kidheart/flatland-research-loop
with the name flatland-research-loop.
If an installation directory with that name already exists,
explain the situation before proceeding and do not overwrite it.
```

Alternatively, clone into the user-level skill directory with PowerShell. These commands stop if the destination already exists:

```powershell
$skillPath = Join-Path $HOME '.agents/skills/flatland-research-loop'

if (Test-Path -LiteralPath $skillPath) {
    throw 'The destination already exists. Check the current installation; do not overwrite it.'
}

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $skillPath) | Out-Null
git clone https://github.com/kidheart/flatland-research-loop.git "$skillPath"

if ($LASTEXITCODE -ne 0) {
    throw 'Cloning did not complete. Check the Git output and destination directory before proceeding.'
}
```

After installation, use `$flatland-research-loop` in a new conversation; restart Codex if it has not discovered the skill. See [OpenAI's skills documentation](https://learn.chatgpt.com/docs/build-skills) for directories and installation guidance. [agents/openai.yaml](agents/openai.yaml) supplies optional Codex display metadata only.

</details>

## Optional: interactive coaching

When explicitly asked to teach or work through questions, the agent asks one or two questions about the most important uncertainty at a time. It helps you separate observations from explanations, form a hypothesis that could be disproved, and design a small check together. Without actual project material, it can use a clearly labeled fictional example.

```text
Follow the loaded guidance in interactive coaching mode to help me analyze this trace.
First help me find the first divergence between plan and execution,
then let me suggest possible causes. Give progressive hints if I get stuck,
and help me design a small check that distinguishes the explanations.
```

## Contents

| File | Purpose |
| --- | --- |
| [Chinese skill](SKILL.md) · [English skill](SKILL.en.md) | A lightweight entry point and reading routes for the current task. |
| [Diagnosis guide](references/en/diagnosis.md) · [中文](references/diagnosis.md) | Locate problems from the system, evaluation, and traces; choose where to change. |
| [Tooling guide](references/en/tooling.md) · [中文](references/tooling.md) | Trace format, tool usage, and replay integration boundaries. |
| [Trace tools](scripts/rail_trace.py) · [Synthetic examples](examples/) | Local evidence inspection tools and demonstration data. |
| [Autonomous research guide](references/en/autonomous-research.md) · [中文](references/autonomous-research.md) | Bounded progress, actual checks, and version preservation. |
| [Anonymized experiment cases](references/en/reasoning-cases.md) · [中文](references/reasoning-cases.md) | Conditions, observations, and bounded conclusions from six cases. |
| [Question and hint bank](references/en/question-bank.md) · [中文](references/question-bank.md) | Questions for interactive coaching, used as needed. |
| [Experiment card](references/en/experiment-card.md) · [中文](references/experiment-card.md) | Record hypotheses, results, and decisions when further experiments are needed. |

## Privacy and evidence limits

The agent uses project material provided or authorized by the current user and public sources. This repository contains no source-project code, exact configurations, parameters, per-case scores, or implementation details that could reconstruct its solution. It does not call for recovering the source solution from past conversations or private projects.

Environment versions, transition rules, speeds, malfunction visibility, goal handling, and evaluation rules can differ. Diagnosis and changes must follow the current environment. Local checks, local execution, and full evaluations support different scopes of conclusion. The project does not promise a specific score or optimality; case judgments should change when stronger evidence emerges.

## Contributing

Use an [Issue](https://github.com/kidheart/flatland-research-loop/issues) or [Pull Request](https://github.com/kidheart/flatland-research-loop/pulls) to improve diagnosis methods, tools, synthetic examples, and translations. A new case should describe observations, explanations, a check that distinguishes them, and the limits of its conclusions.

Submit only material you have permission to publish and have sufficiently anonymized. Check whether cases reveal the source solution when combined. Do not submit private code, parameters, configurations, scores, logs, or commit identifiers. Contributions are released under the repository's license.

## License

© kidheart. This repository is licensed under [Creative Commons Attribution–NonCommercial 4.0 International (CC BY-NC 4.0)](LICENSE). You may share and adapt the material for noncommercial purposes under the license, provided you give appropriate credit, link to the license, indicate changes, and comply with its other terms. Commercial use requires separate permission.

Suggested attribution:

> Based on [Flatland Research Loop](https://github.com/kidheart/flatland-research-loop) by kidheart, licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). Describe any changes here.
