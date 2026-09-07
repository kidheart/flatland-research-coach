# Small evidence tools

[简体中文](../tooling.md) | **English**

These stdlib Python tools inspect evidence supplied by the current user. They do not depend on a Flatland release or contain an original author's solver, settings, traces, or benchmark results. Every included fixture and the demonstration runner is **synthetic**, invented for this package. Python 3.9 or later is required.

From the repository root, choose the relevant command; these are not a required sequence:

```text
python scripts/rail_trace.py diagnose examples/synthetic_trace.json --limit 20
python scripts/rail_trace.py slice examples/synthetic_trace.json --start 1 --end 1 --context 1 --output trace-slice.json
python scripts/rail_trace.py replay examples/synthetic_replay.json --adapter scripts/synthetic_rail_runner.py --timeout 10 --trace-output replay-trace.json
python scripts/rail_trace.py reservations examples/synthetic_reservations.json
python scripts/smoke_rail_trace.py
```

All four commands accept `--output PATH`; otherwise JSON goes to stdout. Reports use compact JSON. Replay reports omit the full trace; optional `--trace-output PATH` saves it separately for later `slice` or `diagnose`. Report collections include `items`, `total_count`, and `truncated`; `--limit` bounds displayed items per collection and does not stop examination of the input or truncate a saved trace. A report containing findings still exits 0. Argument, input/schema, output, adapter failure, and actual subprocess timeout errors exit 2 with a JSON `error` on stderr. `--help` prints ordinary CLI help. No report or trace file is written before validation and execution succeed. An output path resolving to the input, adapter, or other output, including an existing hard-link alias, is rejected. Different existing output files are replaced.

## Normalized trace: `rail-trace/v1`

The smallest useful invented trace is:

```json
{
  "schema": "rail-trace/v1",
  "synthetic": true,
  "semantics": {"agent_model": "point", "vertex": "exclusive", "edge_swap": "forbidden"},
  "frames": [
    {"tick": 0, "agents": [
      {"id": "A", "position": [0, 0], "direction": 1, "occupies": true,
       "planned": {"position": [0, 0]}}
    ]}
  ]
}
```

Ticks are nonnegative integers, strictly increasing, with no duplicate frames. Each frame has an `agents` array with unique nonempty string IDs. Integer fields reject booleans. A position, when present, is `[row, column]` with two integers or `null`; direction is `0..3` or `null`. An explicit `occupies` is boolean. `occupies: true` together with `position: null` is contradictory and rejected. Missing state fields are accepted as incomplete evidence. `null` is an explicit recorded value, not a substitute for an unknown field; omit unknown fields.

`planned` contains any of `position`, `direction`, and `occupies`, expressed **at the same tick** as the observed agent record. Only fields present on both sides are compared. Missing plan or actual fields increase `comparison.uncompared_fields`; lack of a mismatch is not complete agreement. The earliest compared mismatch is `first_divergence`, ordered by tick, then agent ID, then position/direction/occupies. With an incomplete earlier record, this means the first **recorded comparable** divergence.

Optional `blocked_by: ["B"]` records an explicit wait dependency supplied by the runner at that tick. It must not be manufactured from unchanged positions. Optional `release_tick` is a nonnegative integer supplied when a release time is actually known and visible to the decision maker; it is reported as an unverified hint. `status`, `malfunction`, and other metadata may be retained, but this tool does not interpret them or infer release conditions. Missing `blocked_by` is unknown dependency evidence; an empty array records no listed dependency at that tick.

`semantics` must declare each of:

| Field | Accepted values | Effect |
| --- | --- | --- |
| `agent_model` | `point`, `unspecified` | Collision checks require `point`. |
| `vertex` | `exclusive`, `allowed`, `unspecified` | Shared recorded positions are reported only with `exclusive`. |
| `edge_swap` | `forbidden`, `allowed`, `unspecified` | Reversed recorded endpoints are reported only with `forbidden`. |

`diagnose` can establish these bounded observations:

