# Diagnose the target gap, loss, and improvement mechanism

[简体中文](../diagnosis.md) | **English**

Diagnosis should help choose a mechanism that can improve the current objective. It addresses errors and also **legal programs whose plans execute as intended but whose solutions are poor**. Move to a decision when evidence is sufficient; do not mechanically repeat the whole process.

## 1. Establish the objective, then inspect remaining loss

Obtain the primary metric, direction, target value or completion condition, hard constraints, and best verified result from the request and evaluator. Distinguish official/server metrics, official local results, and custom proxies. Do not replace an unknown primary metric with waiting counts or aggregate cost.

Build a short gap table from existing per-case results:

| Loss or unresolved part | Relationship to the objective | Current evidence | Candidate explanation or next observation |
| --- | --- | --- | --- |
| An observed failure, quality gap, or resource bottleneck in the user's project | Verified scoring effect; say when it cannot be quantified | Version, instance/segment, metric, or relevant function | A mechanism explanation and how to distinguish it |

Unfinished tasks, late arrivals, and waiting can overlap; do not simply add them. If the known evaluator permits a reliable decomposition, use it to rank losses. With an unknown formula, investigate actual returned primary results and traceable cases rather than inventing precise gain estimates.

Call loss unavoidable only when rules or a justified bound establish it. A single-agent relaxation may reveal one kind of improvement opportunity without decomposing multi-agent interaction or proving full-episode optimality. Keep the rest unexplained; failure to improve is not a theoretical limit.

Address localized hard-constraint failures first. Otherwise select a direction using objective loss, evidence, mechanism potential, and implementation/evaluation cost. The easiest small fix is not necessarily the quality gap most worth addressing.

## 2. Connect the objective to current source code

Read the relevant call chains and record the current user's files/functions:

| Relationship | Evidence to inspect |
| --- | --- |
| Which decisions affect the primary metric | Evaluator, candidate selection, cost and penalty calculations. Check whether proxies correspond to final evaluation. |
| How the initial plan is formed | Path search, task/agent ordering, constraint representation, and failure returns. Separate infeasibility, search failure, and budget truncation. |
| What subsequent search changes | Neighborhood generation, affected-agent selection, acceptance/best-solution logic, actual visits, and exits. |
| How plans become actions and occupancy | Plan consumers, action conversion, speed/interval semantics, tick phases, and states after arrival. |
| How events change coordination | Malfunction handling, dependencies, shared constraints, partial repair, and plan handoff. |
| Where limited computation goes | Profiling or relevant timings, separating useful search, repeated maintenance, simulation, logging, and framework overhead. |

A trace tool cannot infer the function to edit or prove a module necessary in the user's project. Verify responsibilities in actual code rather than prescribing a final combination first.

## 3. Distinguish errors from quality bottlenecks using evidence

| Current evidence | What to verify first | Mechanisms to investigate |
| --- | --- | --- |
| Plan and execution differ at the same time | Clock, plan version, action and state conversion; move backward to an explanatory divergence | Plan consumption, state handoff, or execution constraints. Do not replace search before ruling out mapping errors. |
| A legal plan executes reliably but the objective remains poor | Which agents, resources, or decisions concentrate loss, and why current choices retain it | Initial order, objective calculation, candidate comparison, and bottleneck coordination. Quality research does not require a bug. |
| Failed or high-loss agents share an interaction | Specific conflicts/dependencies, corridor or time constraints, and feasible alternatives | Change ordering, affected sets, or joint neighborhoods so coordination that isolated changes cannot express becomes a candidate. |
| Search fails to find plans or frequently exhausts its budget | Legal transitions, overly strong constraints, rejection reasons, state representation, and actual expansions | Search representation/pruning, constraint granularity, or resource allocation. Do not equate failure to find with infeasibility or merely add time. |
| Candidates repeat and a mature plan rarely improves | Visit distribution, decisions the neighborhood can change, best-solution retention, and exit reasons | First fix missed visits or storage errors. If behavior is correct, consider coverage, neighborhoods, or search selection rather than only relaxing acceptance. |
| Static plans look good but execution regresses after events | First handoff difference, blocker source, repair scope, and acceptance criteria | Dependency execution, repair of affected parts, and replacement rules. Let the event justify scope; larger is not automatically better. |
| Computation limits quality | Hotspots, repeated construction, useful search and quality change per available resource | Incremental maintenance, reuse, search allocation, or coverage. Assess throughput benefits through actual time-limited quality. |
| Local improvement but actual scoring regression | Code/result association, evaluation rules, per-case changes, timeouts, and condition differences | Identify the layer where regression occurs. An unknown cause does not justify diagnosing overfitting or declaring the direction exhausted. |

