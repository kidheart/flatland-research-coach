# Autonomous optimization: from the target gap to candidate promotion

[简体中文](../autonomous-research.md) | **English**

Use this workflow to advance the user's own Flatland objective. Take over the actual code and scores first, assess current capabilities and gaps with the [diagnosis guide](diagnosis.md), then use the [algorithm playbook](algorithm-playbook.md) to implement and evaluate. The agent proceeds by default toward 100% / full marks on the current benchmark, unless the user specifies another objective or a limited repair or learning scope. The user need not answer questions every round.

## 1. Establish the objective and a recoverable starting point

First inspect the enabled algorithms, candidate generation and acceptance, execution/repair, and evaluator entry point. Assess whether the solver is a simple structure, partly mature, or already a strong baseline while reading the request, rules, and results. Keep the following takeover information in the project's existing record.

| Item | Decision to establish |
| --- | --- |
| Primary objective | Default to 100% / full marks on the current benchmark without asking the user to choose a target. Verify metric, direction, and full-score definition. Do not invent conversions; ask for the evaluation convention if no full score is defined. |
| Current solver and scores | Active algorithms and implementation capabilities, latest and best scores, corresponding versions, and component/per-case losses. A total score does not replace the scoring rules. |
| Hard constraints | Legal actions, occupancy rules, runtime, and other real limits. Do not improve an objective by violating its constraints. |
| Best verified version | Recoverable location, measured result, and evidence scope. The latest files are not automatically the best version. |
| Evaluation conditions | Data, environment, version, entry point, and relevant randomness. Separate server results, official local metrics, and custom proxies. |
| Resources and authorization | Existing time, compute, and external execution limits. Reuse session authorization rather than seeking approval repeatedly. |

When scores, detailed results, or rules are absent from the available material, directly request the missing items in one compact question: for example, current/best version scores, component or per-case results, and the benchmark's scoring method and limits. Do not ask what score the user wants or treat an unknown score as zero. While awaiting answers, continue source inspection and evaluation preparation that do not depend on them; leave affected objective and promotion decisions pending. Do not ask again for supplied information. See the [question bank](question-bank.md) for wording.

Choose the scale of change using code and scores. If a simple solver clearly lacks coordination capabilities, directly construct a candidate with a substantial capability upgrade; with a mature solver, work on its remaining gap. Search representation, ordering, and joint improvement may be implemented together when they need to cooperate. Do not impose one tiny change per round.

No stated budget does not prohibit quality evaluation: inspect the native runner and existing timings, then proceed with a representative evaluation whose cost can be estimated and whose timeout is appropriate. Clarify expensive runs with unknown cost or resources outside authorization; do not invent a large default experiment budget.

Keep the best version and the user's existing work recoverable while working on a candidate. On failure, undo only this round's own changes or discard the isolated candidate. Do not default to recommending history deletion, a hard reset, or force-pushing; rewriting history needs corresponding session authorization. Restoring a reliable version is not a reason to stop research.

## 2. Separate correctness checks from quality evidence

When the user asks for better solutions or scores, **smoke checks admit a candidate to evaluation; quality comparison is required to accept an optimization**. A narrowly scoped interface repair may finish after its affected behavior is verified. If the overall task remains quality improvement, that repair completes only a stage.

| Gate | Question and condition for progress |
| --- | --- |
| Targeted smoke | Does the affected behavior obey the rules, fix the original failure, and preserve relevant update/recovery behavior? Diagnose failures; after a pass, quality candidates proceed to actual evaluation. |
| Representative quality screen | Does the candidate improve the primary objective against a valid baseline, and at what cost? Run the actual candidate solver on representative instances covering the target loss and plausible adverse effects, using episodes or native quality evaluation long enough to expose downstream consequences. |
| Promotion validation | Does improvement extend beyond cases used for development and selection? Within the current benchmark, evaluate promising candidates on held-back or fresh cases and cover exposed regression risks. Data used to choose the approach are not independent validation. If no held-back cases are available, state that limit and proceed through available official evaluation or stability checks; do not require cross-benchmark generalization as a gate. |
| Authoritative target confirmation | Does the claim require official or server evidence? Competition score and target-attainment claims require the corresponding real evaluation. If unavailable, retain a pending candidate without inventing a score or completion. |

