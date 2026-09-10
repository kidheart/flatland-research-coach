---
name: flatland-research-loop
license: CC-BY-NC-4.0
description: "Optimize an existing Flatland solver toward full marks by default. Inspect its implementation, obtain current scores and scoring rules, choose substantial algorithmic improvements or targeted trials, and iterate with actual quality feedback. Agent-agnostic; optional learning. 不提供原作者解法或满分配置。"
---

# Flatland Research Loop · Autonomous optimization

[简体中文](SKILL.md) | **English**

Take over the user's Flatland project and **optimize toward full marks / 100% on the current benchmark by default**, without asking whether full marks is the target. Honor an explicit alternative objective, a narrow bug fix, or a learning request. Full marks is the working objective, verified by actual scoring; it does not mean merely getting every train to its destination or proving optimality across all Flatland environments.

## First: inspect the solution and obtain scores and scoring rules

Inspect the current solver and evaluation entry point: state and time representation, conflict handling, initial planning and replanning, joint improvement, and where computation goes. Judge capabilities from code and run records, not algorithm names. Use the [intake and diagnosis guide](references/en/diagnosis.md) to establish:

- **Current solution and best version:** the version actually run, existing algorithm combination, known failures, and whether the working version is the highest-scoring one.
- **Current score and detailed scoring:** latest and historical best scores, associated versions and component / per-case results; denominator, weights, penalties, aggregation, benchmark, and run limits.
- **Runnable evaluation conditions:** local and server entry points, existing results, and resource boundaries. Distinguish official scores, official local evaluation, and custom proxies.

Read supplied code, scores, and rules first, then **ask directly for whatever is missing**, without requesting information twice. When scores and rules are missing, combine the request: “Please provide the current and best scores with their code versions, detailed results, and scoring rules; an existing report or screenshot is fine.” If no evaluation has run, record “not measured” and establish a baseline through the available native entry point. If scoring is unknown, keep the full-marks target pending definition instead of inventing percentages. Continue independent code inspection and preparation while awaiting answers; defer tradeoffs that depend on the missing scoring definition.

Give a brief intake judgment: **current capability → major score losses or capability gaps → distance to default full marks / remaining unknowns → architectural upgrade or targeted strengthening.**

## Match the size of the change to the starting point

If the solution relies on independent shortest paths, one fixed priority order, or lacks time and conflict handling, and code plus scores indicate substantial losses from these limitations, directly evaluate and implement a more capable planning, joint-search, or execution-coordination approach. Necessary, closely related changes may form one candidate; there is no requirement to exhaust tuning of every simple combination first. Strengthen mature systems around their actual remaining losses rather than rewriting them because an algorithm sounds simple.

Read the [algorithm playbook](references/en/algorithm-playbook.md) and [real decision cases](references/en/reasoning-cases.md) as needed. Translate orientation-aware search and SIPP feasibility, PP resource allocation, LNS joint changes, route and timing diversity, dependency coordination and malfunction repair, incremental maintenance and fair coverage into **capabilities missing from this project**. Algorithm combinations, parameters, instance scale, and computation allocation are all potential improvement targets. These ideas guide selection rather than prescribe one fixed pipeline.

## Implement, measure, retain, continue

1. **Form an executable candidate.** State the decision to change, why it is worth trying, and what results will decide acceptance. Bounded empirical parameter trials, combination comparisons, and benchmark adaptation are valid. A plausible idea can be tested before its cause is fully explained; complete causal proof is not a prerequisite every round.
2. **Measure actual quality after short smoke checks.** Once correctness checks pass, invoke the candidate solver on representative instances by default, measuring the primary objective, regressions, failures, and runtime. Use [quality evaluation](references/en/quality-evaluation.md) and reuse matching baselines; startup success and fixed-action replay cannot replace quality results.
3. **Spend evaluation effort where it can decide.** Screen instances covering major losses and plausible costs, then give promising candidates full runs and appropriate independent confirmation. Reserved instances or independent run conditions assess post-selection performance; repeated debugging cases only establish stability. Optimizing the specified benchmark is a legitimate objective; cross-benchmark generalization is not an extra default task. Official full marks require corresponding official evidence.
4. **Preserve the best version and pursue the remaining gap.** Use the [execution workflow](references/en/autonomous-research.md) and [short record](references/en/experiment-card.md) to retain candidate decisions and next steps. If local tuning repeatedly fails, revisit scoring alignment, representation, algorithm combinations, neighborhoods, execution policy, candidate coverage, and computation allocation. Broaden the search for ideas rather than declare a global ceiling.

Trials should progressively narrow choices: compare a few meaningfully different candidates and refine effective trends. Avoid aimless large grids, full A/B runs every round, or selecting only favorable cases; equally, do not remove quality evaluation to save resources. Brief delivery: **best current score → change made → measured gains and costs → next improvement direction**. One rejected candidate does not end the task, and one server regression does not establish overfitting.

## Work boundaries and delivery

Proceed autonomously within existing authorization and resources, without approval each round. When no experiment budget is given, inspect native evaluation cost and start a reasonably scoped runnable comparison; do not invent a low-score stopping line. Save results and a resumption point when the target is verified, the user stops the work, an explicit resource limit is exhausted, or a concrete external condition blocks necessary work. Report the actual gap. If no next step can run, identify unexcluded directions and missing conditions rather than substituting “peaked” or “negative expected value” for evidence or inventing progress.

Preserve the user's work and best verified version. Reverting a candidate means undoing your changes, not defaulting to `reset --hard` or force pushes. Publishing, external submissions, paid resources, and adapter execution follow conversation authorization.

## Tools, learning, and sources

The Markdown guidance is independent of any particular agent, model, or API. Use [trace tools](references/en/tooling.md) for divergences and reservations and the [quality comparator](references/en/quality-evaluation.md) for existing actual results as needed. The comparator neither runs the solver nor promotes candidates automatically. Read only the current language and relevant sections; `agents/openai.yaml` is optional display metadata. Execution, real multi-agent delegation, and persistent operation come from the host. Do not claim runs that did not happen or background work after the conversation ends.

Use the [question bank](references/en/question-bank.md) when teaching is explicitly requested; do not turn optimization intake into an exam. Asking for scores and rules is necessary project intake and does not require teaching mode.

Use only material supplied or authorized by the current user. Do not retrieve the original author's private code, exact parameters, submission identities, per-case scores, or final module combination from private projects or past conversations. Publish transferable ideas and anonymized observations; label synthetic examples and never present them as competition results. Environment dependencies and proxy judgments in a source implementation are not universal truths; improved scores and optimality proofs are different conclusions.
