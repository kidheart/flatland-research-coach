# Experiment record: objective, mechanism, and measured quality

[简体中文](../experiment-card.md) | **English**

Reuse the user's existing records. Keep decisions short by default and expand only for complex mechanisms or difficult results; do not require a report every round. In autonomous mode the agent records its own judgments. Interactive mode may invite the user's explanation first, without impersonating their views.

## Default short record

~~~text
Objective and gap: <primary metric, direction, target; best verified value and evidence level; remaining problem>
Mechanism and change: <observation separate from explanation; user file/function and candidate version; decision to change>
Checks and quality: <smoke result; actual candidate-solver evaluation, baseline/candidate primary metrics, major regressions and resources>
Promotion evidence: <development/screening/independent validation/authoritative result; completed, failed, missing or timed out; unverified parts>
Decision and next step: <candidate/best locations by evidence level; acceptance or rejection; next mechanism or specific pause condition>
~~~

Write “not measured” when the primary metric is unavailable, not zero. Write “not obtained” for missing authoritative results. Do not subtract values from different evidence levels, conditions, or objectives. Reference an existing record that answers a field instead of copying raw output.

**A smoke pass cannot complete acceptance of a quality optimization.** See [quality evaluation](quality-evaluation.md) and the [execution workflow](autonomous-research.md) for comparison and promotion requirements. A narrowly scoped repair may report “tested failure fixed; overall quality not evaluated.” If the overall task still has a quality target, continue with the remaining gap.

## Before implementation: turn a mechanism into a distinguishing prediction

When expansion helps, add only fields needed for the current decision:

~~~text
Relevant objective, hard constraints, and actual evaluation rules:
Baseline/best locations, results, and conditions for reuse:
Main remaining loss and supporting code, trace, or per-case evidence:
Current mechanism explanation and evidence that would contradict it:
Decision to change, scope, and what stays fixed:
Why representative evaluation covers expected gains and possible costs:
Acceptance criteria and evidence needed for promotion at each relevant level:
Known run cost, actual resource limits, and timeout:
~~~

Consult the [algorithm playbook](algorithm-playbook.md) for mechanisms and [real cases](reasoning-cases.md) for related experience. These support predictions, not results for the current user. A simple implementation error needs no invented competing hypothesis. A legal but low-quality solver need not contain a bug to justify algorithmic improvement.

## After running: retain comparable facts

~~~text
Actual code/configuration, inputs, environment, entry point, and resource conditions:
Whether the candidate solver actually made planning/repair decisions:
Expected cases and completed cases; missing results, failures, timeouts:
Primary metric and key constraints; per-case gains and major regressions:
Validity of the baseline comparison; resource cost and run variation:
Whether data supported development, screening, or validation untouched by selection:
Authoritative target result, or a note that it was not obtained:
What observations support and cannot establish; candidate decision:
~~~

Do not retain only successful or improved cases. Fixed-action replay does not automatically establish a new planning policy's benefit, and estimated plan quality does not automatically establish execution quality. Reuse baselines only under matching conditions; otherwise obtain the needed comparison rather than borrowing unrelated evidence.

When gains approach variation, use a bounded comparison that determines acceptance or retain an unconfirmed candidate; do not expand into an aimless matrix. When quality fails to improve or authoritative results decline, first record the measured regression and unknown cause. Do not assert overfitting without evidence. Preserve the preceding best version; a local candidate cannot replace the authoritative best.

## Updating the direction and ending a stage

Keep a short account of **remaining loss → tried mechanisms and results → other feasible directions → next evidence or missing condition**. After rejecting a candidate, update the explanation and select another mechanism; one failed attempt does not end the whole task. For a pause, use the [stopping rules](autonomous-research.md) to state the specific condition and what resumption needs.

Conclude whether the primary target has corresponding evidence, which reliable versions remain, which mechanisms succeeded or failed, and within what scope. State when the target remains unmet; do not claim universal optimality or guarantee success. Share only authorized material; the source author's code, parameters, commit identifiers, and winning combination are unnecessary.