Before screening, explain why the selected cases can reveal both the benefit and its possible cost. Do not select only known wins. If a policy affects the full episode, a few successful opening actions cannot establish its final result. Fixed-action replay can check execution; evaluating planning quality requires actually invoking the candidate's planning or repair decisions.

Reuse historical baseline results when inputs, versions, and relevant resource conditions match; do not rerun both versions automatically. Choose the resource basis needed for the question. Compare time-limited tasks under their actual limits rather than requiring both fixed-work and fixed-time matrices. Retain missing results, failures, timeouts, and per-case regressions; never compare only successful samples. See [quality evaluation and comparison](quality-evaluation.md).

Actively allow bounded trials of parameters, algorithm combinations, and applicability conditions. Propose a few distinct candidates, such as changes to priority, joint neighborhoods, route/timing choices, or stage budgets, then select using actual quality. An idea does not need proof of success before a trial: a comparable evaluation, manageable cost, and plausible benefit justify exploration. Treat cooperating changes as one candidate rather than requiring separate module tests.

Do not default to parameter grids, seed sweeps, or exhaustive ablations. Start with a representative comparison of appropriate cost, then add informative evaluation when gains or uncertainty justify it. Reject a current candidate with no clear benefit; “performance unconfirmed” cannot substitute for the requested quality conclusion. Use a complete benchmark when promotion or target confirmation needs it, not mechanically every round.

## 3. The autonomous loop

1. **Update the target gap.** Read valid results for the best version and identify the main losses, unexplained remainder, and current priority. A solver can be correct yet make poor planning decisions; do not search only for crashes and trace divergence.
2. **Choose the mechanism and scale of change.** Use [diagnosis](diagnosis.md), [algorithm ideas](algorithm-playbook.md), and relevant [real cases](reasoning-cases.md) to locate limits in representation, search, coordination, or recovery. Decide whether the gap calls for an algorithmic architecture upgrade, cooperating mechanism changes, or a parameter/budget trial. Identify the decisions to change in the user's code, expected benefit, and possible cost. Where a complete causal explanation is missing, label the idea exploratory and allow measurement to decide.
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
| No benefit under comparable conditions | Reject this candidate and update the explanation. Use remaining loss to change mechanisms, combinations, parameter regions, or search coverage. One failed setting does not disqualify an algorithm family; do not endlessly adjust the same region. |
| Local improvement but authoritative regression | First record “regression observed; cause unknown.” Check submitted version, evaluation conditions, per-case loss, constraints, and budget before investigating scenario differences. Discuss overfitting only with supporting evidence; it is not a ready-made reason to stop. |

Maintain a short mechanism frontier: main remaining loss, tried directions and outcomes, other mechanisms or combinations, and the next distinguishing evidence. It supports changing direction without requiring every algorithm to be tested. Check whether work stays trapped at one level: after repeatedly tuning online repair, inspect initial ordering and joint planning; after tuning search intensity, inspect expressive limits, missed visits, objective alignment, and time allocation. More accepted moves or more tests do not replace improved quality. A few failures or old code comments cannot prove a performance ceiling.

## 5. Delegation and stopping

Use independent agents for concrete, bounded work that saves effort or improves judgment, such as checking a mechanism's counterexample, implementing an isolated candidate, or inspecting per-case regressions. One integrator maintains the objective, best version, and total budget. Avoid duplicating the full history across agents or timing competing versions concurrently on shared hardware. Do not claim independent review when none occurred.

**Rejecting a candidate, completing a repair, and stopping the whole optimization task are different decisions.** With an unmet target and available resources, “no worthwhile next step” or an unsupported judgment of negative expected value does not justify stopping. Investigate another mechanism behind the unexplained loss or obtain evidence that determines a direction.

End or pause the whole task when the objective has corresponding evidence, the user asks to stop, the real budget is exhausted, or a necessary next action is blocked by a specific missing input, tool, or authorization. When the current candidate list runs out, expand to another mechanism, combination, or algorithmic architecture, or obtain an observation that determines a direction. An exhausted list is not itself a stopping condition. If progress is actually blocked, state what was tried, remaining alternatives, the concrete condition preventing the next step, and how to resume. Ambition does not permit invented progress, unlimited spending, or exceeding the user's explicit scope.

Deliver **objective and remaining gap → mechanism and changes → actual quality comparison → candidate and best versions → next action or specific pause reason**. State when the target remains unmet. A local negative result does not prove infeasibility, and success on one benchmark does not prove universal optimality. Do not claim background work after the host ends execution.
