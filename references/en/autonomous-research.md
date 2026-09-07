# After diagnosis: implement, confirm, and stop

[简体中文](../autonomous-research.md) | **English**

Use this after the [diagnosis guide](diagnosis.md) identifies an evidence-supported problem and a next decision. If the fault is already located, proceed directly to a local repair; if a critical observation is missing, collect it first. The user need not answer a quiz each round. Ask only about critical facts that cannot be established from available material and affect progress.

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

## The decision to establish before editing

Map the diagnosis to a file/function in the user's project. Explain its connection to the objective, the judgment supported by evidence, and the change expected in the smallest check. Do not manufacture competing hypotheses for a directly located simple bug. For an unconfirmed mechanism, state which observation could refute it.

When experience helps, read only a relevant [decision card](reasoning-cases.md). Its evidence branches guide where to inspect or whether to change direction; they do not supply code. If clock, occupancy, or blocking semantics are missing, establish the mapping first. Unreliable diagnostic output must not drive solver changes.

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

1. **Preserve the starting point.** Retain a recoverable version and valid existing results. Do not rerun the baseline by default or treat the newest file as the best version automatically.
2. **Receive the diagnosis.** Connect the problem and evidence to the user's function. With insufficient diagnosis, the current candidate is an observation change, not a speculative algorithm change.
3. **Define confirmation.** State how the original failure should change and which related behavior must remain valid. Use a native small reproduction, or the [tool protocol](tooling.md) to extract a segment, check events, and replay through a project adapter. A slice alone is not execution.
4. **Implement and check.** Change the located decision or implementation, run the selected check, and record actual completion, failure, or timeout. On failure, revisit the diagnosis rather than automatically expanding search or a test matrix.
5. **Accept or reject.** Apply acceptance criteria and hard constraints, distinguishing a verified repair, unconfirmed performance, and a verified performance gain. Revert only this round's rejected changes; promote only claims supported by appropriate evidence.
6. **Update the diagnosis or stop.** Feed results back into the selected branch and record excluded explanations and reconsideration conditions. Continue only for a decision-changing check worth its cost, not because budget remains.

Use the short record in the [experiment card](experiment-card.md) or existing logs; expand fields only as needed for mechanism or performance research. Keep the version, check results, and acceptance rationale without producing long reports, retelling every case, or repeating raw output for each smoke check. Record the agent's own judgment rather than the user's supposed opinion, and distinguish proposed, implemented, started, completed, and verified work.

## Comparisons and stopping

When a comparison is needed, control inputs, versions, and relevant randomness, and choose the work or time measure that answers the question rather than running both automatically. Causal explanations need to separate strategy, throughput, and machine variation; whole-task claims require corresponding execution evidence. Data already used for selection are not unseen validation data, but ordinary smoke checks do not require a new training/validation pipeline.

Save state and stop the affected work when evidence confirms the objective, the budget is exhausted, no next check can change the decision at a worthwhile cost, or critical input, tools, or permissions are missing. Without execution tools, provide analysis and a transferable experiment contract, label it not run, and do not claim completed autonomous optimization. Do not claim continued background work after the host stops execution; persistent execution requires host support.

Deliver the problem location, evidence, change rationale, actual checks, and unproven claims, with recoverable candidate/best-version locations and the stopping reason. State when performance comparisons were not run; local diagnosis does not establish competition scores or global optimality. Even without an improvement, preserve justified updates and a reliable baseline rather than treating a tested negative result as a permanent ban on a method family.
