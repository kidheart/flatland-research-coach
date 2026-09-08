# Autonomous optimization: from the target gap to candidate promotion

[简体中文](../autonomous-research.md) | **English**

Use this workflow to advance the user's own Flatland objective. Follow the [diagnosis guide](diagnosis.md) to identify loss and a mechanism that can change it, then use the [algorithm playbook](algorithm-playbook.md) to implement and evaluate. The agent proceeds by default; the user need not answer questions every round.

## 1. Establish the objective and a recoverable starting point

Confirm the following from the request, evaluator, and existing results. Use the project's existing record.

| Item | Decision to establish |
| --- | --- |
| Primary objective | Metric, direction, and target value or explicit completion condition. Preserve a requested score target; do not invent conversions when the formula is unknown. |
| Hard constraints | Legal actions, occupancy rules, runtime, and other real limits. Do not improve an objective by violating its constraints. |
| Best verified version | Recoverable location, measured result, and evidence scope. The latest files are not automatically the best version. |
| Evaluation conditions | Data, environment, version, entry point, and relevant randomness. Separate server results, official local metrics, and custom proxies. |
| Resources and authorization | Existing time, compute, and external execution limits. Reuse session authorization rather than seeking approval repeatedly. |

Ask only for a missing detail that affects the decision. No stated budget does not prohibit quality evaluation: inspect the native runner and existing timings, then proceed with a representative evaluation whose cost can be estimated and whose timeout is appropriate. Clarify expensive runs with unknown cost or resources outside authorization; do not invent a large default experiment budget.

Keep the best version and the user's existing work recoverable while working on a candidate. On failure, undo only this round's own changes or discard the isolated candidate. Do not default to recommending history deletion, a hard reset, or force-pushing; rewriting history needs corresponding session authorization. Restoring a reliable version is not a reason to stop research.

## 2. Separate correctness checks from quality evidence

When the user asks for better solutions or scores, **smoke checks admit a candidate to evaluation; quality comparison is required to accept an optimization**. A narrowly scoped interface repair may finish after its affected behavior is verified. If the overall task remains quality improvement, that repair completes only a stage.

| Gate | Question and condition for progress |
| --- | --- |
| Targeted smoke | Does the affected behavior obey the rules, fix the original failure, and preserve relevant update/recovery behavior? Diagnose failures; after a pass, quality candidates proceed to actual evaluation. |
| Representative quality screen | Does the candidate improve the primary objective against a valid baseline, and at what cost? Run the actual candidate solver on representative instances covering the target loss and plausible adverse effects, using episodes or native quality evaluation long enough to expose downstream consequences. |
| Promotion validation | Does improvement extend beyond the cases used for development and selection? Evaluate promising candidates on held-back or fresh cases and cover exposed regression risks. Data already used to choose the approach are not independent validation. |
| Authoritative target confirmation | Does the claim require official or server evidence? Competition score and target-attainment claims require the corresponding real evaluation. If unavailable, retain a pending candidate without inventing a score or completion. |

Before screening, explain why the selected cases can reveal both the benefit and its possible cost. Do not select only known wins. If a policy affects the full episode, a few successful opening actions cannot establish its final result. Fixed-action replay can check execution; evaluating planning quality requires actually invoking the candidate's planning or repair decisions.

Reuse historical baseline results when inputs, versions, and relevant resource conditions match; do not rerun both versions automatically. Choose the resource basis needed for the question. Compare time-limited tasks under their actual limits rather than requiring both fixed-work and fixed-time matrices. Retain missing results, failures, timeouts, and per-case regressions; never compare only successful samples. See [quality evaluation and comparison](quality-evaluation.md).

Do not default to bulk A/B runs, parameter grids, seed sweeps, or exhaustive ablations. Advance one justified mechanism at a time. If representative evidence cannot distinguish gain from variation, add only a bounded comparison that affects selection. Reject a candidate with no clear benefit; “performance unconfirmed” cannot substitute for the requested quality conclusion. Use a complete benchmark when promotion or target confirmation needs it, not mechanically every round.

