[简体中文](README.md) | **English**

![Flatland Research Loop: from objective gaps to measured quality](assets/cover.svg)

# Flatland Research Loop

**Inspect the solver and scores first. Aim for full marks by default.**

Have the agent inspect your actual algorithms and implementation, read current and best scores, detailed results, and scoring rules, then choose changes with enough scope to address the gap. **Unless you set another objective, optimization aims for 100% / full marks on your current benchmark; there is no need to answer another target-setting question.** The core loop is **solver and scores → missing capabilities → algorithm combinations or targeted trials → actual quality feedback → preserve the best version → continue improving.**

This agent-agnostic Markdown skill includes Python standard-library tools, Chinese and English guidance, and useful ideas alongside failed directions distilled from real research. Autonomous optimization is the default; learning through questions is optional. The author's full-score code, exact parameters, and reconstructable final combination are not included.

## What you get

- **A clear starting point:** the algorithms actually running, current and best scores, associated versions, detailed losses, and scoring rules; missing essentials are requested directly.
- **Changes suited to that starting point:** upgrade a simple solver's architecture when core capabilities are missing; use actual losses to improve combinations, search, or execution in a mature solver.
- **Real quality feedback:** objective changes, per-case regressions, failures, and compute costs from runs in which the candidate solver participated.
- **A recoverable best version:** correctness, screening, independent validation, and official confirmation remain distinct.
- **A next action after failure:** update the loss explanation, change mechanisms, or address another relevant instance; rejecting one candidate does not automatically end optimization.

Use it for valid but poor schedules, stalled search, disruption losses, or proxy gains accompanied by official-score regressions. Start with your project and available scores. The agent reads the material, then bundles questions about missing current/best scores, detailed results, rules, or version information while continuing independent code inspection. If scoring is unclear, it establishes what full marks mean instead of equating all trains arriving with full marks or inventing a percentage. Your explicit alternative objective, narrow repair scope, and resource limits take precedence.

## Transfer ideas from algorithms

The [algorithm playbook](references/en/algorithm-playbook.md) connects research lessons with public algorithmic principles. Choose by the current loss instead of installing a fixed architecture:

| Current problem | Idea to investigate |
| --- | --- |
| Spatially short routes are temporally infeasible or expensive to search | Orientation-aware A*, time constraints, and SIPP: represent conditions that actually determine reachability. |
| Early planning consumes bottleneck capacity and later trains lose out | Order allocation in prioritized planning and LNS neighborhoods that reconsider related trains together. |
| Good plans lose quality after disruptions | Dependency coordination and partial repair: examine commitments, actual state, and the affected boundary. |
| The same candidates consume the available time repeatedly | Fair coverage and resumable search; incremental maintenance reduces repeated work so useful candidates receive more computation. |

In a synthetic bottleneck, A's better route is blocked by B's reservation. Replanning A repeatedly may never help. Releasing related decisions together and replanning that group changes which solutions search can reach. In another synthetic example, restarting a scan at its beginning after every gain can leave later blocking components untouched. **Change what search can express and actually visits, not merely how long it runs.**

These ideas can work together: priorities allocate resource access, SIPP supports single-agent search under time constraints, and LNS allows interdependent blocking decisions to change together. Route choices, entry order, and waiting times create different candidates; incremental maintenance and fair coverage determine how many receive useful attention within the available time. Disruptions call for coordination or repair based on dependencies and actual state. These are selectable capabilities whose use depends on the current solver, results, and environment.

For example, if a solver only plans in one fixed order and detailed results show many trains blocked by each other, prioritize alternative orders and joint replanning of related trains, strengthening low-level temporal search where needed. Several rounds of waiting-threshold adjustments need not come first. If a mature combination already completes nearly all trains, use its actual remaining penalties, execution losses, and search coverage to choose the next change.

These are mechanism explanations; synthetic examples are not competition results. Real cases retain failures and conditional gains. Finding a mechanism in source code does not alone establish that it caused a score improvement.

## Default workflow: inspect the solver and scores, then pursue the gap

1. **Inspect the existing solver and gather scoring information.** Follow the actual entry point into planning, search, and execution code to establish which capabilities are active. Read current and best scores, associated versions, per-case/component results, and scoring/runtime rules. Ask for missing essentials without requesting information already available or asking for the default target again.
2. **Match the scope of change to the loss.** Aim for full marks by default. When a simple solver has structural limitations, actively choose a more capable algorithm combination. Preserve useful foundations in mature systems and address remaining losses. More algorithm names do not establish stronger capabilities; inspect implementation and results.
3. **Implement or run purposeful trials.** Upgrade cooperating modules where needed, or compare a few plausible priority, neighborhood, acceptance, budget, or combination candidates. A reasonable expectation is enough to start a recoverable experiment; a complete causal proof is not a prerequisite. Results determine what to keep, adjust, or replace.
4. **Measure actual quality after smoke checks.** Use short checks to reject interface, conflict, or recovery errors. Then actually run the candidate solver through the native evaluator on representative target-loss and regression scenarios. Reuse matching baseline evidence instead of selecting only favorable cases.
5. **Validate promising candidates and preserve the best result.** Within the benchmark's scope, use instances untouched by selection, reserved run conditions, or the corresponding official evaluation. A fixed public suite can be rerun in full after freezing the candidate, but debugging cases cannot be claimed as independent generalization evidence. An official-score target needs appropriate official evidence; investigate evaluation and per-case differences when local and server results disagree.
6. **Redirect after failure; address the remaining gap after success.** Record which combinations and conditions help, then direct computation toward new candidates or uncovered losses. A few reversions, an unsuccessful neighborhood, or a code comment cannot establish an algorithmic ceiling.

**Tuning parameters and trying combinations for the current benchmark are legitimate optimization work.** Select candidates around the current gap and compare actual score and cost; do not default to huge parameter matrices, seed sweeps, exhaustive ablations, or full A/B evaluations each round. A combination that helps on the current evaluation can be retained while its explanation and stability evidence are developed further. Fixed-action replay cannot establish an improved planning policy. Reserve expensive full evaluations for promising versions, concrete regression risks, or target verification; an inexpensive native suite may simply be run in full. See [autonomous research](references/en/autonomous-research.md) and [quality evaluation](references/en/quality-evaluation.md).

One failed direction does not end an unmet objective. Preserve the best version and continue examining alternative combinations, candidate coverage, and unexplained losses. If the user pauses, explicit resources run out, or a required external condition is missing, preserve state and report the remaining gap, explored evidence, and what is needed next. A short run without improvement does not justify declaring a ceiling. Execution and permissions come from the host; the skill is not a background service.

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
Available scores and material: <current/best scores, detailed results, rules, and code locations; leave missing items blank>
Current symptoms: <optional>
Permitted changes and time budget: <scope and budget>

Inspect the algorithms and implementation actually running, then read scores and rules.
Ask me directly for missing current/best scores, detailed results, associated versions,
or scoring rules while continuing independent code inspection.
Unless I set another objective, aim for 100% / full marks on the current benchmark;
do not ask me to restate that default target.
Choose the scope of change from the solver and its losses: actively upgrade combinations
when core capabilities are missing; target remaining losses in mature systems.
Purposeful parameter and combination trials are welcome; huge sweeps are not the default.
After smoke checks, actually run the candidate solver for quality comparison, then validate promising candidates.
Reuse matching baselines and preserve the best version. If a direction fails, choose another;
do not treat it as evidence of a ceiling.
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
| [Question and hint bank](references/en/question-bank.md) · [中文](references/question-bank.md) | Gather missing scoring information, with optional learning questions. |
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