- A first recorded plan/actual mismatch for a compared field.
- A cyclic strongly connected component in the **same-tick explicit** `blocked_by` graph, its recorded edges, and available `release_hints`. The result explicitly sets `deadlock_proven: false`. No hint does not mean a dependency will never release. Check runner events, malfunction visibility, resource ownership, and reachable future release conditions before calling a cycle a deadlock.
- A shared vertex under declared exclusive point occupancy, using only `occupies: true` plus a known position.
- A reversed endpoint pair over consecutive integer ticks, when both agents explicitly occupy their positions at both endpoints and point swaps are forbidden. This is an endpoint check, not a proof that the recorded segment is a legal rail transition. It does not check swept footprints, intermediate cells, fractional movement, longer trains, or all possible track conflicts.

The coverage report records gaps, previously recorded agents missing from the next frame, unresolved blocker IDs, and unknown occupancy. A missing agent is **unrecorded**, never inferred to have exited or finished. Entirely absent agents cannot be counted without an external roster. No duration, delay, lost score, or throughput loss is derived from unchanged position: a slow train may still be moving within a cell. No conflicts found means no conflicts found in the checks actually enabled and recorded.

## Record slice, not state reconstruction

`slice` selects recorded frames within inclusive `--start` and `--end`. It retains `--context` observed frames on each side, default 1, including their full agent metadata and semantics. An interval with no recorded frame is rejected. The `slice` metadata distinguishes `selected_ticks` from `included_ticks`; diagnose on that file includes the context frames too. `--context 0` deliberately omits surrounding evidence.

This command does not run a simulation. Context may itself be sparse, and starting mid-run does not supply a complete initial state. Positions and directions alone cannot reconstruct a Flatland checkpoint, motion progress, random state, pending malfunctions, departures, or wrapper state. The slice explicitly records `is_simulation: false` and `complete_checkpoint: false`.

## Actual adapter execution

`replay` requires the current user to explicitly select a Python executable file with `--adapter`; it never discovers or executes code named by the JSON data. It calls `[sys.executable, adapter_path]` with `shell=False`, passes one JSON manifest on stdin, captures stdout, and enforces `--timeout` through `subprocess.run(timeout=...)`. This is ordinary local Python execution, not a sandbox. The adapter must finish its replay synchronously and must not launch background workers that outlive the call; the timeout terminates the selected process, not an arbitrary descendant process tree. Adapter diagnostics should use stderr; nonzero exit is reported without echoing potentially private diagnostic text.

The manifest envelope is:

```json
{
  "schema": "rail-replay/v1",
  "synthetic": true,
  "clock": {"start_tick": 0, "action_timing": "before_step"},
  "runner_requirements": {"engine": "synthetic-line/v1"},
  "checkpoint": {"adapter_defined": "complete initial state goes here"},
  "actions": []
}
```

This block shows envelope structure only; its placeholder checkpoint is deliberately not runnable. The executable fixture is [`examples/synthetic_replay.json`](../../examples/synthetic_replay.json). `clock`, `runner_requirements`, and `checkpoint` must be nonempty objects, `clock.start_tick` a nonnegative integer, `clock.action_timing` a nonempty string, and `actions` an array. The adapter validates the engine/version, checkpoint contents, action schedule, and any project-specific fields it needs. The tool cannot infer whether an arbitrary project's checkpoint is sufficient.

Successful **adapter** stdout must be exactly one JSON object:

```text
{"schema":"rail-replay-result/v1","trace":<valid rail-trace/v1>, ...optional metadata...}
```

The trace must include the initial checkpoint frame at `clock.start_tick`. The tool validates it and emits a compact `rail-replay-report/v1`: actual adapter path, execution flag, frame count, tick range, selected runner/completion scalar fields, and diagnosis. Runner fields are limited to `engine`, `version`, `name`, `is_flatland`, and `synthetic`; completion fields to `actions_applied`, `final_tick`, and `status`. Strings are capped at 200 characters, integers at 20 digits including a minus sign, and arbitrary nested metadata is omitted. Neither the full adapter result nor its trace is echoed into the report.

Use `--trace-output replay-trace.json` to retain the full validated `rail-trace/v1` object, including all frames and trace metadata. `--output replay-report.json` independently saves the compact report. Its `trace_output` is the resolved saved path, or `null` when no trace file was requested. The saved trace can be passed directly to `slice` or `diagnose`; the report is not a trace. These two output paths must be distinct from each other, the manifest, and the adapter, including aliases.

Successful execution establishes that this adapter returned that trace; it does not establish Flatland fidelity, agreement with another runner, or benchmark performance. Without an adapter and the state its runner requires, use record slicing and report the missing replay prerequisites.

