#!/usr/bin/env python3
"""Compare actual, normalized evaluator results; never run or promote a solver."""

import argparse
from collections import Counter
import json
import math
from pathlib import Path
import sys


class ToolError(Exception):
    pass


def require(condition, message):
    if not condition:
        raise ToolError(message)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def number(value):
    if type(value) not in (int, float):
        return False
    try:
        return math.isfinite(value)
    except OverflowError:
        return False


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "Duplicate JSON key: " + key)
        result[key] = value
    return result


def reject_constant(value):
    raise ToolError("Non-finite JSON number: " + value)


def read_result(path):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8-sig"),
                          object_pairs_hook=unique_object, parse_constant=reject_constant)
    except (OSError, UnicodeError, ValueError) as exc:
        raise ToolError(f"Cannot read {path}: {exc}") from exc
    validate(data)
    return data


def validate(data):
    require(isinstance(data, dict), "Result must be an object")
    require(data.get("schema") == "rail-quality/v1", "Expected rail-quality/v1")
    require(nonempty(data.get("solver_version")), "solver_version must identify the actual evaluated code")
    require(type(data.get("synthetic")) is bool, "synthetic must be boolean")
    require(data.get("role") in ("screen", "validation"), "role must be screen or validation")
    evidence = data.get("evidence")
    require(isinstance(evidence, dict), "evidence must be an object")
    require(evidence.get("kind") in ("server", "local", "proxy"), "Invalid evidence.kind")
    require(nonempty(evidence.get("reference")), "evidence.reference must locate the actual run artifact")
    comparison = data.get("comparison")
    require(isinstance(comparison, dict), "comparison must be an object")
    for key in ("suite", "evaluator", "environment", "budget"):
        require(nonempty(comparison.get(key)), "comparison." + key + " is required")
    objective = data.get("objective")
    require(isinstance(objective, dict), "objective must be an object")
    require(nonempty(objective.get("name")), "objective.name is required")
    require(objective.get("direction") in ("min", "max"), "objective.direction must be min or max")
    require(nonempty(objective.get("aggregation")), "objective.aggregation is required")
    execution = data.get("execution")
    require(isinstance(execution, dict), "execution must be an object")
    require(execution.get("kind") in ("episode", "planning", "fixed_action_replay"), "Invalid execution.kind")
    require(type(execution.get("solver_invoked")) is bool, "execution.solver_invoked must be boolean")
    if "validation" in data:
        validation = data["validation"]
        require(isinstance(validation, dict), "validation must be an object")
        require(validation.get("selection") in ("held_back", "fresh", "reused_for_tuning", "unknown"),
                "Invalid validation.selection")
        require(nonempty(validation.get("reference")), "validation.reference is required")
    expected = data.get("expected_cases")
    require(isinstance(expected, list) and expected, "expected_cases must be a nonempty array")
    seen = set()
    for case in expected:
        require(isinstance(case, dict), "Expected case must be an object")
        for key in ("id", "scenario", "input_fingerprint"):
            require(nonempty(case.get(key)), "Expected case " + key + " is required")
        require(case["id"] not in seen, "Duplicate expected case: " + case["id"])
        seen.add(case["id"])
    records = data.get("records")
    require(isinstance(records, list), "records must be an array; do not drop failed runs")
    seen = set()
    for record in records:
        require(isinstance(record, dict), "Record must be an object")
        require(nonempty(record.get("id")), "Record id is required")
        require(nonempty(record.get("input_fingerprint")), "Record input_fingerprint is required")
        require(record["id"] not in seen, "Duplicate record: " + record["id"])
        seen.add(record["id"])
        require(record.get("status") in ("ok", "failed", "timeout"), "Invalid record status")
        require("objective" in record and (record["objective"] is None or number(record["objective"])),
                "Record objective must be finite numeric or null, never boolean")
        require("constraints_passed" in record and
                (record["constraints_passed"] is None or type(record["constraints_passed"]) is bool),
                "Record constraints_passed must be boolean or null")
        require(number(record.get("runtime_seconds")) and record["runtime_seconds"] >= 0,
                "Record runtime_seconds must be finite and nonnegative")
        if record["status"] != "ok" and record["objective"] is not None:
            require(nonempty(record.get("penalty_source")),
                    "A scored failure/timeout requires penalty_source identifying the native evaluator rule/artifact")


def limited(items, limit):
    return {"items": items[:limit], "total_count": len(items), "truncated": len(items) > limit}


