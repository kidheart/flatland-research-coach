# Explain the loss before choosing where to change the code

[简体中文](../diagnosis.md) | **English**

Start from the user's current problem, not an algorithm. Diagnose only as far as needed for the next decision. If the fault is already located, verify it directly instead of retracing this entire guide.

## 1. Connect evaluation to actual code

Locate the relevant call sites in the current project and note them in existing logs:

| Relationship to establish | Evidence to inspect |
| --- | --- |
| Which losses affect the objective, and which are secondary observations | Evaluator, primary metric, and hard constraints. Unfinished tasks, lateness, and waiting can overlap; do not add them directly or infer scores without scoring rules. |
| Which time, direction, and occupancy the plan describes | Planning interface and path consumer. Establish before/after-step timing, speed/interval semantics, and occupancy after reaching a target. |
| How the plan becomes actual actions | Action conversion, state updates, and control call sites. Compare planned and actual fields only at matching times and with matching semantics. |
| What changes future plans after a failure | The project's malfunction handling, repair entrypoints, and shared state. Do not assume a required algorithm architecture. |
| Which computation is worth optimizing | Existing timings or minimal profiling. Separate planning, simulation, logging, and framework overhead; code length does not locate a bottleneck. |

Identify actual user files/functions and verified relationships rather than producing a generic architecture diagram. Trace tools cannot infer which source function to change; the agent establishes that mapping by reading the current project.

## 2. Select a segment that matters to the objective

Prioritize the reported error, a hard-constraint violation, or an instance contributing substantial loss to the actual objective. If only aggregates exist, first find one traceable per-instance result. Do not rerun the whole benchmark by default.

Distinguish three statements:

- **Observation:** Directly supported by code, state, or evaluation, such as the first recorded disagreement with a plan.
- **Explanation:** A proposed cause, such as action mapping possibly using the wrong direction.
- **Verified repair:** The original failure segment passes relevant checks after a change under the same semantics. The claim remains limited to tested behavior.

Find the earliest divergence that may explain later symptoms instead of optimizing the final congestion symptom first. The earliest recorded divergence can still be later than the true cause. If the segment starts with an already abnormal state, obtain relevant earlier context.

## 3. Choose an investigation from the evidence

| Evidence | First question to resolve | Likely location of the decision |
| --- | --- | --- |
| Planned and actual position, direction, or occupancy differ at the same tick | Are clocks aligned, has the plan been replaced, and do action/state conversions agree? | Locate the path consumer or state update first. Related to C5; do not switch search methods before excluding mapping errors. |
| Explicit waiting dependencies recur | Identify blockers, reservation/occupancy sources, known release events, legal transitions, and participants outside the segment. | The user's coordination, repair, or constraint maintenance. A cycle is a clue, not a deadlock proof; choose C2, C3, or C5 from evidence. |
| The plan is invalid, absent, or rejected | Check interface rules, legal transitions, rejection reasons, and input completeness. | Planning or constraint checks. Failure to find a plan does not prove infeasibility or justify extra search budget by itself. |
| Search stalls or visits concentrate on a few opportunities | Inspect actual visited states, acceptance records, best-solution return values, and candidate coverage. | C1 or C6 helps distinguish state/return bugs from a need to change search choices. |
| A method helps weak starts but adds little to the current system | Is the mature starting state comparable, and does an unresolved need for the capability remain? | C2: establish marginal value before replacing or abandoning work, without duplicating existing capabilities. |
| Aggregate gains disagree with actual evaluation rankings | Verify versions, per-instance losses, aggregation, and scoring boundaries. | C4: correct the selection criterion rather than substituting tool counts for the objective. |
| Runtime is the main loss | Inspect representative timings, repeated construction work, and recovery behavior. | C3 or the actual current hotspot; establish whether local gains could affect the objective before optimizing a negligible cost. |

A stationary position does not imply a wasted step: a slow train may progress within a cell, and waiting may be required by constraints. Counts of stationary observations, cycles, and conflicts are not a decomposition of score loss.

Call loss unavoidable only when rules or justified bounds establish that conclusion under the current conditions. Leave the rest unexplained. Unexplained loss is not automatically removable by an algorithm, and lack of current improvement is not a theoretical limit.

## 4. Turn the judgment into one change

After selecting a [decision case](reasoning-cases.md), state which branch the observation supports, what would refute it, and which user function should be inspected or changed. If no case fits, reason from current evidence without forcing a match.

Prioritize located hard-constraint failures; otherwise weigh the objective loss, strength of evidence, edit scope, and verification cost. Do not invent numerical benefit scores or pursue several directions at once.

When evidence is missing, collect only observations that could change the decision, such as one failure tick's plan, action, actual state, and blocking reason. Reuse logs or add a removable observation point rather than building full telemetry first. State the scope if observation overhead could affect timing or behavior.

A decision can be brief:

```text
Problem and evidence: <run/segment/tick/agent; observation versus proposed explanation>
Change location and rationale: <user file/function; connection to objective, or one missing observation>
Verification and retention: <smallest check and actual result; candidate/best version; unknowns and next step>
```

## 5. Confirm the segment without broadening the claim

Use an existing native reproduction entrypoint when available. Otherwise adapt logs and replay through the [tool protocol](tooling.md). Verify field meanings, clock alignment, and segment completeness before relying on diagnostics.

- `diagnose` locates recorded divergence, conflicts under declared semantics, and explicit wait relations to guide inspection.
- `slice` narrows reading scope; it does not create runnable environment state or restore external trains or random state.
- `replay` runs an explicitly selected project adapter with an actual checkpoint and actions. Reproduction needs sufficient environment, train, event, and random state; positions alone are insufficient.
- `reservations` replays reservation events and checks supplied observations. Without actual snapshots, it checks only the event model's internal behavior.

Public synthetic examples demonstrate tool behavior only. Resolve mismatches in project rules, adapters, or data before treating tool success as Flatland validation.

After confirming a local repair, retain results through the [execution and stopping workflow](autonomous-research.md). Leave unmeasured whole-system performance unconfirmed, and expand checks only for a decision-changing question. Feed new evidence back into the diagnosis rather than defending the first selected case.
