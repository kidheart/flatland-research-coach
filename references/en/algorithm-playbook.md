# Algorithm Mechanisms: Choose the Decision That Can Reduce Loss

[简体中文](../algorithm-playbook.md) | **English**

This is a symptom-based library combining authorized review of research material with general algorithmic ideas. It omits the original solution's final combination, order, parameters, and implementation. These mechanisms are optional; inclusion in a successful version does not establish an individual contribution. First identify which decision still causes loss, then read the relevant entry.

| Current loss signal | Decision to investigate |
| --- | --- |
| A metric improves without an actual score gain | Whether objectives, feasibility, and proxies have been conflated |
| Illegal paths or time search exhausts the budget | State representation, heuristics, and time compression |
| Later-planned trains repeatedly detour or lose access | Who receives scarce passage opportunities first |
| Replanning one train repeatedly changes nothing | Which mutually constrained paths must be released together |
| Feasible plans incur severe losses after disruptions | Passage dependencies, actual progress, and repair scope |
| Unchanged data is rebuilt repeatedly | Whether maintenance savings can fund useful search |
| Search improves but repeatedly visits the same candidates | Coverage and where search resumes after acceptance |
| Success depends on predictions that fail elsewhere | Whether the information driving decisions is available |

Every story below is an **explicitly synthetic teaching example**, not an original map or score. After correctness checks, algorithm candidates still require [quality evaluation](quality-evaluation.md): representative real complete executions against the validated version. A smoke check establishes only whether a local mechanism behaves as expected.

## Objective mismatch: change which result gets selected

- **Signal → decision:** On-time arrivals, internal cost, or average path length improves while the final score falls. Expand the current evaluator's per-case calculation and aggregation before revising candidate and best-version selection.
- **Mechanism:** Separate hard constraints, the formal objective, predicted costs, and search heuristics. Proxies can generate candidates but cannot substitute for the actual score. Completion-versus-cost priorities must follow the user's goal or evaluator, rather than an assumed lexicographic order.
- **Current code responsibility:** Locate score parsing, candidate acceptance, best-version storage, and the returned result. Keep the search's current state separate from the best validated version; exploring temporary deterioration must not lose that version.
- **Synthetic example:** A change makes more trains punctual but sends another group on long detours. If the objective accumulates travel and tardiness costs, the punctuality count alone cannot justify promotion.
- **Falsifiable prediction → evaluation:** On the same real complete cases, revised selection should improve the formal objective while satisfying constraints. Retain per-case regressions and resource costs. A proxy-only gain fails the quality claim and calls for further diagnosis.

See the actual score mismatch in [C4](reasoning-cases.md); [C1](reasoning-cases.md) also shows why more acceptances and best-solution updates do not establish a better final result.

## State and time: A*, orientation, and safe intervals