def finite_sum(values):
    try:
        value = math.fsum(values)
        return value if math.isfinite(value) else None
    except (OverflowError, ValueError):
        return None


def inspect_side(data, limit):
    expected = {case["id"]: case for case in data["expected_cases"]}
    records = {record["id"]: record for record in data["records"]}
    missing, unexpected = sorted(expected.keys() - records.keys()), sorted(records.keys() - expected.keys())
    fingerprint_errors = sorted(case_id for case_id in expected.keys() & records.keys()
                                if expected[case_id]["input_fingerprint"] != records[case_id]["input_fingerprint"])
    statuses = Counter(record["status"] for record in records.values())
    constraints = Counter("unknown" if record["constraints_passed"] is None else
                          "passed" if record["constraints_passed"] else "failed" for record in records.values())
    problems = [{"id": record["id"], "status": record["status"],
                 "constraints_passed": record["constraints_passed"], "objective": record["objective"]}
                for record in sorted(records.values(), key=lambda item: item["id"])
                if record["status"] != "ok" or record["constraints_passed"] is not True or record["objective"] is None]
    summary = {
        "solver_version": data["solver_version"], "evidence": data["evidence"],
        "expected_count": len(expected), "record_count": len(records),
        "missing": limited(missing, limit), "unexpected": limited(unexpected, limit),
        "fingerprint_errors": limited(fingerprint_errors, limit),
        "status_counts": {key: statuses[key] for key in ("ok", "failed", "timeout")},
        "constraint_counts": {key: constraints[key] for key in ("passed", "failed", "unknown")},
        "unscored_count": sum(record["objective"] is None for record in records.values()),
        "runtime_seconds_sum": finite_sum(record["runtime_seconds"] for record in records.values()),
        "problem_records": limited(problems, limit),
    }
    return expected, records, summary


