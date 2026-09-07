# Real Anonymized Cases: From Observations to Code Decisions

[简体中文](../reasoning-cases.md) | **English**

These cases come from one Flatland research effort, rewritten after the creator authorized a review of experiment notes, structured results, and historical evaluation tables. They include discarded directions and conditional positive results; their order implies no final architecture or recommended combination. Rationales restate hypotheses suggested by the changes and context, rather than direct quotations.

Source code, exact parameters, version identifiers, per-instance scores, and raw logs are omitted. This is a qualitative report grounded in records, not an independently reproducible public performance comparison. Each card separates real history and its limits from current decision rules; those rules add no historical facts.

## Diagnose first, then select a relevant card

Start with [diagnosis and modification decisions](diagnosis.md). Diagnose from current project evidence before drawing on a similar case; these six cases may not cover your environment. The hypotheses in this index require checking, rather than following directly from the observations.

| Current observation | Diagnostic hypothesis to check | Card |
| --- | --- | --- |
| Improvement stalls; relaxed acceptance increases activity | Lost best solutions, repeated visits, or no benefit from the current acceptance rule | C1 |
| A method helps weak starts but adds little to the full system | Incomparable starts, duplicated stages, or unresolved joint constraints | C2 |
| Reservation maintenance takes substantial time | Rebuilding is a bottleneck and unchanged state can safely be reused | C3 |
| Completions and total cost improve, but the actual score falls | Misassociated results, a mismatched proxy objective, or per-instance regressions hidden by aggregation | C4 |
| Broader repair improves the plan estimate but worsens execution | Inconsistent handoff state, a mismatched replacement rule, or side effects of changing scope | C5 |
| The same candidates get priority while later ones receive few visits | Traversal omissions, budget truncation, or an unsuitable coverage policy | C6 |

Modification locations below identify conceptual responsibilities. The agent locates the corresponding functions and call chains in **the current user's source**, without finding or transplanting the original author's implementation. Check existing records first, then use one local smoke check that distinguishes the key branches. Act on evidence instead of stopping at an experiment plan. Record decisions in the [experiment card](experiment-card.md); follow the [autonomous workflow](autonomous-research.md) for escalation. Broaden validation only when local results cannot settle adoption and another check could change that decision. Large A/B runs are not the default.

## C1: Relaxed acceptance changed exploration but did not improve the result

**Real history.** As improvements slowed, equal-cost sideways moves and historical-cost acceptance of some temporarily worse candidates were tried: strict improvement might block better regions. Under a fixed workload, the equal-cost version tied final cost and took longer. The historical-cost version did make sideways moves, accept uphill moves, and update the best solution, yet its returned best result was worse than the control. Neither candidate was integrated; the validated strict-improvement process was retained.

**Evidence limits.** Notes and structured comparisons support those observations, but do not identify the cause among acceptance rules, neighborhoods, budgets, or instance structure. They do not rule out other methods that allow temporary deterioration.

**Trigger → verify first.** When search stalls or acceptances surge, inspect distinct visited states, acceptance types, the best-solution history, and the return value. Distinguish failure to find a better solution from failure to retain one.

**Evidence → modification and action.**

- A better solution was found but not returned: fix best-solution storage, restoration, or return handling; defer relaxing acceptance.
- Visits repeat the same states: inspect candidate generation, deduplication, and neighborhood selection. Make a local change where evidence identifies the repetition; a plateau alone does not establish overly strict acceptance.
- New states are explored but the best result does not benefit: keep the validated version and disable this candidate. More acceptances alone do not justify more effort.

**Minimum check and stop/restart.** Run briefly from one relevant saved state; check visits, the best-solution record, and the returned value. End the round once the fix covers the known error. Add a relevant comparison under comparable resources only if retention still depends on benefit. Reopen when plateau structure, insufficient diversity, or changed budgets/instances provide new evidence, rather than merely hoping another adjustment will work.

## C2: Useful joint search need not justify an extra stage after a mature baseline

**Real history.** Waiting and rerouting were searched jointly for small groups of interacting trains, later including broader and related groups, to coordinate decisions difficult to adjust incrementally. Small-graph results matched an independent joint shortest-path comparison. Most screened cases improved from weak initial plans; after a thoroughly optimized baseline, directly comparable cases showed only occasional tiny gains, with the rest tied. The method remained a research candidate. Saved mature complete plans supported checks of broader or related groups without repeatedly rerunning the expensive baseline. Later screening still mainly found small gains, which did not justify added submission complexity.