- **Signal → decision:** The same cell is incorrectly treated as the same state, or long waits create excessive time expansion. Check whether future actions also depend on direction, time, speed phase, and occupancy before choosing a representation.
- **Mechanism:** Include orientation when it changes rail transitions. Reverse static distances can provide a more informative lower bound than geometry alone. If the dynamic model permits merging consecutive safe times, consider safe-interval search while preserving its arrival and waiting assumptions. [Original SIPP paper](https://publications.ri.cmu.edu/sipp-safe-interval-path-planning-for-dynamic-environments)
- **Current code responsibility:** Locate state keys, legal successors, heuristic caching, reservation checks, and dense-path reconstruction. Replacing a priority queue cannot repair incorrect state merging; changed versions or speed semantics require renewed assumptions.
- **Synthetic example:** Two trains enter a junction from different directions and have different exits. Deduplicating by cell can discard the feasible route. Elsewhere, a long wait can be represented by one safe interval instead of enumerating every wait step.
- **Falsifiable prediction → evaluation:** Correct representation should eliminate the relevant illegal path or missed solution. Compression should preserve quality under matching constraints and improve completion or cost within a fixed runtime on real scenarios. Fewer expansions without better final quality is an efficiency result.

## Prioritized planning: order allocates scarce resources

- **Signal → decision:** Individual routes look reasonable, but later-planned trains consistently wait or detour. Inspect junctions and single-track sections already claimed by fixed paths, then reconsider who receives passage opportunities first.
- **Mechanism:** Prioritized planning gains speed by fixing earlier paths and planning against their reservations. That also restricts an earlier train's ability to yield. Deadline slack, remaining distance, and resource dependencies suggest different orders; none is universally best.
- **Current code responsibility:** Locate initial ordering, path reservation, missing-path handling, and candidate retention. Compare a few structurally motivated orders or change a relevant local precedence; avoid unguided seed sweeps.
- **Synthetic example:** A claims the only passage first, forcing B onto a long detour. If A passes slightly later, both can use short routes. The decision to change is resource order, rather than B's single-agent search depth.
- **Falsifiable prediction → evaluation:** Contention losses should fall without merely shifting them to unobserved trains. Compare the full formal objective under the same resources in a real complete case, then check representative congestion conditions for retained benefit.

## Related neighborhoods: LNS must release coupled decisions

- **Signal → decision:** Repeatedly replanning an expensive train returns the same path, or an added stage helps only weak starts. Identify which reserved paths prevent a cheaper route before selecting paths to remove and replan together.
- **Mechanism:** Large neighborhood search keeps most of a solution and destroys and repairs a selected part. Delay, actual blockers, and diversity can guide MAPF neighborhoods. Larger groups expose coordinated changes but increase repair failures and computational cost. [Original MAPF-LNS paper](https://www.ijcai.org/proceedings/2021/568)
- **Current code responsibility:** Locate loss ranking, blocker provenance, neighborhood expansion, reinsertion order, and acceptance. Distinguish encountered search blockers from potential associations based only on shared cells. Preserve outside paths and fully roll back unsuccessful candidates.
- **Synthetic example:** B reserves A's cheap route, while C reserves B's alternative. Releasing A alone changes nothing. Following these dependencies into a related candidate may reveal an arrangement benefiting all three.
- **Falsifiable prediction → evaluation:** Starting from the current mature plan, a candidate should remove the recorded restriction and improve complete-execution quality. Cheap screening from the same saved plan still needs real execution validation. Beating a weak start does not justify appending a stage to a mature system.

See the actual baseline-dependent gains in [C2](reasoning-cases.md). Relaxed acceptance failed to win in [C1](reasoning-cases.md): changed search behavior still needs quality evidence, without implying a ban on that algorithm family.

## Execution coordination: precedence must agree with actual progress

- **Signal → decision:** A promising plan develops waiting cascades or repeated broad rerouting after a disruption. Determine whether passage times changed, resource precedence is unsuitable, or spatial routes themselves need to change.
- **Mechanism:** MCP-style coordination can retain resource precedence while retiming from actual progress; partial replanning can instead alter relevant routes. They address different constraints. Published Flatland research studies planning together with execution coordination. [Flatland planning and coordination paper](https://ojs.aaai.org/index.php/SOCS/article/view/18576)
- **Current code responsibility:** Locate action commitment, actual-progress synchronization, entry tokens or dependency tables, disruption occupancy, and repair boundaries. Advance corresponding state only after a real transition; an unselected candidate must not contaminate live retry bookkeeping.
- **Synthetic example:** Broken train A occupies a section; B waits for A and C waits for B. Simply shifting A's schedule may be insufficient. Propagate actual occupancy effects, then evaluate changing relevant routes or precedence when the fixed ordering cannot resolve the loss.
- **Falsifiable prediction → evaluation:** Coordination should reduce realized disruption losses without adding collisions, stranding, or excessive repair costs. Replay the handoff event, then execute complete disruption cases. A cheaper projected schedule is insufficient for promotion.

See the execution regression and evidence limits of broader repair in [C5](reasoning-cases.md). A wait-graph cycle alone does not prove deadlock; inspect release conditions and execution semantics.

## Computational efficiency: turn saved time into quality

- **Signal → decision:** Rebuilding unchanged reservations or indexes consumes substantial search time. Identify the actual hotspot before choosing which state can safely be reused.
- **Mechanism:** Incremental maintenance retains unchanged paths and removes or adds only affected reservations. Reference counts preserve shared occupancy; transactional restoration handles failure and interruption. Savings must come from eliminating repeated work, not corrupting reservations.
- **Current code responsibility:** Locate reservation updates, position/time indexes, shared-occupancy counts, invalidation, and exceptional rollback. Preserve candidate semantics initially; do not silently change search policy inside an efficiency change.
- **Synthetic example:** Changing a few paths triggers a full-fleet table rebuild, leaving valuable candidates unexplored. Reusing unchanged reservations lets the same time budget complete more relevant repairs.
- **Falsifiable prediction → evaluation:** Under fixed work, verify matching behavior and cost with reduced runtime. Under a fixed total budget, use representative complete executions to see whether added useful candidates improve formal quality. These answer different questions; they do not require two large suites for every small edit.

See the positive result and attribution limits in [C3](reasoning-cases.md). If quality stays unchanged, retain the measured speed result and reconsider how saved resources are allocated; do not claim an unobserved score gain.

## Fair coverage: stop restarting the same hotspot

- **Signal → decision:** Search keeps making small improvements while later dependency groups receive few visits. Record visited roots, distinct groups, the post-acceptance cursor, and exit reasons to detect repeated restarts at the front.
- **Mechanism:** Acceptance may require refreshed dependencies without discarding unvisited candidates. Retain a pending queue and a visited set, give overlooked regions a chance, and rerank after the round while respecting the total budget.
- **Current code responsibility:** Locate root ordering, early exits, acceptance-triggered restarts, dependency caches, and deadlines passed into low-level search. Fairness means justified coverage, not equal time for everything or exhaustive group enumeration.
- **Synthetic example:** Group P repeatedly saves a little and restarts the list. Group Q has a clear unresolved dependency but is never reached. Retaining Q's pending position can expose a different improvement within the existing budget.
- **Falsifiable prediction → evaluation:** Visit records should show relevant previously omitted groups receiving attention. Real complete cases under equal total budgets should improve the formal objective or its stability. Gains requiring extra time are a resource-for-quality tradeoff, not proof of a coverage effect.

This lesson draws on the real continuation work in [C6](reasoning-cases.md). Historical gains were not fully separated from additional runtime, so it cannot be credited alone for the eventual success. More visited groups are not themselves a gain.

## Information boundaries: prediction assumptions are part of the algorithm

- **Signal → decision:** A mechanism degrades in a new environment or relies on supposedly known future events. Check the formal interface, observable state, and environmental assumptions before treating information as a constraint.
- **Mechanism:** Observed disruptions, explicitly supplied calendars, and uncertain predictions are different information classes. One matching prediction does not make the future known. Invalidate contradicted assumptions while preserving an executable response.
- **Current code responsibility:** Locate input provenance, time alignment, model state, mismatch handling, and selection. Use only task-permitted inputs, not evaluator internals. State applicability conditions for versions, motion semantics, and prediction error.
- **Synthetic example:** A model reserves a gap for a typical disruption duration, then keeps trains waiting after the observed fault has ended. Check whether observations release obsolete constraints and separate predicted cost from realized loss.
- **Falsifiable prediction → evaluation:** Across representative real cases where assumptions hold and reasonably fail, inspect the formal objective, constraints, and fallback behavior. Restrict applicability if gains require strong assumptions; a bounded benchmark result is not cross-environment capability.

## Turn one mechanism into the next action

Record “loss evidence → decision to change → current source responsibility → falsifiable quality prediction → representative candidate evaluation.” Follow [quality evaluation](quality-evaluation.md), retain the best actually validated version according to the objective's minimization or maximization direction, and identify which scenarios regress. After a direction fails, return to remaining losses and untested mechanisms; local failure does not mean the user's goal is complete.
