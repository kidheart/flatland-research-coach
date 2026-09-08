#!/usr/bin/env python3
"""Targeted checks for the comparator; this does not benchmark a Flatland solver."""

import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from quality_compare import ToolError, compare, read_result, validate


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "scripts" / "quality_compare.py"
BASE = read_result(ROOT / "examples" / "synthetic_quality_baseline.json")
CAND = read_result(ROOT / "examples" / "synthetic_quality_candidate.json")


def pair():
    return copy.deepcopy(BASE), copy.deepcopy(CAND)


def expect_invalid(value):
    try:
        validate(value)
    except ToolError:
        return
    raise AssertionError("Invalid input was accepted")


def main():
    checks = 0
    report = compare(BASE, CAND)
    assert report["verdict"] == "screen_gain"
    assert report["aggregate"] == {"baseline": 100.0, "candidate": 80.0,
                                   "signed_improvement": 20.0, "positive_means": "candidate_better", "case_count": 3}
    assert report["case_changes"]["regressions"]["items"][0]["id"] == "easy"
    assert report["case_changes"]["regressions"]["items"][0]["signed_improvement"] == -10
    assert report["candidate"]["runtime_seconds_sum"] == 6
    assert report["decision"]["automatically_promoted"] is False
    assert report["decision"]["official_goal_verified"] is False
    checks += 1

    a, b = pair()
    for item in (a, b):
        item["objective"]["aggregation"] = "mean"
    report = compare(a, b)
    assert abs(report["aggregate"]["candidate"] - 80 / 3) < 1e-12
    assert abs(report["aggregate"]["signed_improvement"] - 20 / 3) < 1e-12
    for item in (a, b):
        item["objective"]["direction"] = "max"
    assert compare(a, b)["verdict"] == "regression"
    checks += 1

    for path, value in ((('comparison', 'suite'), "other-suite"),
                        (('comparison', 'evaluator'), "other-evaluator"),
                        (('comparison', 'environment'), "other-environment"),
                        (('comparison', 'budget'), "larger-budget"),
                        (('objective', 'name'), "different-metric"),
                        (('objective', 'aggregation'), "mean"),
                        (('evidence', 'kind'), "server"),
                        (('execution', 'kind'), "planning")):
        a, b = pair()
        b[path[0]][path[1]] = value
        report = compare(a, b)
        assert report["verdict"] == "inconclusive" and report["aggregate"] is None
        checks += 1

    a, b = pair()
    for item in (a, b):
        item["objective"]["aggregation"] = "native-weighted-composite"
    assert compare(a, b)["aggregate"] is None
    checks += 1

    for change in ("missing", "unexpected", "expected_fingerprint", "record_fingerprint", "scenario", "unscored"):
        a, b = pair()
        if change == "missing":
            b["records"].pop()
        elif change == "unexpected":
            extra = copy.deepcopy(b["records"][0])
            extra["id"] = "unplanned-case"
            b["records"].append(extra)
        elif change == "expected_fingerprint":
            b["expected_cases"][0]["input_fingerprint"] = "changed-input"
            b["records"][0]["input_fingerprint"] = "changed-input"
        elif change == "record_fingerprint":
            b["records"][0]["input_fingerprint"] = "wrong-input"
        elif change == "scenario":
            b["expected_cases"][0]["scenario"] = "changed-scenario"
        else:
            b["records"][0]["objective"] = None
        report = compare(a, b)
        assert report["verdict"] == "inconclusive" and report["aggregate"] is None
        if change == "missing":
            assert report["candidate"]["missing"]["items"] == ["easy"]
        checks += 1

    for status in ("failed", "timeout"):
        a, b = pair()
        b["records"][0]["status"] = status
        b["records"][0]["objective"] = None
        report = compare(a, b)
        assert report["aggregate"] is None and report["candidate"]["status_counts"][status] == 1
        b["records"][0]["objective"] = 40
        expect_invalid(b)
        b["records"][0]["penalty_source"] = "invented-native-penalty-rule"
        report = compare(a, b)
        assert report["aggregate"]["signed_improvement"] == 20
        assert report["verdict"] == "inconclusive"
        assert report["candidate"]["problem_records"]["items"][0]["status"] == status
        checks += 1

    for value in (False, None):
        a, b = pair()
        b["records"][0]["constraints_passed"] = value
        assert compare(a, b)["verdict"] == "inconclusive"
        checks += 1

    for constraint in (False, None):
        a, b = pair()
        a["records"][0].update(status="failed", objective=200, constraints_passed=constraint,
                                penalty_source="invented-native-failure-penalty")
        report = compare(a, b)
        assert report["verdict"] == "screen_gain"
        assert report["aggregate"]["signed_improvement"] == 160
        assert report["baseline"]["status_counts"]["failed"] == 1
        assert "baseline_failed_records" in report["quality_concerns"]["items"]
        assert report["gain_blockers"]["total_count"] == 0
        b["records"][0].update(status="failed", penalty_source="invented-native-failure-penalty")
        report = compare(a, b)
        assert report["verdict"] == "inconclusive"
        assert "candidate_failed_records" in report["gain_blockers"]["items"]
        b["records"][0]["status"] = "ok"
        a["records"][0]["objective"] = None
        report = compare(a, b)
        assert report["verdict"] == "inconclusive" and report["aggregate"] is None
        assert "baseline_unscored_records" in report["comparability_blockers"]["items"]
        checks += 1

    a, b = pair()
    for item in (a, b):
        item["role"] = "validation"
    assert compare(a, b)["verdict"] == "inconclusive"
    for item in (a, b):
        item["validation"] = {"selection": "held_back", "reference": "invented-selection-record-v1"}
    assert compare(a, b)["verdict"] == "validation_gain"
    a["validation"]["selection"] = "unknown"
    report = compare(a, b)
    assert report["verdict"] == "inconclusive"
    assert "baseline_validation_selection_unestablished" in report["gain_blockers"]["items"]
    a["validation"]["selection"] = "held_back"
    b["validation"]["selection"] = "reused_for_tuning"
    assert compare(a, b)["verdict"] == "inconclusive"
    for item in (a, b):
        item["validation"]["selection"] = "fresh"
        item["evidence"]["kind"] = "proxy"
    assert compare(a, b)["verdict"] == "inconclusive"
    checks += 1

    for execution in ({"kind": "fixed_action_replay", "solver_invoked": True},
                      {"kind": "episode", "solver_invoked": False}):
        a, b = pair()
        a["execution"] = b["execution"] = execution
        report = compare(a, b)
        assert report["aggregate"] is None and report["verdict"] == "inconclusive"
        checks += 1

    a, b = pair()
    b["records"][0]["objective"] = 10
    b["records"][1]["objective"] = 40
    report = compare(a, b, limit=1)
    assert report["aggregate"]["signed_improvement"] == 30
    assert report["case_changes"]["regressions"]["total_count"] == 2
    assert report["case_changes"]["regressions"]["truncated"] is True
    assert len(report["case_changes"]["regressions"]["items"]) == 1
    checks += 1

    for field, value in (("objective", True), ("objective", float("inf")),
                         ("runtime_seconds", True), ("runtime_seconds", -1),
                         ("constraints_passed", 1)):
        _, b = pair()
        b["records"][0][field] = value
        expect_invalid(b)
        checks += 1
    _, b = pair()
    b["records"].append(copy.deepcopy(b["records"][0]))
    expect_invalid(b)
    _, b = pair()
    b["expected_cases"].append(copy.deepcopy(b["expected_cases"][0]))
    expect_invalid(b)
    checks += 1

    with tempfile.TemporaryDirectory(prefix="rail-quality-smoke-") as temporary:
        work = Path(temporary)
        first, second, output = work / "baseline.json", work / "candidate.json", work / "report.json"
        first.write_text(json.dumps(BASE), encoding="utf-8")
        second.write_text(json.dumps(CAND), encoding="utf-8")
        original = first.read_bytes()
        command = [sys.executable, str(TOOL), str(first), str(second)]
        run = subprocess.run(command + ["--output", str(output)], capture_output=True, text=True, timeout=5)
        assert run.returncode == 0 and not run.stdout and json.loads(output.read_text(encoding="utf-8"))["verdict"] == "screen_gain"
        for target in (first, second):
            run = subprocess.run(command + ["--output", str(target)], capture_output=True, text=True, timeout=5)
            assert run.returncode == 2 and "overwrite" in json.loads(run.stderr)["error"]
        alias = work / "alias.json"
        os.link(first, alias)
        run = subprocess.run(command + ["--output", str(alias)], capture_output=True, text=True, timeout=5)
        assert run.returncode == 2 and first.read_bytes() == original
        for raw in ('{"schema":"rail-quality/v1","schema":"other"}',
                    json.dumps(CAND).replace('"objective": 40', '"objective": 1e999')):
            second.write_text(raw, encoding="utf-8")
            run = subprocess.run(command, capture_output=True, text=True, timeout=5)
            assert run.returncode == 2 and "error" in json.loads(run.stderr)
        checks += 1

    print(json.dumps({"status": "PASS", "targeted_checks": checks,
                      "scope": "Comparator behavior with invented fixtures; no Flatland quality result"}))


if __name__ == "__main__":
    main()
