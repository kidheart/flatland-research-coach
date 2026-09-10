# Let actual quality results decide what to keep

[简体中文](../quality-evaluation.md) | **English**

A smoke check can answer whether an edit runs and a local fault disappears. It cannot answer whether planning quality improves. Extra reservation buffers may pass collision checks while making more trains wait. A perfect replay of the old solver's fixed actions never measures the new planner's choices. **Evidence of quality improvement requires runs in which the candidate algorithm actually makes decisions, scored by the current evaluator's real objective.**

## Three checks answer different questions

1. **Smoke: is the implementation credible?** Check the affected constraint, state transition, or repair path. Passing leads to quality evaluation; it does not finish optimization or establish success.
2. **Representative quality screen: does the objective improve, and at what cost?** Select instances exposing the diagnosed major loss, together with cases the proposed mechanism might harm. For example, a more conservative congestion policy also needs sparse-traffic delay observations. Run the candidate's own decisions and record the objective, failures/timeouts, hard constraints, and time. Choose scope according to the mechanism's reach; neither a huge suite nor one convenient instance is a universal default.
3. **Independent validation: does the selected direction survive beyond debugging instances?** After choosing a candidate, check held-back instances not used to choose it, or fresh instances. An episode-level objective needs actual episode execution. An official target requires the corresponding official evidence. When only a local screen exists, continue confirmation or identify the real missing evidence; do not relabel missing evidence as proof that no useful direction remains.

Do not repeat every layer on every edit. Reuse existing baseline results when code, input, evaluator, environment, and budget bindings match. Once a local repair passes, run a quality screen that distinguishes gains from costs; reserve independent validation resources for promising candidates. If stochastic variation affects the decision, add only the repetitions or cases that resolve that uncertainty. Keep implementation passed, screen gain, independent validation gain, and officially verified as separate states.

Compare native values for the same objective. Do not replace an official score with average completion, speed, or local wait counts merely because they are convenient. Check the actual denominators, penalties, weights, and aggregation first; keep failures instead of dropping them before averaging. Show harmed scenarios even when the total improves. When server performance falls, check the evaluated version, metric definitions, inputs, and actual failure modes first. Overfitting is one possible explanation, not a conclusion established by a screenshot of lower scores.

## Evaluate toward full marks on the current benchmark

Use the user's actual scoring rules to define full marks and the remaining gap; do not ask for a target value when none has been specified. Read available material or directly request missing current scores, detailed results, and rules. If no run exists, establish a baseline through the native entry point rather than manufacture scores from synthetic examples.

Directed parameter and combination trials follow the same quality route: screen a few meaningfully different candidates and refine useful regions. A cheap change with broad effects may go directly through the complete native suite. Do not split an inexpensive real evaluation into multiple rounds merely to satisfy a staged format.

Keep validation scoped to the specified benchmark. For a fixed public suite, freeze the candidate, rerun the full suite, and report that result. If cases informed selection, label that honestly rather than claim unseen-scenario generalization. The absence of an extra held-back set does not prohibit further optimization or obtaining official results. If the target includes hidden cases or random malfunctions, reserve relevant independent instances/run conditions to check selection bias; good proxy validation still does not prove hidden-set full marks. The actual rules determine evidence of attainment, without adding a universal cross-benchmark optimality task.

## A runnable result comparator

From the repository root:

```text
python scripts/quality_compare.py examples/synthetic_quality_baseline.json examples/synthetic_quality_candidate.json
python scripts/quality_compare.py path/to/baseline.json path/to/candidate.json --limit 8 --output quality-report.json
```

The [comparator](../../scripts/quality_compare.py) reads normalized results exported from the user's native evaluator. It does not run a solver, manufacture an official score, or replace the best version. The two included `synthetic_quality_*.json` fixtures use invented values and declarations to illustrate an aggregate gain alongside one harmed scenario. They are not executed Flatland experiments. `synthetic: true` remains visible in the report.

If an evaluator provides only a whole-run report, or its native formula cannot be represented by a `sum` or `mean` of per-instance scalars, retain that report and compare by its real formula. Do not invent instances, copy a global total into each case, average averages, or change the objective to fit this tool. The comparator is optional in that situation. Recording an unsupported native formula name as `aggregation` produces `inconclusive` with a null aggregate.

## Input: `rail-quality/v1`

Both files have the same structure. Complete examples are the [baseline](../../examples/synthetic_quality_baseline.json) and [candidate](../../examples/synthetic_quality_candidate.json).

