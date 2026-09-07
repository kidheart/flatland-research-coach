# Autonomous research: advance optimization through experiments

[简体中文](../autonomous-research.md) | **English**

Use this workflow on the user's own Flatland project. Questions are handled within research and review; the user need not answer a quiz each round. Proceed with work already determined and authorized. Ask the user only about critical missing facts that affect the objective, cost, or scope and cannot be inferred from available material.

## Establish the bounds

From project instructions, code, logs, and the current request, establish the working directory and editable scope; primary metric and hard constraints; baseline version and existing evidence; available data and actual execution entrypoint; and resource limits such as time, computation, and experiment count. Reuse existing records instead of asking the user to fill in a new form.

The budget covers all agents and experiments; delegation does not expand it. Set host-enforceable timeouts for potentially long runs and reserve time for analysis and saving results. If no budget was specified, begin with read-only investigation and state a conservative, finite scope for local trials. Clarify before long runs whose cost cannot be estimated; autonomous optimization is not authorization for unlimited computation. An unanswered question is not permission.

Preserve a recoverable baseline and best version in the user's project. Keep candidates and unverified changes separate. Revert only failed changes introduced by this work, preserving the user's existing modifications. External submissions, pushes, sharing, and paid resources follow current conversation authorization; this mode neither adds a repetitive confirmation requirement nor grants extra permissions.

## Use real cases to choose an investigation

Select a relevant item from the index in [anonymized reasoning cases](reasoning-cases.md). Record which conditions match, which differ, what the case suggests checking, and what evidence would undermine its relevance. Cases generate controlled experiments; they are not a list of previously successful components to install together.

For example, compare a candidate with the current mature baseline if its benefits were seen only on weak initial plans. Investigate scoring and per-case changes if internal aggregates and actual evaluations rank versions differently. Separate equal-workload comparisons from time-limited full execution when investigating implementation speedups. These branches come from specific experience; consult the observations and limits in each case.

## Divide work when useful; agreement is not evidence

| Responsibility | Deliverable |
| --- | --- |
| Research and integration | Define the question, testable hypothesis, candidate change, and experiment contract; maintain the best version and remaining budget; decide the next step. |
| Counterexample review | Check confounders, counterexamples, constraint regressions, and whether the experiment distinguishes explanations; identify the most valuable missing check rather than demanding unlimited testing. |
| Implementation and evaluation | Implement the candidate, run specified checks, and return actual versions, raw results, failures, and resource use. The integration agent may perform this work. |

When real delegation tools are available and useful, assign another agent an independent, bounded task. Provide rules, necessary code or candidate differences, raw results, and the required output. Avoid priming an independent reviewer with the conclusion that the idea should work. Define file ownership and let one integrator accept changes; isolate independent candidates or assign disjoint edit scopes.

Without delegation tools, the same agent proposes a change and checks counterexamples, explicitly identifying this as single-agent self-review. Do not invent researcher/reviewer conversations or claim independent verification. Review should produce an executable check or a clear acceptance/rejection reason. Continue discussion only when new evidence or concerns justify it.

Avoid running baseline and candidate timing experiments concurrently when they compete for hardware. Text review and independent analysis may run in parallel; experimental conditions and version dependencies must remain explicit.

## The autonomous loop

1. **Anchor the baseline.** Read existing verifiable results. Reproduce relevant checks or a baseline when needed, recording code, data, environment, seeds, and commands. Do not treat the newest file as the best version automatically.
2. **Form a candidate hypothesis.** Address one clear question with an observation, possible mechanism, competing explanation, change, and controlled variables. State predictions and refutation conditions. For an interface fact check, state what the check can answer without inventing a causal story.
3. **Review the experiment.** Have a reviewer or the same agent check fairness, alignment with the objective, and whether failures count. Incorporate the most consequential concern. Do not add agents or controls merely for appearances.
4. **Implement and run.** Make the smallest reasonable change that tests the hypothesis. Perform necessary correctness checks, then task execution under comparable resources within the budget. Record what actually completed; failures, timeouts, and no improvement are results too.
5. **Accept or reject.** Promote a candidate to the best verified version only when it satisfies hard constraints and the acceptance criteria set in advance. Keep noisy or insufficiently validated results as pending candidates, without silently moving the best-version pointer. Restore this iteration's rejected changes while preserving the failure record.
6. **Continue from evidence.** Update the hypothesis, case applicability, and remaining budget. Continue when a new discriminating question and sufficient budget remain. One gain does not finish a request for continued optimization, and parameter sweeps without new information are not progress.

Reuse fields from the [experiment card](experiment-card.md). In autonomous mode, agents record their own hypotheses, review findings, and judgments; this does not mean inventing the user's opinions. Records may be brief, but must distinguish proposed, implemented, started, completed, and verified work.

## Comparisons and stopping

Control inputs, versions, and relevant randomness, and state whether the comparison uses equal workloads or equal time budgets. For causal explanations, separate strategy, throughput, and machine variation. For task improvements, record the actual objective and hard constraints through full execution. Separate candidate-selection data from validation data not used for tuning; data repeatedly consulted to choose candidates are no longer unseen validation data.

Save state and stop the affected work when evidence confirms the objective, the budget is exhausted, no new testable direction remains, or critical input, tools, or permissions are missing. Without execution tools, provide analysis and a transferable experiment contract, label it not run, and do not claim completed autonomous optimization. Do not claim continued background work after the host stops execution; persistent execution requires host support.

Deliver the best version and recoverable location, actual comparison with the baseline, candidate decisions, runtime and failures, unresolved questions, and the stopping reason. Local evidence supports local conclusions, not inferred competition scores or global optimality. An unsuccessful optimization effort should still leave justified exclusions and a preserved reliable baseline.
