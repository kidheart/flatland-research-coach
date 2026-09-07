# Real Anonymized Cases: Attempts, Failures, and Revised Judgments

[简体中文](../reasoning-cases.md) | **English**

These cases describe real attempts from a single Flatland research effort. They were rewritten after the creator authorized a review of experiment notes, structured results, and historical evaluation tables. Organized by research difficulty, they include both directions that were not retained and positive results that hold under specific conditions. Their order does not describe a final architecture or recommended combination. The hypotheses restate the reasoning suggested by the changes and their context at the time; they are not direct quotations.

To protect the original solution, this document omits source code, exact parameters, version identifiers, per-instance scores, and raw logs. It is therefore a qualitative case report grounded in source records, not a public performance comparison that readers can independently reproduce. Each case states its evidence type and limitations, and separates actions taken at the time from experiments suggested now. In autonomous mode, the agent investigates the questions and runs experiments; the user does not have to answer them first.

## Choose a case that matches the current observation

| Current observation | Relevant case | First action |
| --- | --- | --- |
| Search has reached a plateau, and you are considering relaxing the acceptance rule | C1: Allowing sideways moves and temporary deterioration | Check whether new states are actually explored and whether the best solution returned benefits. |
| A method helps from a weak starting point but adds little to the complete system | C2: Joint search for small groups of trains | Measure its marginal value from the same saved, mature plan. |
| Repeated data maintenance consumes substantial time | C3: Maintaining reservations incrementally | Compare states and rollback behavior before measuring throughput under a fixed workload. |
| More tasks finish and aggregate cost falls, but the actual evaluation worsens | C4: Aggregate metrics disagree with the evaluation | Verify versions and per-instance results; stop substituting a proxy for the actual objective. |
| A broader repair plan looks better, but execution regresses | C5: Comparing a broader rescheduling plan with the existing plan | Trace plan replacement through to changes in execution, and check complete execution results. |
| The same candidates repeatedly receive priority, while later opportunities remain unclear | C6: Broadening coverage of candidate starting points | Record actual coverage and compare the coverage policy separately from extra budget. |

If no case fits, formulate a new hypothesis from failure evidence in the current project; do not force a match. After choosing a case, use the [experiment card](experiment-card.md) to record which conditions are similar, which differ, and what result would invalidate the reason for drawing on it.

## C1: Relaxed acceptance changed the exploration, but did not improve the result

**Attempt and rationale.** As search improvements became less frequent, two acceptance rules were tried: allowing sideways moves at equal cost, and using historical costs to accept some temporarily worse candidates. The rationale was that accepting only strict improvements might block paths to better regions of the search space.

**Actual observations.** In screening with a fixed workload, the equal-cost version tied the final cost while adding runtime. Records for the historical-cost acceptance version showed that sideways moves, uphill acceptances, and updates to the best solution all occurred. Nevertheless, the best result it returned was worse than the control. More search activity did not mean a better solution.

**Action taken at the time.** These candidates were not integrated. The previously validated process that accepted strict improvements was retained.

**Evidence and limits.** Experiment notes and structured comparison results support these observations. They do not determine whether the failure came from the acceptance rule, neighborhood, budget, or instance structure. Nor do they rule out other search methods that allow temporary deterioration.

**What to test now.** If your project also encounters a plateau, first record acceptance types, visits to distinct states, the history of the best solution, and the final return value. Then compare both fixed workloads and comparable time budgets. If only the acceptance count rises, without improving the best solution, reject that candidate. If better states are found but not returned, repair the logic that retains the best solution before tuning how permissive acceptance should be.

**When to reconsider.** Evidence shows that the current neighborhood requires crossing a plateau, that states lack diversity, or that the budget and instance structure have changed. A new experiment should address those new conditions, rather than rely only on the hope that another adjustment might work.

## C2: Joint search helped weak starting points but added little to a mature baseline

**Attempt and rationale.** Waiting and rerouting choices were searched jointly for small groups of interacting trains. Broader and related groups were also tried later. The idea was that coordinating interdependent decisions might find improvements that incremental adjustments could miss.

