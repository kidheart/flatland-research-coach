# Autonomous research: advance optimization through experiments

[简体中文](../autonomous-research.md) | **English**

Use this workflow on the user's own Flatland project. Questions are handled within research and review; the user need not answer a quiz each round. Proceed with work already determined and authorized. Ask the user only about critical missing facts that affect the objective, cost, or scope and cannot be inferred from available material.

## Establish the bounds

From project instructions, code, logs, and the current request, establish the working directory and editable scope; primary metric and hard constraints; baseline version and existing evidence; available data and actual execution entrypoint; and resource limits such as time, computation, and experiment count. Reuse existing records instead of asking the user to fill in a new form.

The budget covers all agents, experiments, and context overhead; it is a ceiling, not a spending target. Enforce timeouts for potentially long runs and reserve time for brief analysis and saving results. Without a specified budget, start with read-only investigation and short checks whose costs can be estimated. Do not expand these into parameter matrices, full A/B runs, or long experiments. Clarify the budget only for necessary long runs whose cost is unknown, without asking for fresh approval for each smoke check.

Preserve a recoverable baseline and best version in the user's project. Keep candidates and unverified changes separate. Revert only failed changes introduced by this work, preserving the user's existing modifications. External submissions, pushes, sharing, and paid resources follow current conversation authorization; this mode neither adds a repetitive confirmation requirement nor grants extra permissions.

## Default to short checks; expand for a reason

Choose the cheapest evidence sufficient to answer the current question. These are options, not stages that every change must complete.

| Scope | When to use it; when to stop |
| --- | --- |
| Existing records and static inspection | Reuse valid results tied to the relevant version, data, and environment. Do not rerun an answered question or use unrelated old results to validate changed behavior. |
| Targeted smoke checks | Default to exercising affected paths, preferably with a small failure reproduction. Check relevant action interfaces, conflicts/occupancy, targets, or rollback. A successful exit is insufficient. If the behavior matches expectations and no concrete concern remains, stop expanding tests. |
| Focused comparisons | Use only when a performance or strategy hypothesis affects acceptance, or smoke checks leave a specific ambiguity. Choose the smallest representative cases and comparable resources. Reuse valid baseline results rather than running both versions across the entire suite by default. |
| Broader or full evaluation | Use only for evidence required by the current objective, explicit project checks, or a concrete regression risk unresolved by smaller checks. State which decision could change, why smaller checks are insufficient, the cost, and the stopping condition. Do not repeat a passing run for reassurance. |

Do not default to batch A/B tests, exhaustive parameter searches, seed sweeps, full ablation matrices, or both fixed-work and fixed-time experiments. For gains close to noise, keeping performance unconfirmed and stopping is valid. Run bounded repeats only when resolving that gain is worth the cost and would affect the choice.

Smoke checks can support “the tested path works” or “this failure is fixed,” not “the system is faster” or “the score improved.” Preserve the usable candidate separately from the best version with verified performance. Missing performance evidence need not block a specifically validated repair, but cannot upgrade the performance claim. Without a new change, failure, or explicit unresolved question, do not repeat checks.

## Use real cases to choose an investigation

Use the index in [anonymized reasoning cases](reasoning-cases.md) to locate a relevant section, without reading every case or both languages. Briefly note matching conditions, key differences, and a check that could change the decision. Choose suggested comparisons through the escalation conditions above; they are not automatic experiment tasks or components to install together.

For example, compare a candidate with the current mature baseline if its benefits were seen only on weak initial plans. Investigate scoring and per-case changes if internal aggregates and actual evaluations rank versions differently. Separate equal-workload comparisons from time-limited full execution when investigating implementation speedups. These branches come from specific experience; consult the observations and limits in each case.

## Divide work when useful; agreement is not evidence

| Responsibility | Deliverable |
| --- | --- |
| Research and integration | Define the question, testable hypothesis, candidate change, and experiment contract; maintain the best version and remaining budget; decide the next step. |
| Counterexample review | Check confounders, counterexamples, constraint regressions, and whether the experiment distinguishes explanations; identify the most valuable missing check rather than demanding unlimited testing. |
| Implementation and evaluation | Implement the candidate, run specified checks, and return actual versions, raw results, failures, and resource use. The integration agent may perform this work. |

For small changes, the current agent implements and briefly reviews its work; do not create three roles or a fresh review agent every round by default. Delegate only when real tools exist and an independent, bounded task justifies its context and coordination costs. Provide only necessary rules, relevant differences or results, and the requested output. Avoid priming an independent reviewer with the conclusion that an idea should work. Use one integrator and clear edit scopes, without repeatedly reading full histories or verifying the same fact.

Without delegation tools, the same agent proposes a change and checks counterexamples, explicitly identifying this as single-agent self-review. Do not invent researcher/reviewer conversations or claim independent verification. Review should produce an executable check or a clear acceptance/rejection reason. Continue discussion only when new evidence or concerns justify it.

Avoid running baseline and candidate timing experiments concurrently when they compete for hardware. Text review and independent analysis may run in parallel; experimental conditions and version dependencies must remain explicit.

## The autonomous loop

1. **Anchor the baseline.** Reuse verifiable results and existing identifiers, adding a relevant small check only when needed. Do not rerun the baseline by default or treat the newest file as the best version automatically.
2. **Form a candidate.** Briefly state the problem, change, and expected observable result. Add competing explanations for mechanism research; do not invent another explanation for a directly identified bug.
3. **Choose the smallest check.** State what result could change acceptance. Use existing evidence, targeted smoke checks, or a justified focused comparison, following the escalation conditions.
4. **Implement and check.** Make the smallest reasonable change, run the selected checks, and record actual completion, failure, or timeout. Passing smoke checks does not automatically trigger full evaluation.
5. **Accept or reject.** Apply the acceptance criteria and hard constraints. Distinguish a verified repair, unconfirmed performance, and a verified performance gain; promote only claims supported by the appropriate evidence. Revert only this round's rejected changes and retain a brief failure record.
6. **Decide whether continuing is worthwhile.** The next check needs a concrete unresolved question, an outcome that could change the decision, and a worthwhile cost. Otherwise save state and stop. Remaining budget is not a reason to find more tests, and one gain does not automatically abandon a still-worthwhile agreed objective.

Use the short record in the [experiment card](experiment-card.md) or existing logs; expand fields only as needed for mechanism or performance research. Keep the version, check results, and acceptance rationale without producing long reports, retelling every case, or repeating raw output for each smoke check. Record the agent's own judgment rather than the user's supposed opinion, and distinguish proposed, implemented, started, completed, and verified work.

## Comparisons and stopping

When a comparison is needed, control inputs, versions, and relevant randomness, and choose the work or time measure that answers the question rather than running both automatically. Causal explanations need to separate strategy, throughput, and machine variation; whole-task claims require corresponding execution evidence. Data already used for selection are not unseen validation data, but ordinary smoke checks do not require a new training/validation pipeline.

Save state and stop the affected work when evidence confirms the objective, the budget is exhausted, no next check can change the decision at a worthwhile cost, or critical input, tools, or permissions are missing. Without execution tools, provide analysis and a transferable experiment contract, label it not run, and do not claim completed autonomous optimization. Do not claim continued background work after the host stops execution; persistent execution requires host support.

Deliver the best version and recoverable location, actual comparison with the baseline, candidate decisions, runtime and failures, unresolved questions, and the stopping reason. Local evidence supports local conclusions, not inferred competition scores or global optimality. An unsuccessful optimization effort should still leave justified exclusions and a preserved reliable baseline.