## 3. The autonomous loop

1. **Update the target gap.** Read valid results for the best version and identify the main losses, unexplained remainder, and current priority. A solver can be correct yet make poor planning decisions; do not search only for crashes and trace divergence.
2. **Choose a mechanism that can change it.** Use [diagnosis](diagnosis.md), [algorithm ideas](algorithm-playbook.md), and relevant [real cases](reasoning-cases.md) to explain why the current representation, search, coordination, or recovery may leave this loss. Locate the user's functions, identify the decision to change, and state what would contradict the explanation.
3. **Set acceptance criteria.** Establish the primary objective, hard constraints, relevant costs, and required evidence before implementation. If the real objective permits local regressions in exchange for aggregate benefit, follow that objective; do not revise criteria afterward to favor a candidate.
4. **Implement, smoke, and screen.** Fix implementation failures, then run actual quality evaluation. Record the tested version, scope, results, and resources. Add only observations needed for the decision, not an unrelated telemetry system.
5. **Validate and decide promotion.** A promising candidate becomes the best at a given evidence level only after the corresponding validation. Distinguish the local best, authoritative best, and pending candidate; local gains cannot overwrite a known better server-tested version.
6. **Update the mechanism judgment and continue toward the target.** On failure, identify the layer that failed and return to loss analysis or change mechanisms. After a local success, inspect the remaining gap. End target work when the target has corresponding evidence.

Use the [short record](experiment-card.md) to preserve changes in the gap, quality results, versions, and the next decision. Do not reread every case, generate long reports, or repeat raw output every round.

## 4. What to do after a failure

| Result | What should change next |
| --- | --- |
| The implementation is inactive or violates rules | Fix integration, state, or constraints. This does not establish that the algorithmic idea is ineffective. |
| The mechanism acts and a proxy improves, but the primary objective does not | Check objective alignment, downstream execution, and the expected beneficiary cases. Do not keep improving only the proxy. |
| Relevant cases improve while another group regresses | Investigate applicability, effects on other agents, and resource costs; then limit scope, change the mechanism, or reject it. |
| No benefit under comparable conditions | Reject this candidate and update the explanation. Select a different mechanism from the remaining loss instead of endlessly adjusting one parameter. |
| Local improvement but authoritative regression | First record “regression observed; cause unknown.” Check submitted version, evaluation conditions, per-case loss, constraints, and budget before investigating scenario differences. Discuss overfitting only with supporting evidence; it is not a ready-made reason to stop. |

Maintain a short mechanism frontier: main remaining loss, tried directions and outcomes, different mechanisms still available, and the next distinguishing evidence. It supports changing direction; it does not require testing every algorithm. More accepted moves or more tests are not substitutes for improved quality.

## 5. Delegation and stopping

Use independent agents for concrete, bounded work that saves effort or improves judgment, such as checking a mechanism's counterexample, implementing an isolated candidate, or inspecting per-case regressions. One integrator maintains the objective, best version, and total budget. Avoid duplicating the full history across agents or timing competing versions concurrently on shared hardware. Do not claim independent review when none occurred.

**Rejecting a candidate, completing a repair, and stopping the whole optimization task are different decisions.** With an unmet target and available resources, “no worthwhile next step” or an unsupported judgment of negative expected value does not justify stopping. Investigate another mechanism behind the unexplained loss or obtain evidence that determines a direction.

End or pause the whole task when the objective has corresponding evidence, the user asks to stop, the real budget is exhausted, or a necessary next action is blocked by a specific missing input, tool, or authorization. A pause is also possible after bounded investigation has ruled out the currently supported mechanism frontier, but document the mechanisms tested, their evidence, remaining alternatives, and what each lacks. Do not merely call them unworthy; neither must every imaginable algorithm be exhausted nor spending continue indefinitely.

Deliver **objective and remaining gap → mechanism and changes → actual quality comparison → candidate and best versions → next action or specific pause reason**. State when the target remains unmet. A local negative result does not prove infeasibility, and success on one benchmark does not prove universal optimality. Do not claim background work after the host ends execution.