**Actual observations.** Results on small graphs matched an independent joint shortest-path comparison. Most screened cases improved when starting from weaker initial plans. After a thoroughly optimized, mature baseline, however, the directly comparable cases showed only occasional tiny gains; the rest tied. These answer two different questions: whether the method can find an improvement, and whether it is worth adding to the current system.

**Action taken at the time.** The method remained a research candidate. Broader or related groups were investigated using saved, mature, complete plans, avoiding an expensive rerun of the baseline each time. Later screening still mostly yielded small gains, which did not justify adding complexity to the submission.

**Evidence and limits.** Small-graph comparison records, screening results, and research notes support these differences. Agreement on small graphs does not prove optimality on large instances. Whether the mature baseline had already resolved the structures this method handles well remains an unverified explanation.

**What to test now.** Run both a continuation of the baseline and the candidate from the same saved plan, comparing resources and additional gains. If the method helps only from a weak starting point, formulate a separate hypothesis about using it to replace earlier work. Do not use gains from a weak starting point to justify appending a stage at the end. Without enough marginal benefit, retain the current best version.

**When to reconsider.** The baseline differs, early convergence is the main bottleneck, or trajectories reveal joint constraints that the current method repeatedly fails to resolve.

## C3: Maintain reservations incrementally, and check tested behavior before claiming a speedup

**Attempt and rationale.** Local search repeatedly reads and updates path occupancy information. The attempt removed and rebuilt reservations only for affected paths, reusing the rest to reduce repeated construction work. Challenges included shared occupancy, restoring state after undoing a change, and maintaining consistent state after an exception.

**Actual observations.** Table-level comparisons and exception rollback checks passed. In optimizer comparisons with a fixed number of rounds, the candidate and baseline produced identical complete paths, costs, random states, and acceptance histories, while the candidate took less time. This provided finer behavioral evidence than matching only the final number of completed tasks.

**Action taken at the time.** The candidate was retained and followed by complete execution regressions at different scales. Implementation efficiency and final execution benefits were checked separately.

**Evidence and limits.** Structured reservation-state checks and optimizer behavior comparisons are available. The candidate also contained related efficiency changes, so the entire optimizer-level speedup cannot be attributed to one change. Table-level timing supports attribution over a narrower scope. Agreement in a limited set of tests is not a formal proof of equivalence for all inputs, and does not imply that a whole episode must run faster.

**What to test now.** If your bottleneck is similar, first check whether repeated work accounts for a substantial share of the cost. Use differential checks for normal updates, overlapping occupancy, rejected candidates, and recovery from exceptions. Locate any behavioral differences first. Once behavior matches, measure throughput under a fixed workload and complete execution under comparable resources separately. Better results in a time-limited run may come from doing more work; they cannot directly establish a stronger search strategy.

**When to continue or abandon the direction.** Continue only if profiling shows that the relevant overhead warrants the effort. Change direction if the bottleneck lies elsewhere or maintenance complexity offsets the benefit.

## C4: More completions and lower aggregate cost still coincided with a worse actual score

**Attempt and rationale.** Search effort was increased, and the treatment of task urgency during planning was adjusted. The expectation was that completing more tasks in difficult scenarios, meeting more deadlines, and reducing total cost would also improve final performance.

**Actual observations.** Two historical tables of actual evaluation results showed that total completions, on-time completions, and aggregate cost improved, while the final score fell. The per-instance tables contained scenarios with clear regressions. The disagreement was not limited to local estimates versus the server: it also appeared between different levels of aggregation within comparable actual results.

**Action taken at the time.** Analysis shifted to per-instance regressions and failure states. Targeted repair candidates were proposed for further validation, and aggregate metric improvements alone no longer determined whether to submit a candidate.

**Evidence and limits.** This observation can be checked in the two original evaluation tables and per-instance records supplied by the user, making it more direct than an account based only on a verbal measurement summary. The results themselves do not supply the exact scoring formula or prove that a particular malfunction was the sole cause.

**What to test now.** Match each result to its code, data, and evaluation conditions. List changes in the primary metric and constraints for each instance, and verify aggregation or normalization rules. Read the evaluator if the rules are accessible. Otherwise, leave them unknown and use the actual returned metric. Before accepting a candidate, establish where benefits are concentrated and whether regressions affect critical constraints.

