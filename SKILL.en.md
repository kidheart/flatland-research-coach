---
name: flatland-research-loop
license: CC-BY-NC-4.0
description: "Improve Flatland solution quality toward the user's measurable objective using algorithmic mechanisms, real anonymized research cases, targeted correctness checks, and actual solver quality evaluation. Preserve the best verified version and change direction when a candidate fails. Agent-agnostic; optional interactive learning. 不提供原作者解法或满分配置。"
---

# Flatland Research Loop · Autonomous optimization

[简体中文](SKILL.md) | **English**

By default, advance solution quality in the user's own Flatland project. Translate the remaining objective gap into a planning, search, or execution decision that can change, implement a candidate, and judge progress through actual solver results. Diagnosis and smoke checks serve that objective. Honor a narrower request to fix one bug or learn.

## Establish what success means

Recover the **primary metric and direction, target or success condition, hard constraints, best verified version, actual evaluation entry point, and resource limits** from available material. Keep real scoring, official local evaluation, and custom proxies distinct. Do not invent a conversion when the scoring formula is unknown. “100%” is a user target requiring verification, not an algorithmic guarantee.

Default brief delivery: **remaining gap → mechanism changed and evidence → measured quality changes and regressions → candidate decision → next unresolved loss.** A valid schedule that executes correctly can still be poor. Absence of an execution divergence does not establish absence of optimization opportunities.

## Advance through quality feedback

1. **Explain the current gap.** Use the [diagnosis guide](references/en/diagnosis.md) to connect evaluation, code, and run results. Identify major losses, known limits, and unexplained portions. Describe a server regression as a regression with an unconfirmed cause; do not immediately attribute it to overfitting or an inability to improve.
2. **Choose an algorithmic idea that changes decisions.** Consult the [algorithm playbook](references/en/algorithm-playbook.md) as needed: state and time representation, priorities, joint neighborhoods, dependency coordination, repair scope, search throughput, and candidate coverage. Combine these with failures and limited gains in the [real decision cases](references/en/reasoning-cases.md). Explain why the current method handles this loss poorly, which user function should change, and which actual metric should improve. Do not install every algorithm or remain confined to threshold tuning.
3. **Check correctness, then measure quality.** Targeted smoke checks reject broken implementations early. For optimization tasks, a pass leads by default to [quality evaluation](references/en/quality-evaluation.md): actually invoke the candidate solver on representative instances and inspect objective values, major regressions, and resource consumption. Fixed-action replay and successful startup cannot replace this. Reuse baseline results when conditions match.
4. **Validate promising candidates.** After screening finds a gain, validate with relevant instances or independently reserved run conditions not used to select the candidate. Repeating screening cases can check stability, not unseen-scenario performance. Obtain appropriate official evidence for an official-score target. Screening and validation should cover plausible costs of the change, not only favorable cases. Local gains, proxy gains, or one screening result do not establish target attainment.
5. **Preserve the best result and address the remaining gap.** Accept, reject, or continue checking a candidate using the [execution and stopping workflow](references/en/autonomous-research.md), recording quality changes in the [short record](references/en/experiment-card.md). After a candidate fails, update the explanation, change mechanisms, or address the next major loss. Rejecting a candidate does not end the entire optimization task.

Reduce experiments that provide no useful information: do not default to parameter matrices, seed sweeps, exhaustive ablations, or full A/B evaluations every round. The goal is quality feedback that selects solutions; do not remove quality evaluation to save time. Use a scope sufficient to distinguish candidates, reserving expensive full evaluations for promising versions, concrete regression questions, or target verification. A budget is a ceiling, not a spending target.

## Continue or stop while the target is unmet

Save state and report actual results when the target is verified, the user stops the work, an explicit resource limit is exhausted, or a concrete external condition blocks the next necessary action. If the currently feasible directions appear exhausted, identify mechanisms ruled out, remaining possibilities, and the conditions they lack, explicitly stating that the target remains unmet. “Negative expected value” or “no worthwhile next step” alone is insufficient; neither spend indefinitely nor invent progress. Report a pause or blocker supported by evidence, not optimization success.

Proceed within existing authorization without repeated questions or approval each round. Ask only when missing information affects the next action and cannot be inferred from available material. Undo only your own changes and preserve existing work. Keeping the best version does not imply a default `reset --hard` or force push; rewriting history requires corresponding authorization.

## Tools and selective reading

The Markdown guidance is independent of any particular agent, model, or API. Optional Python standard-library helpers include [trace tools](references/en/tooling.md) for divergences, slicing, reservation checks, and replay through a project adapter, plus a [quality comparator](references/en/quality-evaluation.md) that aligns actual evaluation results and exposes gains, regressions, and missing evidence. The comparator does not run a solver, replace the native evaluator, or automatically promote a candidate.

Read only the current language and relevant sections. Chinese uses [SKILL.md](SKILL.md); `agents/openai.yaml` supplies optional display metadata. File access, execution, and real agent delegation come from the host. Delegate concrete independent work when useful and do not fabricate review. If execution is unavailable, state what did not run. The skill does not continue in the background after the conversation ends.

## Learning and source boundaries

When explicitly asked to teach, use the [question bank](references/en/question-bank.md) for progressive questions about key decisions. Satisfy direct explanation or implementation requests without imposing an exam. Label synthetic examples and separate them from real research observations.

Use only material supplied or authorized by the current user. Do not retrieve the original author's private code, parameters, submission identifiers, per-case scores, or final module combination from private projects or past conversations. Public mechanisms are transferable ideas, not a full-score recipe. Environment dependencies and proxy decisions in a source implementation are not universal truths. Applicability, feasibility, actual scores, and optimality require their own evidence. Publishing, external submissions, paid resources, and adapter execution follow conversation authorization; a tool-compatible format does not authorize disclosure of user data.
