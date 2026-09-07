#!/usr/bin/env python3
"""One bounded smoke for the public SYNTHETIC diagnostic/protocol examples."""

import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

import rail_trace as tool


ROOT = Path(__file__).resolve().parents[1]


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def cli(*args, expected_code=0):
    result = subprocess.run([sys.executable, str(ROOT / "scripts/rail_trace.py"), *map(str, args)],
                            capture_output=True, text=True, encoding="utf-8", shell=False, timeout=10)
    check(result.returncode == expected_code, f"Unexpected exit {result.returncode}: {result.stderr}")
    raw = result.stdout if expected_code == 0 else result.stderr
    return json.loads(raw) if raw else None


def main():
    trace = tool.read_json(ROOT / "examples/synthetic_trace.json")
    report = tool.diagnose(trace, 1)
    check(report["first_divergence"] == {"tick": 1, "agent": "A", "field": "position", "planned": [0, 0], "actual": [0, 1]}, "First divergence")
    check(report["wait_cycles"]["total_count"] == 1 and report["wait_cycles"]["items"][0]["deadlock_proven"] is False, "Bounded wait-cycle claim")
    check(report["wait_cycles"]["items"][0]["release_hints"] == [{"agent": "A", "release_tick": 2}], "Release hint")
    check(report["conflicts"]["total_count"] == 2 and report["conflicts"]["truncated"], "Count preserved with truncation")
    check(report["coverage"]["tick_gaps"]["total_count"] == 1 and report["coverage"]["agent_disappearances"]["total_count"] == 1, "Partial coverage reported")
    check(report["comparison"]["uncompared_fields"] > 0 and report["coverage"]["agent_records_without_known_occupancy"] == 1, "Missing fields unexamined")
    unspecified = copy.deepcopy(trace)
    unspecified["semantics"]["agent_model"] = "unspecified"
    check(tool.diagnose(unspecified, 20)["conflicts"]["total_count"] == 0, "No invented collision semantics")
    for change in ("bool_tick", "bool_coordinate", "duplicate_agent", "duplicate_tick"):
        bad = copy.deepcopy(trace)
        if change == "bool_tick":
            bad["frames"][0]["tick"] = True
        elif change == "bool_coordinate":
            bad["frames"][0]["agents"][0]["position"][0] = True
        elif change == "duplicate_agent":
            bad["frames"][0]["agents"].append(bad["frames"][0]["agents"][0])
        else:
            bad["frames"][1]["tick"] = 0
        try:
            tool.validate_trace(bad)
        except tool.ToolError:
            pass
        else:
            raise AssertionError("Accepted invalid schema: " + change)
    reservations = tool.reservations(tool.read_json(ROOT / "examples/synthetic_reservations.json"), 20)
    check(reservations["duplicate_references"]["total_count"] == 1, "Duplicate reserve counts")
    check([x["kind"] for x in reservations["issues"]["items"]] == ["overlap", "overlap", "unowned_release"], "Half-open overlap and unowned release")
    check([x["matches"] for x in reservations["observations"]["items"]] == [True, True, False], "Release, rollback, observed mismatch")
    check(reservations["final_reference_count"] == 1, "Final count after rollback and release")
    no_observation = {"schema": "rail-reservations/v1", "interval": "half-open", "events": []}
    check(tool.reservations(no_observation, 20)["observed_equivalence"] == "not_checked_no_observed_snapshots", "No claimed equivalence without observations")
    with tempfile.TemporaryDirectory(prefix="synthetic-rail-smoke-") as directory:
        work = Path(directory)
        source = work / "source.json"
        source.write_text(json.dumps(trace), encoding="utf-8")
        sliced = work / "slice.json"
        cli("slice", source, "--start", 1, "--end", 1, "--output", sliced)
        recorded = tool.read_json(sliced)
        check(recorded["slice"]["selected_ticks"] == [1] and recorded["slice"]["included_ticks"] == [0, 1, 3], "Observed context retained")
        check(recorded["slice"]["complete_checkpoint"] is False, "Slice is not an executable checkpoint")
        check(cli("diagnose", source, "--output", source, expected_code=2)["error"]["code"] == "input_overwrite", "Prevent input overwrite")
        check(tool.read_json(source) == trace, "Input unchanged")
        bad = work / "bad.json"
        bad.write_text('{"schema":"wrong"}', encoding="utf-8")
        check(cli("diagnose", bad, expected_code=2)["error"]["code"] == "invalid_schema", "JSON schema error on CLI")
        manifest = ROOT / "examples/synthetic_replay.json"
        check(cli("replay", manifest, expected_code=2)["error"]["code"] == "arguments", "No implicit adapter")
        adapter = ROOT / "scripts/synthetic_rail_runner.py"
        trace_output, report_output = work / "replayed-trace.json", work / "replay-report.json"
        default_report = cli("replay", manifest, "--adapter", adapter)
        check(default_report["trace_output"] is None and "result" not in default_report and "trace" not in default_report, "Default stdout stays compact")
        summary = tool.replay_metadata({"name": "x" * 500, "engine": {"large": [1] * 500}, "extra": "y" * 500}, ("name", "engine"))
        check(len(summary["name"]) == 203 and set(summary) == {"name"}, "Adapter metadata cannot expand the report arbitrarily")
        replayed = cli("replay", manifest, "--adapter", adapter, "--trace-output", trace_output)
        check(replayed["executed"] and replayed["runner"]["is_flatland"] is False, "Real synthetic subprocess")
        check("result" not in replayed and "trace" not in replayed and replayed["frame_count"] == 4 and replayed["tick_range"] == [0, 3], "Compact report without full trace")
        check(replayed["completion"]["actions_applied"] == 3 and replayed["trace_output"] == str(trace_output.resolve()), "Completion summary and saved trace path")
        saved_trace = tool.validate_trace(tool.read_json(trace_output))
        frames = saved_trace["frames"]
        by_tick = [{a["id"]: a for a in frame["agents"]} for frame in frames]
        check(by_tick[1]["slow"]["position"] == [0, 0] and by_tick[1]["slow"]["blocked_by"] == [], "Slow motion is not definite blocking")
        check(by_tick[2]["slow"]["position"] == [0, 1] and by_tick[1]["lead"]["position"] == [0, 2] and by_tick[2]["lead"]["position"] == [0, 3], "Checkpoint phase and malfunction affect actual execution")
        check(replayed["diagnosis"]["conflicts"]["total_count"] == 0, "Synthetic execution has no recorded conflicts")
        # Existing trace plus new report also exercises the output alias guard's missing-path case.
        cli("replay", manifest, "--adapter", adapter, "--trace-output", trace_output, "--output", report_output)
        saved_report = tool.read_json(report_output)
        check(saved_report["frame_count"] == len(tool.read_json(trace_output)["frames"]) and "result" not in saved_report, "Separate report and complete trace files")
        for protected in (manifest, adapter, report_output):
            check(cli("replay", manifest, "--adapter", adapter, "--trace-output", protected, "--output", report_output, expected_code=2)["error"]["code"] == "input_overwrite", "Trace output protects input, adapter and report")
        alias = work / "report-hardlink.json"
        os.link(report_output, alias)
        check(cli("replay", manifest, "--adapter", adapter, "--trace-output", alias, "--output", report_output, expected_code=2)["error"]["code"] == "input_overwrite", "Hard-linked output aliases rejected")
        check(tool.read_json(report_output) == saved_report, "Rejected output collisions preserve report")
        sleepy = work / "synthetic_timeout_adapter.py"
        sleepy.write_text("# SYNTHETIC timeout-only smoke adapter\nimport time\ntime.sleep(2)\n", encoding="utf-8")
        check(cli("replay", manifest, "--adapter", sleepy, "--timeout", "0.05", expected_code=2)["error"]["code"] == "runner_timeout", "Actual subprocess timeout")
    print(json.dumps({"synthetic": True, "status": "passed", "checks": ["diagnosis_and_coverage", "schema_rejection", "slice_context", "reference_counts_and_rollback", "actual_adapter_execution", "input_overwrite_guard", "actual_timeout"]}))


if __name__ == "__main__":
    main()