**Evidence limits.** Small-graph comparisons, screening results, and notes support the differences. Agreement on small graphs proves no large-instance optimality. The explanation that the mature baseline had already handled the relevant structures remains unverified.

**Trigger → verify first.** When a new stage adds little to the full system, check starting plans, resource conditions, and whether the stage actually runs. Then inspect failure trajectories for joint constraints it could still address.

**Evidence → modification and action.**

- Starts differ or the stage does not run: fix saved-plan loading, stage integration, or result recording before broadening joint search.
- Benefits occur only from weak starts: do not append the stage to the mature pipeline. If early work is a demonstrated bottleneck, assess replacing it at the stage-scheduling boundary.
- A reproducible remaining interaction is absent from the current group or boundary: locate group selection and joint-search boundaries and modify them for that interaction. Without such evidence and sufficient marginal benefit, keep the current version.

**Minimum check and stop/restart.** Use the same relevant saved plan to check stage invocation and the local result for one remaining interaction. Compare baseline continuation with the candidate's resources and gains only if additional value determines the decision. Stop appending stages without enough marginal value. Reopen when the baseline changes, early convergence becomes a bottleneck, or new trajectories expose unhandled joint constraints.

## C3: Incremental reservation maintenance needs matching behavior before speed matters

**Real history.** To reduce repeated reservation construction during local search, only affected paths' reservations were removed and rebuilt; the rest were reused. Challenges included shared occupancy, restoration after undo, and exceptions. Table-level comparisons and exception rollback checks passed. With fixed optimizer rounds, complete paths, costs, random states, and acceptance histories matched, while the candidate took less time. It was retained, followed by complete execution regressions at different scales, checking implementation efficiency separately from execution benefits.

**Evidence limits.** Structured reservation-state and optimizer comparisons exist, but the candidate included related efficiency changes: the whole optimizer speedup cannot be attributed to one change. Table-level timing supports narrower attribution. Limited agreement is no formal equivalence proof and does not guarantee a faster episode.

**Trigger → verify first.** If maintenance appears expensive, inspect profiling or local timing to establish whether rebuilding is a major cost. Check the semantics of updates, shared occupancy, and restoration.

**Evidence → modification and action.**

- Most cost lies elsewhere: address the actual hotspot instead of adding incremental-maintenance complexity.
- State differs after undo, rejection, or an exception: fix reservation ownership, updates, or rollback first; suspend speed claims.
- Repeated cost is substantial and state semantics are clear: introduce local reuse at reservation construction/update boundaries, preserving tested behavior. Do not change search strategy concurrently to explain the speedup.

**Minimum check and stop/restart.** Locally compare affected normal updates, overlapping occupancy, rejection, and exception recovery. After they pass, check behavior and timing under a small fixed workload. Stop to locate state differences; end this direction if overhead is insignificant or maintenance costs offset the gain. Broaden runs only if episode-level resource/quality decisions remain unresolved. Gains from doing more work within a time limit are efficiency gains. Recheck when hotspots or the state model change.

## C4: More completions and lower total cost still coincided with a lower actual score

**Real history.** Search effort was increased and the treatment of task urgency was adjusted, expecting more completions and on-time arrivals and lower total cost in difficult scenarios to improve performance. Two historical actual-evaluation tables instead showed better aggregates but a lower final score, with clear per-instance regressions. The disagreement also occurred between aggregation levels within comparable actual results. Analysis shifted to individual regressions and failure states, producing targeted repair candidates for further validation; aggregate improvement alone no longer determined submission.

**Evidence limits.** The user's two original evaluation tables and per-instance records support this observation more directly than a verbal measurement summary. They provide neither the exact scoring formula nor proof that one malfunction was the sole cause.

**Trigger → verify first.** When proxies conflict with the actual objective, match code, data, evaluation conditions, and per-instance primary metrics. Inspect aggregation/normalization in the evaluator when accessible; leave inaccessible rules unknown.

**Evidence → modification and action.**

- Versions, instances, or metrics were mismatched: fix result association and evaluation records before changing the planner.
- The selection criterion optimizes the wrong objective: correct objective calculation/candidate selection using verified rules. If rules are unknown, use actual returned metrics instead of inventing a formula.
- Results are correctly associated and regressions cluster in a concrete failure: use relevant trajectories to locate and fix the responsible constraint handling or execution path. Do not simply add search effort to pursue better aggregates.