def compare(baseline, candidate, limit=8):
    validate(baseline)
    validate(candidate)
    require(type(limit) is int and limit > 0, "limit must be a positive integer")
    be, br, bs = inspect_side(baseline, limit)
    ce, cr, cs = inspect_side(candidate, limit)
    blockers = []
    for field in ("synthetic", "role"):
        if baseline[field] != candidate[field]:
            blockers.append(field + "_mismatch")
    if baseline["evidence"]["kind"] != candidate["evidence"]["kind"]:
        blockers.append("evidence_kind_mismatch")
    for field in ("suite", "evaluator", "environment", "budget"):
        if baseline["comparison"][field] != candidate["comparison"][field]:
            blockers.append("comparison_" + field + "_mismatch")
    for field in ("name", "direction", "aggregation"):
        if baseline["objective"][field] != candidate["objective"][field]:
            blockers.append("objective_" + field + "_mismatch")
    if baseline["execution"]["kind"] != candidate["execution"]["kind"]:
        blockers.append("execution_kind_mismatch")
    if baseline["objective"]["aggregation"] not in ("sum", "mean"):
        blockers.append("unsupported_native_aggregation")
    if set(be) != set(ce):
        blockers.append("expected_case_set_mismatch")
    mismatched_cases = sorted(case_id for case_id in be.keys() & ce.keys()
                              if any(be[case_id][key] != ce[case_id][key] for key in ("scenario", "input_fingerprint")))
    if mismatched_cases:
        blockers.append("expected_case_binding_mismatch")
    for side, data, summary in (("baseline", baseline, bs), ("candidate", candidate, cs)):
        if data["execution"]["kind"] == "fixed_action_replay" or not data["execution"]["solver_invoked"]:
            blockers.append(side + "_did_not_evaluate_candidate_solver")
        for field in ("missing", "unexpected", "fingerprint_errors"):
            if summary[field]["total_count"]:
                blockers.append(side + "_" + field)
        if summary["unscored_count"]:
            blockers.append(side + "_unscored_records")

    concerns, gain_blockers = [], []

    def concern(code, prevents_gain=True):
        concerns.append(code)
        if prevents_gain:
            gain_blockers.append(code)

    for side, summary in (("baseline", bs), ("candidate", cs)):
        for status in ("failed", "timeout"):
            if summary["status_counts"][status]:
                concern(side + "_" + status + "_records", prevents_gain=side == "candidate")
        for state in ("failed", "unknown"):
            if summary["constraint_counts"][state]:
                concern(side + "_constraints_" + state, prevents_gain=side == "candidate")
    if baseline["solver_version"] == candidate["solver_version"]:
        concern("same_solver_version_no_code_change_established")
    if candidate["role"] == "validation":
        for side, data in (("baseline", baseline), ("candidate", candidate)):
            if data.get("validation", {}).get("selection") not in ("held_back", "fresh"):
                concern(side + "_validation_selection_unestablished")
        if baseline.get("validation") != candidate.get("validation"):
            concern("validation_selection_binding_mismatch")
        if candidate["evidence"]["kind"] == "proxy":
            concern("proxy_cannot_establish_validation_gain")

    aggregate = None
    regressions = []
    gains = ties = 0
    if not blockers:
        values = [finite_sum(records[case_id]["objective"] for case_id in sorted(be)) for records in (br, cr)]
        if None in values:
            blockers.append("aggregate_arithmetic_not_finite")
        else:
            if baseline["objective"]["aggregation"] == "mean":
                values = [value / len(be) for value in values]
            sign = 1 if baseline["objective"]["direction"] == "max" else -1
            delta = sign * (values[1] - values[0])
            deltas = [(case_id, sign * (cr[case_id]["objective"] - br[case_id]["objective"])) for case_id in sorted(be)]
            if not number(delta) or not all(number(value) for _, value in deltas):
                blockers.append("difference_arithmetic_not_finite")
            else:
                aggregate = {"baseline": values[0], "candidate": values[1],
                             "signed_improvement": delta, "positive_means": "candidate_better", "case_count": len(be)}
                for case_id, change in deltas:
                    if change < 0:
                        regressions.append({"id": case_id, "scenario": be[case_id]["scenario"],
                                            "baseline": br[case_id]["objective"], "candidate": cr[case_id]["objective"],
                                            "signed_improvement": change})
                    elif change > 0:
                        gains += 1
                    else:
                        ties += 1
                regressions.sort(key=lambda item: (item["signed_improvement"], item["id"]))
    verdict = "inconclusive"
    if aggregate is not None:
        delta = aggregate["signed_improvement"]
        if delta < 0:
            verdict = "regression"
        elif not gain_blockers:
            verdict = "tie" if delta == 0 else candidate["role"] + "_gain"
    return {
        "schema": "rail-quality-report/v1", "verdict": verdict,
        "scope": {"synthetic": candidate["synthetic"], "role": candidate["role"],
                  "evidence_kind": candidate["evidence"]["kind"], "execution_kind": candidate["execution"]["kind"],
                  "comparison": candidate["comparison"], "objective": candidate["objective"],
                  "validation": candidate.get("validation"), "bindings_are_caller_supplied": True},
        "comparability_blockers": limited(blockers, limit), "quality_concerns": limited(concerns, limit),
        "gain_blockers": limited(gain_blockers, limit),
        "mismatched_cases": limited(mismatched_cases, limit),
        "baseline": bs, "candidate": cs, "aggregate": aggregate,
        "case_changes": {"gains": gains if aggregate is not None else None,
                         "ties": ties if aggregate is not None else None, "regressions": limited(regressions, limit)},
        "decision": {"automatically_promoted": False, "official_goal_verified": False,
                     "claim": "Measured scope only; inspect regressions and native artifacts before retaining a candidate."},
    }


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise ToolError(message)


def main(argv=None):
    parser = Parser(description=__doc__)
    parser.add_argument("baseline")
    parser.add_argument("candidate")
    parser.add_argument("--limit", type=int, default=8, help="displayed items per collection (default: 8)")
    parser.add_argument("--output", help="write compact JSON report here instead of stdout")
    try:
        args = parser.parse_args(argv)
        require(args.limit > 0, "--limit must be positive")
        inputs = [Path(args.baseline), Path(args.candidate)]
        if args.output:
            output = Path(args.output)
            for input_path in inputs:
                require(output.resolve() != input_path.resolve() and
                        not (output.exists() and input_path.exists() and output.samefile(input_path)),
                        "Output must not overwrite either input, including a hard-link alias")
        result = compare(read_result(inputs[0]), read_result(inputs[1]), args.limit)
        encoded = json.dumps(result, ensure_ascii=False, allow_nan=False, separators=(",", ":")) + "\n"
        if args.output:
            Path(args.output).write_text(encoded, encoding="utf-8")
        else:
            print(encoded, end="")
        return 0
    except (ToolError, OSError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