An unchanged position is not automatically wasted time: a slow agent may still advance within a cell, and waiting may be necessary for feasibility. A waiting cycle is a lead; check external participants, available transitions, and release events before calling it deadlock.

Use the [algorithm playbook](algorithm-playbook.md) to explain which representation or decision changes and why that could affect current loss. Use [real cases](reasoning-cases.md) to inspect conditions and failure modes of similar attempts. Choose a direction supported by evidence; do not install algorithms in order or force every problem into an existing case.

## 4. Form a testable improvement decision

Separate observation, explanation, implementation, and measured outcome:

- **Observation** comes from code, state, or evaluation, such as poor achieved quality in a class of instances.
- **Explanation** states why the current mechanism may cause the loss and what would contradict it.
- **Implementation** identifies the user's files/functions and the decision to change, not just an algorithm name.
- **Measured outcome** reports whether the candidate improved the primary objective, affected constraints or costs, and the scope of evidence.

When key evidence is missing, add an observation that changes selection rather than building full telemetry first. Algorithm research does not require proving a software bug: an observed quality gap, plausible mechanism, and discriminating evaluation can justify a bounded candidate implementation.

Before implementation, choose real evaluation cases that expose both the intended benefit and plausible regressions. Evaluate sufficiently long actual execution when a policy affects the full episode. Fixed-action replay or a synthetic toy case is not quality evidence. See [quality evaluation](quality-evaluation.md).

## 5. Negative results update the direction instead of automatically ending work

Keep a short frontier to avoid unsupported repetition:

| Main remaining loss | Tried mechanisms and evidence | Different mechanisms still available | What the next decision needs |
| --- | --- | --- | --- |
| Current user evidence | Implementation failure, ineffective mechanism, local gain, or verified regression | Relevant alternatives in representation, order, neighborhoods, execution/repair, or throughput | An observation, implementation, or quality comparison; specify any missing condition |

For example, if isolated changes cannot alter the relevant agents' mutual constraints, consider a neighborhood capable of changing those decisions together. If the neighborhood can express the opportunity but rarely visits it, inspect selection and budget. If a wrong proxy rejects useful opportunities, inspect the objective criterion. These are evidence-driven shifts between levels, not a prescribed pipeline.

After rejecting a candidate, inspect the main remaining unexplained loss. No gain may end that direction without ending the user's overall objective. If the currently supported frontier has genuinely been investigated, state the remaining alternatives and their missing conditions, then preserve state and explain the pause under the [execution workflow](autonomous-research.md).

## 6. Tools and limits of conclusions

Prefer the project's native evaluation and reproduction entry points. Use [trace tools](tooling.md) when relevant: first-divergence and explicit-wait diagnosis, readable slices, actual adapter execution, and reservation-event checks against observed snapshots. Slicing is not simulation; replay depends on sufficient state and a faithful adapter; the synthetic runner does not represent Flatland.

A local check can confirm a repair on the tested behavior. Optimization conclusions also require actual candidate-solver quality comparisons and corresponding promotion evidence. Use the [experiment record](experiment-card.md) for the gap, mechanism, measured change, best version, and next step. Successful diagnosis is not an improved score.