**Minimum check and stop/restart.** Recheck relevant rows and aggregates in existing tables first; replay one instance explaining the regression only if necessary. End the round after repairing evaluation association or the local failure. Expand validation only if adoption remains unresolved. If the aggregate is the actual objective and execution/scoring agree, use it directly for selection. This case challenges unverified metric substitution, not aggregate metrics generally.

## C5: Broader repair selected by a better estimate can still worsen execution

**Real history.** After malfunction repair, an extra rescheduling plan covered more active tasks and was compared with the existing plan using estimated planning quality, hoping to remove blocking left by local repair. Records preserve testing, tighter replacement conditions, retesting, disabling, and deletion. A measurement summary reported higher execution penalties and planning time in a local scenario. The comparison mechanism broadening replacement scope was then removed, restoring protected existing behavior before assessing other candidates.

**Evidence limits.** Evidence consists of test invocations, edit/rollback records, and the assistant's measurement summary from the time, without independently checkable raw run output. Other repair behavior changed concurrently, preventing sole attribution to this mechanism. “Oscillation” or “repair scope must match malfunction scope” remain possible explanations.

**Trigger → verify first.** When the plan estimate improves but execution worsens, inspect replacement times, before/after estimated costs, actual state, and the first trajectory divergence. Separate scope, acceptance rules, and concurrent changes.

**Evidence → modification and action.**

- The new plan conflicts with execution-time state or constraints: fix plan submission, state handoff, or execution validation before broadening rescheduling.
- Handoff is correct but an estimated improvement harms the primary objective: fix plan comparison/replacement criteria. Restore validated behavior while the cause is unclear; estimates must not overwrite validated results.
- Local repair leaves a reproducible coordination gap: make a targeted change at affected-task selection and repair boundaries, then check execution. Waiting or plan estimates alone do not establish that broader scope will help.

**Minimum check and stop/restart.** Replay one relevant replacement through its first divergence. After the fix, cover that event and the affected execution segment. A hard-constraint failure or primary-objective regression stops candidate promotion. Broaden validation only if adoption still depends on full-episode effects. Reopen when executor conditions change or a local coordination failure allows controlled verification; this is no permanent ban on broad repair.

## C6: Visiting later candidates brought limited gains and added time

**Real history.** Local refinement's starting-point traversal was changed so later candidates could be checked, aiming to avoid repeated expenditure on a few preferred items. Behavioral checks recorded traversal with and without improvements. Screening on saved mature plans improved most cases and tied the rest. Paired complete executions slightly lowered aggregate cost, preserved completions and on-time arrivals, and increased runtime; records also preserved changes before and after the added stage. Local screening and complete execution validation were completed. The cited material gives no subsequent actual server performance, so later success is not attributed backward to this direction.

**Evidence limits.** Behavioral checks, saved-plan screening, and execution records support limited gains and added time, but do not fully separate extra budget from coverage policy. They do not establish insufficient coverage as the cause of earlier losses. Within-run stage gains, cross-run initial-plan differences, and final execution differences must remain distinct.

**Trigger → verify first.** If visits seem concentrated near the start, inspect the actual visit distribution, exit reasons, and runtime. Distinguish traversal defects from deliberate tradeoffs within a budget; iteration counts alone are insufficient.

**Evidence → modification and action.**

- Unexpected early exits, cursor resets, or omissions occur: fix candidate traversal/termination, initially preserving the budget.
- Traversal is correct but trajectories reveal relevant opportunities in unvisited regions: make a small change to candidate ordering or budget allocation and check benefit within current resources.
- Coverage is adequate, or gains require more time: do not attribute the cause to coverage. Stop this candidate if resource limits exclude it; otherwise report the resource-for-quality tradeoff.

**Minimum check and stop/restart.** From one relevant saved state, inspect visits and exits with and without improvement. Stop when the fix settles the choice. Add equal-budget traversal comparisons or a separate budget control only if distinguishing coverage from extra computation affects adoption. Recheck when the candidate set, budget, or hotspot changes.

## Make the decision concrete

Record “current evidence → judgment → located responsibility/function in the user's source → change or retain → minimum check → result.” If evidence is insufficient, run a check that distinguishes causes; if sufficient, fix the relevant location. Form a new hypothesis when no case fits. Do not turn failures under current conditions into algorithm-family prohibitions.

After reaching the goal, preserve the successful version, failed attempts, and unknowns without exhausting alternatives. Success does not prove every module necessary. New cases need real evidence or a fictional label, separation of actual actions from recommendations, and a check for disclosure through combined cases. Interactive mode can discuss one key judgment; autonomous mode has the agent diagnose, modify, and validate.