The provided [`synthetic_rail_runner.py`](../../scripts/synthetic_rail_runner.py) really executes this protocol. Its invented `synthetic-line/v1` world is a single horizontal track, point agents directed east (`1`) or west (`3`), explicit `go`/`hold` actions, integer motion phases, and an initial malfunction countdown. Occupied destinations at the beginning of a step block entry even if the occupant moves during that step; competing proposals into one free cell also block. Every agent stays present, including at a boundary. Motion phase and malfunction countdown are included in its checkpoint. It neither imports Flatland nor implements the original author's solver. Its narrow rules demonstrate why an unmoved cell alone does not prove waiting.

## Reservation event audit: `rail-reservations/v1`

Input has `schema: "rail-reservations/v1"`, `interval: "half-open"`, and an `events` array. The initially empty table is replayed in array order; no time advancement, implicit expiration, or hidden project state is inferred. Resource strings are opaque and must already encode the project's intended conflict resource.

| Operation | Required fields | Meaning |
| --- | --- | --- |
| `reserve` | `owner`, `resource`, `start`, `end` | Increment one reference for this exact key. |
| `release` | `owner`, `resource`, `start`, `end` | Decrement one exact-key reference; remove it at zero. |
| `checkpoint` | unique `name` | Save the full table including counts. |
| `rollback` | `name` | Restore that saved table and its counts. |
| `observed` | `entries` | Compare a supplied snapshot to the current replayed table without changing it. |

Every event includes `op`. Owners and resources are nonempty strings. Bounds are integers with `0 <= start < end`; intervals are `[start, end)`, so `[0, 2)` and `[2, 3)` do not overlap. Observed entries require the same key fields plus positive integer `count`, with no duplicate keys. A complete snapshot of the audited resource scope is needed for meaningful comparison; the format does not represent a partial observed snapshot.

Repeated reservation of the same owner/resource/interval is represented as reference counting and reported under `duplicate_references`; it is not automatically a bug. Releasing a key not owned reports `unowned_release` without mutating the table. Overlap reports require different owners on the same resource with overlapping intervals; overlapping reserves remain represented so the event history can be audited. Same-owner overlap is not reported as a cross-agent conflict. Unknown rollback names are reported without changing state. Duplicate checkpoint names are rejected; successful checkpoints remain independent saved snapshots after any rollback.

`observed_equivalence` distinguishes matching supplied snapshots, a supplied mismatch, and `not_checked_no_observed_snapshots`. Even matching observations establish equality only for the normalized table and observation points supplied. Missing observations cannot establish equivalence with an actual project. An event-stream audit is not by itself proof that an incremental reservation implementation matches a full rebuild or that a schedule is safe.

## Adapting the current user's project

Keep conversion explicit and small. First align the runner's decision tick, action submission, post-step observation, and the plan's expected tick. Export row/column and direction consistently with current topology rules. Declare what `occupies` means for off-grid agents, fractional movement, waiting departures, malfunctioned agents, and completed agents still on or removed from the track. Choose point collision checks only when they apply; retain richer footprint/transition validation in the project adapter when needed.

Export `blocked_by` from actual decision or simulator events, and distinguish what malfunction/release information was available at decision time from hindsight. Do not infer an unknown release time. A replay adapter should restore topology, full per-agent motion state and status, clock, random state, failure schedules or event source, wrapper state, and any other engine requirements before applying the supplied actions. It should validate these prerequisites and fail clearly when absent. Preserve the information available to the original decision maker if replaying a planning decision, and document any deliberately supplied hindsight.

For reservation audits, use the same interval convention and resource identity on the event and observed sides. If comparing an incremental table with a rebuild, export observed snapshots independently from the actual implementation at relevant checkpoint/rollback boundaries. The examples provide a protocol and an audit shape; project-specific conversion, solver improvements, and performance claims still require the user's evidence.

The single smoke script checks concrete divergence, cycle limits, sparse coverage, semantic gating, bad schemas, retained slice context, duplicate reference counts, half-open overlaps, invalid release, rollback and snapshot mismatch, actual runner movement/malfunction behavior, compact replay reports with recoverable complete traces, input/output overwrite rejection including hard links, and an actual timeout. It uses synthetic inputs and temporary files, not benchmark sweeps or A/B runs.
