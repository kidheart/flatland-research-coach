---
name: flatland-research-loop
license: CC-BY-NC-4.0
description: "Diagnose Flatland planning and execution failures, locate sources of objective loss, choose changes using real anonymized decision cases, and verify affected behavior with lightweight trace tools and targeted smoke checks. Use for autonomous optimization of the user's own railway planning project or optional interactive learning. 不提供原作者解法或满分配置。"
---

# Flatland Research Loop

[简体中文](SKILL.md) | **English**

Find the problem in the user's own code, evaluation rules, and traces, choose a justified change, and confirm it with the smallest necessary check. Proceed autonomously by default; use interactive mode only for explicit learning requests.

## Default deliverable

Address one current problem per round: **Where is the problem? → What supports that judgment? → Where should the code change, and why? → Which small check will confirm it? → What remains unproven?**

Separate observations, explanations, and verified repairs. If the mechanism is unclear, obtain the smallest missing observation rather than choosing an implementation by algorithm name or a case's eventual outcome. Preserve the current best version and state the stopping reason when no next step justifies its cost.

## From diagnosis to a change

1. **Understand the current system.** Read the existing objective, interfaces, entrypoints, and results. Use the [diagnosis guide](references/en/diagnosis.md) to connect the relevant evaluation, planning, action execution, and repair code. Check only rules affecting the current question.
2. **Locate loss and the first divergence.** Select a failure segment relevant to the objective. Distinguish rule constraints, planning problems, execution divergence, coordination waits, and computation overhead. Ground judgments in source code and traces; stationary positions, wait cycles, and aggregate counts alone do not establish a cause of loss.
3. **Use a case to decide.** Read a relevant card from the [decision cases](references/en/reasoning-cases.md), follow its evidence branches, and locate the function to change in the user's project. Cases may be overturned or irrelevant; do not install their methods in sequence.
4. **Implement and check locally.** Make a justified change through the [execution and stopping workflow](references/en/autonomous-research.md). Reuse failure reproductions and valid results first. When needed, use the [trace tools](references/en/tooling.md) to inspect divergences, wait relations, or reservation updates, and perform actual replay through an adapter for the current project.
5. **Save the decision.** Use the [short record](references/en/experiment-card.md) to distinguish the current candidate, verified repairs, and the best version with verified performance. Passing checks without measuring performance leaves performance unconfirmed. Continue only for a worthwhile unresolved question.

Do not default to batch A/B tests, parameter matrices, seed sweeps, repeated baselines, or full evaluation every round. Smoke checks must exercise affected behavior, not just startup. They do not establish global correctness, whole-system speedups, or score gains. Broader validation needs a decision it could change, an explanation of why smaller checks are insufficient, and compliance with the existing budget and project requirements. Budgets are ceilings, not spending targets.

## Tools and reading

This Markdown guide does not depend on a particular agent, model, or API. Its optional Python standard-library scripts are neither a Flatland solver nor an automatic adapter. Check the host's actual capabilities; without execution tools, provide a diagnosis or check plan explicitly marked not run. Delegate only specific tasks that justify context and coordination costs; do not fabricate independent reviews.

Read only the current language and relevant reference sections. Use this file and its English references for English conversations; there is no need to load both editions. Skill discovery and invocation depend on the host, and `agents/openai.yaml` only supplies optional display metadata. The skill does not continue running after the host ends the session.

Investigate supplied project material instead of asking users to repeat it. Ask only about a critical missing project, objective, or scope that affects progress. An unanswered question is not permission.

## Interactive learning

For explicit learning requests, use the [question and hint bank](references/en/question-bank.md), focus on one key judgment at a time, and offer progressive hints based on the answer. Move on when evidence is sufficient. Fulfill direct explanation or implementation requests without forcing a quiz. Clearly labeled synthetic examples can support practice; they are not actual project results.

## Sources and claim limits

Use only code, logs, and public material supplied or authorized by the current user. Do not proactively recover the original author's code, parameters, submission identities, per-instance scores, or final module combination from private projects, past conversations, or other tasks. Public cases do not reproduce that solution, and this repository's synthetic examples and tools do not contain it.

Meeting a target, feasibility, a better score, and theoretical optimality require different evidence. Retained components are not necessarily essential; rejected directions are not universally ineffective. Leave unknown scoring rules, semantics, causal explanations, and unmeasured performance unknown. Success in the source experience does not establish success for the current user.

This guide does not expand conversation authorization. Revert only changes introduced by this work, preserving the user's existing edits. Publication, submissions, paid resources, and external adapter execution follow the current task's authorization. Protect user data when sharing diagnostics; conforming to the tool format does not authorize publication.