**When to reconsider.** If your actual objective is the aggregate quantity, and you have verified that execution and scoring are consistent, you can use it directly to select a version. This case challenges unverified metric substitution, not all aggregate metrics.

## C5: Computing a broader repair plan and choosing between plans did not prevent regression

**Attempt and rationale.** After malfunction repair, an additional rescheduling plan was generated for a broader set of active tasks and compared with the existing plan using a planning-stage quality estimate. The rationale was that broader coordination might remove blocking left by local repair, while accepting only a plan estimated to be better appeared to limit side effects.

**Actual observations.** Historical records preserve a sequence of testing, tightening the replacement conditions, testing again, disabling the mechanism, and removing the corresponding logic. A measurement summary from the time reported increased execution penalties and planning time in a local scenario. A better planning estimate was not sufficient evidence of better execution.

**Action taken at the time.** The comparison mechanism that broadened the scope of replacement was removed. The protected existing behavior was restored before other candidates were assessed.

**Evidence and limits.** The evidence consists of test invocations, editing and rollback records, and the assistant's measurement summary at the time. Raw run output that could be independently checked was not retained. Other repair behavior also changed during this period, so the entire difference cannot be attributed solely to this mechanism. “Oscillation” and “the repair scope must match the malfunction scope” are possible explanations, not rules established by this record.

**What to test now.** Save the time of each plan replacement, the estimated costs before and after it, and the actual trajectories. Identify the first execution divergence, and separate replacement scope, acceptance rules, and other concurrent changes. Even if a plan looks better, it cannot become the best version when complete execution violates a hard constraint or worsens the primary objective. Untested plans remain candidates; estimates must not overwrite validated results.

**When to reconsider.** The current executor differs from the original conditions, there is a reproducible failure of local repair, and controlled comparisons can test the benefit of broader coordination.

## C6: Checking later candidates found limited gains and also took more time

**Attempt and rationale.** The traversal of candidate starting points during local refinement was changed so that candidates later in the order also had a chance to be checked. The rationale was that a limited search might repeatedly spend resources on a few preferred candidates and miss other regions with potential improvements.

**Actual observations.** Behavioral checks recorded the traversal of starting points both when improvements occurred and when they did not. Screening on saved, mature plans improved most cases and tied the rest. In paired complete executions, aggregate cost fell slightly, completions and on-time arrivals did not regress, and total runtime increased. Records also preserved the changes before and after the added stage.

**Action taken at the time.** Local screening and complete execution validation were completed. The cited validation materials do not give the subsequent actual server performance; later success is not attributed backward to this direction.

**Evidence and limits.** Behavioral checks, screening on saved plans, and complete execution records support the limited gains and added time cost. They have not fully separated the causal contributions of extra computation and the coverage policy, so they do not establish that insufficient coverage caused the earlier version's losses. Gains within one stage of a single run, initial-plan differences across runs, and differences in final execution must also remain distinct.

**What to test now.** Record the distribution of candidates actually visited, rather than counting only total iterations. If coverage is insufficient, compare different traversal policies under the same budget, and test an increased budget as a separate control. If the gain comes only from more time, report it as a tradeoff of resources for quality. If the coverage policy remains effective under comparable resources, then investigate the mechanism.

**When to reconsider or abandon the direction.** Recheck when the candidate set, budget, or bottleneck changes. Under a tight resource limit, extra runtime may make a candidate unsuitable for retention despite a local gain.

## Use a case to guide the next round, rather than retracing it

Each round, choose only a case that helps the current decision and turn its question into an executable check. Accept or reject the current implementation under the tested conditions, not an entire algorithm family. Update the judgment if new evidence overturns it.

After reaching the goal, preserve the successful version, failed attempts, and unknowns. Reaching a goal does not prove that every retained component was necessary. Nor must every alternative be exhausted before observed progress can be acknowledged. Whether research continues should depend on the current goal, evidence, and budget.

New cases should have a real basis or be clearly labeled as fictional. Separate actual actions from suggested experiments, and check whether several cases together could expose the source solution's distinctive combination. In interactive mode, a key question from a case can be offered to the user to think through. In autonomous mode, the agent investigates, implements, evaluates, and records the decision.