| Field | Meaning and constraints |
| --- | --- |
| `schema` | Exactly `rail-quality/v1`. |
| `synthetic` | Required boolean: `false` for actual project results; `true` for the invented package fixtures. |
| `solver_version` | Version, commit, or content hash of the code actually executed. An old HEAD does not identify uncommitted edits. Equal versions raise a concern that no code improvement has been established. |
| `role` | `screen` or `validation`, identifying the use of this run. |
| `evidence.kind` / `evidence.reference` | `server`, `local`, or `proxy`, plus a locatable native run log/result identifier. Evidence kinds are not mixed. |
| `comparison.suite` | Identity of the instance set or selection manifest chosen before examining these outcomes. Do not remove bad cases afterward. |
| `comparison.evaluator` | Identity/version/hash of the actual evaluator, rules, and scoring definition. |
| `comparison.environment` | Bind the runner, dependencies, hardware/threads, and other conditions affecting comparability. |
| `comparison.budget` | The same resource limits on both sides: planning time, calls, threads, and the actual constraints of this task. |
| `objective` | `name` is the native objective; `direction` is `min` or `max`; `aggregation` is the native `sum` / `mean`. This tool cannot calculate other formulas. |
| `execution` | `kind` is `episode`, `planning`, or `fixed_action_replay`; boolean `solver_invoked` states whether the candidate actually made decisions. |
| `expected_cases` | Nonempty array of unique `id`, `scenario` description, and `input_fingerprint`. Fingerprints should cover maps, endpoints, malfunction/random inputs, initial state, and other inputs affecting that run. |
| `records` | One actual result per run: `id`, actual `input_fingerprint`, `status`, `objective`, `constraints_passed`, and `runtime_seconds`. Missing evidence stays missing, never fabricated as success. |
| `validation` | For validation, provide `selection: held_back` / `fresh` / `reused_for_tuning` / `unknown` and a `reference` locating the selection record. Only the first two support `validation_gain`; both sides should bind the same selection scope. |

`status` is `ok`, `failed`, or `timeout`: the solver/simulation execution completed normally, failed to execute, or reached its execution time limit. Trains still unfinished after a normally completed episode belong in the evaluator's objective/metrics; they do not automatically make execution `failed`. `objective` is finite numeric or `null`; unknown is not zero. `constraints_passed` is `true`, `false`, or `null` for unknown. `runtime_seconds` is finite and nonnegative. Booleans are not accepted as numbers. Duplicate cases, duplicate JSON keys, and invalid data are rejected.

When a failed or timed-out run has a penalty score **actually supplied by the native evaluator**, record it in `objective` and add `penalty_source` locating the native rule or run record. The tool preserves the failure status and never improves a mean by discarding failures. Without a penalty score the aggregate remains unknown. A candidate's own penalty score does not establish quality success, and its unknown constraints still block a positive verdict. If a baseline failure has a real native penalty while the candidate executes normally and passes constraints, a numeric gain from the repair can be recognized. The baseline failures and constraint concerns remain fully reported.

`fixed_action_replay` or `solver_invoked: false` never produces numeric planner-quality improvement. `planning` evidence only covers the declared planning objective; it does not automatically establish end-to-end episode quality or an official final score. Exporters must truthfully bind sources, versions, and selection records. The tool checks consistency of supplied fields; it cannot authenticate declarations or inspect the referenced external artifacts.

## Reading the output

The output is compact `rail-quality-report/v1` JSON. `--limit` is a positive integer, default 8. It limits displayed items per collection, not the calculation. Collections contain `items`, `total_count`, and `truncated`.

- `scope` identifies the evidence, role, execution kind, and comparison bindings. `comparability_blockers` explains why improvement cannot be calculated. Environment, budget, objective, case-set, fingerprint, or coverage mismatch; fixed-action replay; no solver invocation; absent scores; and unsupported aggregation all produce `aggregate: null`. Obtain valid evidence rather than treating null as a tie.
- Each side retains expected/actual counts, missing/unexpected cases, fingerprint errors, success/failure/timeout counts, constraint states, unscored count, and actual total runtime. Runtime is diagnostic information; it does not silently replace the objective.
- For complete comparable results, `aggregate` contains native sum/mean values and `signed_improvement`. **Positive always means the candidate is better.** `case_changes.regressions` lists harmed cases, largest loss first. Do not read only the aggregate.
- `screen_gain` means a numeric gain on this screen without `gain_blockers`. `validation_gain` additionally requires established independent selection declarations on both sides and non-proxy evidence. Neither establishes statistical significance, hidden-set generalization, or an official target. An aggregate gain can coexist with harmed cases; judge those tradeoffs before keeping a change.
- `regression` means the comparable aggregate became worse; `tie` means exactly equal numeric values; otherwise the result is `inconclusive`. `quality_concerns` retains both sides' failures, timeouts, and constraint concerns. Candidate failures/timeouts, failed/unknown candidate constraints, equal code versions, unestablished or inconsistent validation selection, and proxy validation are also listed in `gain_blockers`: even an aggregate gain cannot pass them. Historical baseline failures/constraint concerns do not permanently prevent recognizing a candidate repair. Missing baseline scores still prevent an aggregate, and unestablished baseline validation selection still prevents `validation_gain`.
- `decision.automatically_promoted` and `decision.official_goal_verified` are always `false`. The agent decides whether to retain a candidate using the objective, constraints, harmed cases, and native artifacts. Cite the relevant official evidence separately for official completion.

A completed comparison exits 0 even with findings or uncertainty. Argument, read, schema, or write errors exit 2 with a JSON `error` on stderr. A different chosen output file may be overwritten. Output cannot replace an input, a symlink-resolved identical path, or a hard-link alias.

`python scripts/smoke_quality_compare.py` checks only this comparator's arithmetic and rejection behavior. It does not execute Flatland and cannot replace the user's project quality screen or independent validation.
