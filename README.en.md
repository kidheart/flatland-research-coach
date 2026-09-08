[简体中文](README.md) | **English**

![Flatland Research Loop: from objective gaps to measured quality](assets/cover.svg)

# Flatland Research Loop

**Autonomous Flatland optimization aimed at measured solution quality**

Start with your objective and existing solver, identify major losses, change planning, search, or execution decisions using algorithmic ideas, and run the candidate solver to see whether quality improves. The core loop is **objective gap → algorithmic mechanism → implementation → correctness check → quality comparison → validation and continuation.**

This agent-agnostic Markdown skill includes Python standard-library tools, Chinese and English guidance, and useful ideas alongside failed directions distilled from real research. Autonomous optimization is the default; learning through questions is optional. The author's full-score code, exact parameters, and reconstructable final combination are not included.

## What you get

- **A defined objective and gap:** the actual primary metric, hard constraints, best verified version, and major remaining losses.
- **A reason to change decisions:** which capability is missing, which user function changes, and why it could improve the objective.
- **Real quality feedback:** objective changes, per-case regressions, failures, and compute costs from runs in which the candidate solver participated.
- **A recoverable best version:** correctness, screening, independent validation, and official confirmation remain distinct.
- **A next action after failure:** update the loss explanation, change mechanisms, or address another relevant instance; rejecting one candidate does not automatically end optimization.

Use it for valid but poor schedules, stalled search, disruption losses, or proxy gains accompanied by official-score regressions. Supply the project, existing results, evaluation rules, objective, and resource limits. The agent reads available material before asking for missing information.

## Transfer ideas from algorithms

The [algorithm playbook](references/en/algorithm-playbook.md) connects research lessons with public algorithmic principles. Choose by the current loss instead of installing a fixed architecture:

| Current problem | Idea to investigate |
| --- | --- |
| Spatially short routes are temporally infeasible or expensive to search | Orientation-aware A*, time constraints, and SIPP: represent conditions that actually determine reachability. |
| Early planning consumes bottleneck capacity and later trains lose out | Order allocation in prioritized planning and LNS neighborhoods that reconsider related trains together. |
| Good plans lose quality after disruptions | Dependency coordination and partial repair: examine commitments, actual state, and the affected boundary. |
| The same candidates consume the available time repeatedly | Fair coverage and resumable search; incremental maintenance reduces repeated work so useful candidates receive more computation. |

In a synthetic bottleneck, A's better route is blocked by B's reservation. Replanning A repeatedly may never help. Releasing related decisions together and replanning that group changes which solutions search can reach. In another synthetic example, restarting a scan at its beginning after every gain can leave later blocking components untouched. **Change what search can express and actually visits, not merely how long it runs.**

These are mechanism explanations; synthetic examples are not competition results. Real cases retain failures and conditional gains. Finding a mechanism in source code does not alone establish that it caused a score improvement.

## Default workflow: verify correctness and quality separately

1. **Define the objective and explain the gap.** Align evaluation rules, runtime constraints, and the best version. Inspect major losses and unexplained portions. A server regression has an unconfirmed cause; one regression does not establish overfitting.
2. **Choose an evidence-backed mechanism.** Map the idea to current project code and predict a quality change and plausible costs, instead of remaining confined to parameter tweaks.
3. **Reject broken implementations with a short smoke check.** Check affected interfaces, conflicts, or recovery behavior. Optimization proceeds to quality evaluation after a pass; a narrowly requested bug fix can finish within its own scope.
4. **Screen representative instances.** Actually invoke the candidate solver through the native entry point, covering the target loss and plausible tradeoffs. Reuse matching baseline evidence rather than selecting only favorable cases.
5. **Validate promising candidates.** Use relevant instances or independently reserved run conditions not involved in selection. Repeating screening cases checks stability, not unseen-scenario performance. An official-score target needs appropriate official evidence. Update the best version and address the remaining gap.

Do not default to parameter matrices, seed sweeps, exhaustive ablations, or full A/B evaluations each round. Quality comparison is part of optimization. Fixed-action replay cannot establish an improved planning policy. Reserve full evaluations for promising versions, concrete regression risks, or target verification. See [autonomous research](references/en/autonomous-research.md) and [quality evaluation](references/en/quality-evaluation.md).

One failed direction does not end an unmet objective. When explicit resources run out or a required external condition is missing, preserve state and explain the unmet target and what is needed next. Pausing because currently feasible mechanisms appear exhausted requires evidence of explored mechanisms, remaining alternatives, and the conditions each lacks. Do not stop with an unsupported “no worthwhile next step” or spend indefinitely. Execution and permissions come from the host; the skill is not a background service.

## Quality and trace tools

| Tool | Actual purpose | Limits |
| --- | --- | --- |
| [quality_compare.py](scripts/quality_compare.py) | Align versions, instances, environment, resources, and objectives from native evaluation exports; report quality changes and major regressions. | Does not run the solver or invent scores. Missing or incomparable results cannot prove improvement; promotion is not automatic. |
| `rail_trace.py diagnose` | Locate the first comparable plan/execution divergence, explicit waits, and conflicts under declared semantics. | Diagnostic leads, not direct proof of causes or performance losses. |
| `rail_trace.py slice` | Extract a relevant time window. | A log slice, not simulation or a complete checkpoint. |
| `rail_trace.py replay` | Actually execute a supplied checkpoint and actions through a project adapter. | Requires adaptation; fixed-action replay cannot replace candidate-planner evaluation. |
| `rail_trace.py reservations` | Check reservation events, releases, rollbacks, and supplied snapshots. | Covers only the given event model and observations. |

Try public synthetic data from the repository root:

```text
python scripts/quality_compare.py examples/synthetic_quality_baseline.json examples/synthetic_quality_candidate.json
python scripts/rail_trace.py diagnose examples/synthetic_trace.json
python scripts/rail_trace.py replay examples/synthetic_replay.json --adapter scripts/synthetic_rail_runner.py
```

The first command compares prepared synthetic evaluation data without running Flatland; the third executes a synthetic miniature runner. They demonstrate tools, not the original competition or real performance. Use your project's evaluator, state semantics, and adapters. Formats and usage are in [quality evaluation](references/en/quality-evaluation.md) and the [trace tooling guide](references/en/tooling.md).

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

Establish the actual metric, target, constraints, best version, and major quality gap.
Use algorithmic mechanisms and real cases to choose a change. After smoke checks,
run the candidate solver for representative quality comparison and validate promising candidates.
Reuse matching baselines; do not default to parameter matrices or full A/B each round.
If a direction fails, update the explanation and choose another. Smoke success is not optimization success.
Proceed within authorization and resources. Report quality changes, regressions,
the best version, and the remaining objective.
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
| [Algorithm playbook](references/en/algorithm-playbook.md) · [中文](references/algorithm-playbook.md) | Select ideas that change search or execution decisions from the observed loss. |
| [Quality evaluation](references/en/quality-evaluation.md) · [中文](references/quality-evaluation.md) | Representative screening, validation, and the quality comparison format. |
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
