#!/usr/bin/env python3
"""Small, stdlib-only diagnostics for explicitly normalized railway evidence."""

import argparse
from collections import Counter
import copy
import json
from pathlib import Path
import subprocess
import sys


class ToolError(Exception):
    def __init__(self, code, message):
        self.code, self.message = code, message
        super().__init__(message)


def require(condition, message):
    if not condition:
        raise ToolError("invalid_schema", message)


def integer(value):
    return type(value) is int


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def reject_constant(value):
    raise ValueError("Non-finite JSON number: " + value)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON object key: " + key)
        result[key] = value
    return result


def parse_json(raw, label):
    try:
        return json.loads(raw, parse_constant=reject_constant, object_pairs_hook=unique_object)
    except (ValueError, UnicodeError) as exc:
        raise ToolError("invalid_json", f"{label}: {exc}") from exc


def read_json(path):
    try:
        return parse_json(Path(path).read_text(encoding="utf-8-sig"), str(path))
    except OSError as exc:
        raise ToolError("read_error", str(exc)) from exc


def state_fields(state, label):
    require(isinstance(state, dict), f"{label} must be an object")
    if "position" in state:
        pos = state["position"]
        require(pos is None or (isinstance(pos, list) and len(pos) == 2
                and all(integer(x) for x in pos)), f"{label}.position must be [int,int] or null")
    if "direction" in state:
        direction = state["direction"]
        require(direction is None or (integer(direction) and 0 <= direction <= 3),
                f"{label}.direction must be 0..3 or null")
    if "occupies" in state:
        require(type(state["occupies"]) is bool, f"{label}.occupies must be boolean")
        if state["occupies"] and "position" in state:
            require(state["position"] is not None, f"{label}: occupies=true contradicts null position")


def validate_trace(data):
    require(isinstance(data, dict) and data.get("schema") == "rail-trace/v1",
            "Expected schema rail-trace/v1")
    semantics = data.get("semantics")
    require(isinstance(semantics, dict), "semantics must be an object")
    for key, choices in (("agent_model", ("point", "unspecified")),
                         ("vertex", ("exclusive", "allowed", "unspecified")),
                         ("edge_swap", ("forbidden", "allowed", "unspecified"))):
        require(semantics.get(key) in choices, f"semantics.{key} must be one of {choices}")
    frames = data.get("frames")
    require(isinstance(frames, list), "frames must be an array")
    previous = None
    for index, frame in enumerate(frames):
        label = f"frames[{index}]"
        require(isinstance(frame, dict), f"{label} must be an object")
        tick = frame.get("tick")
        require(integer(tick) and tick >= 0, f"{label}.tick must be a nonnegative integer")
        require(previous is None or tick > previous, "Frame ticks must be strictly increasing")
        previous = tick
        agents = frame.get("agents")
        require(isinstance(agents, list), f"{label}.agents must be an array")
        seen = set()
        for agent in agents:
            state_fields(agent, label + ".agent")
            aid = agent.get("id")
            require(nonempty(aid), f"{label}: agent id must be a nonempty string")
            require(aid not in seen, f"{label}: duplicate agent id {aid}")
            seen.add(aid)
            if "planned" in agent:
                state_fields(agent["planned"], f"{label}.{aid}.planned")
            if "blocked_by" in agent:
                blockers = agent["blocked_by"]
                require(isinstance(blockers, list) and all(nonempty(x) for x in blockers),
                        f"{label}.{aid}.blocked_by must be an array of ids")
                require(len(set(blockers)) == len(blockers), f"{label}.{aid}: duplicate blocker")
            if "release_tick" in agent:
                require(integer(agent["release_tick"]) and agent["release_tick"] >= 0,
                        f"{label}.{aid}.release_tick must be a nonnegative integer")
    return data


def bounded(items, limit):
    return {"items": items[:limit], "total_count": len(items), "truncated": len(items) > limit}


def cyclic_components(graph):
    """Iterative Kosaraju; absent agents have no inferred outgoing edges."""
    nodes = set(graph)
    nodes.update(v for edges in graph.values() for v in edges)
    visited, order = set(), []
    for start in sorted(nodes):
        if start in visited:
            continue
        visited.add(start)
        stack = [(start, iter(sorted(graph.get(start, []))))]
        while stack:
            node, edges = stack[-1]
            nxt = next(edges, None)
            if nxt is None:
                order.append(node)
                stack.pop()
            elif nxt not in visited:
                visited.add(nxt)
                stack.append((nxt, iter(sorted(graph.get(nxt, [])))))
    reverse = {node: [] for node in nodes}
    for node, edges in graph.items():
        for target in edges:
            reverse[target].append(node)
    visited, components = set(), []
    for start in reversed(order):
        if start in visited:
            continue
        component, stack = [], [start]
        visited.add(start)
        while stack:
            node = stack.pop()
            component.append(node)
            for nxt in reverse[node]:
                if nxt not in visited:
                    visited.add(nxt)
                    stack.append(nxt)
        if len(component) > 1 or start in graph.get(start, []):
            components.append(sorted(component))
    return sorted(components)


def occupied(agent):
    return agent.get("occupies") is True and agent.get("position") is not None


def diagnose(data, limit):
    validate_trace(data)
    semantics = data["semantics"]
    vertex_enabled = semantics["agent_model"] == "point" and semantics["vertex"] == "exclusive"
    swap_enabled = semantics["agent_model"] == "point" and semantics["edge_swap"] == "forbidden"
    rings, conflicts, gaps, missing, unresolved = [], [], [], [], []
    compared = mismatches = uncomparable = missing_plans = unknown_occupancy = 0
    first = None
    previous_tick, previous_agents = None, {}
    for frame in data["frames"]:
        tick = frame["tick"]
        agents = {a["id"]: a for a in frame["agents"]}
        graph = {aid: a.get("blocked_by", []) for aid, a in agents.items()}
        for aid in sorted(agents):
            agent = agents[aid]
            if "planned" not in agent:
                missing_plans += 1
            plan = agent.get("planned", {})
            for field in ("position", "direction", "occupies"):
                if field not in agent or field not in plan:
                    uncomparable += 1
                    continue
                compared += 1
                if agent[field] != plan[field]:
                    mismatches += 1
                    if first is None:
                        first = {"tick": tick, "agent": aid, "field": field,
                                 "planned": plan[field], "actual": agent[field]}
            if "occupies" not in agent or (agent.get("occupies") is True and "position" not in agent):
                unknown_occupancy += 1
            for blocker in agent.get("blocked_by", []):
                if blocker not in agents:
                    unresolved.append({"tick": tick, "agent": aid, "blocker_not_recorded": blocker})
        for members in cyclic_components(graph):
            member_set = set(members)
            hints = [{"agent": aid, "release_tick": agents[aid]["release_tick"]}
                     for aid in members if "release_tick" in agents[aid]]
            rings.append({"tick": tick, "agents": members,
                          "edges": [[a, b] for a in members for b in sorted(graph[a]) if b in member_set],
                          "release_hints": hints, "deadlock_proven": False})
        if vertex_enabled:
            cells = {}
            for aid, agent in sorted(agents.items()):
                if occupied(agent):
                    cells.setdefault(tuple(agent["position"]), []).append(aid)
            for position, ids in sorted(cells.items()):
                if len(ids) > 1:
                    conflicts.append({"kind": "vertex", "tick": tick,
                                      "position": list(position), "agents": ids})
        if previous_tick is not None:
            if tick != previous_tick + 1:
                gaps.append({"previous_tick": previous_tick, "next_tick": tick,
                             "unrecorded_ticks": tick - previous_tick - 1})
            for aid in sorted(previous_agents.keys() - agents.keys()):
                missing.append({"agent": aid, "recorded_at": previous_tick, "not_recorded_at": tick})
            if swap_enabled and tick == previous_tick + 1:
                moves = {}
                for aid in sorted(previous_agents.keys() & agents.keys()):
                    before, after = previous_agents[aid], agents[aid]
                    if occupied(before) and occupied(after):
                        src, dst = tuple(before["position"]), tuple(after["position"])
                        if src != dst:
                            moves.setdefault((src, dst), []).append(aid)
                for (src, dst), ids in sorted(moves.items()):
                    if src < dst and (dst, src) in moves:
                        for aid in ids:
                            for bid in moves[(dst, src)]:
                                conflicts.append({"kind": "edge_swap", "from_tick": previous_tick,
                                                  "to_tick": tick, "agents": [aid, bid],
                                                  "endpoints": [list(src), list(dst)]})
        previous_tick, previous_agents = tick, agents
    return {"schema": "rail-diagnosis/v1", "synthetic": data.get("synthetic") is True,
            "frame_count": len(data["frames"]), "first_divergence": first,
            "comparison": {"compared_fields": compared, "mismatched_fields": mismatches,
                           "uncompared_fields": uncomparable, "agent_records_without_plan": missing_plans},
            "checks": {"vertex": "checked_recorded_point_occupancy" if vertex_enabled else "not_checked_by_semantics",
                       "edge_swap": "checked_consecutive_tick_point_endpoints" if swap_enabled else "not_checked_by_semantics"},
            "wait_cycles": bounded(rings, limit), "conflicts": bounded(conflicts, limit),
            "coverage": {"tick_gaps": bounded(gaps, limit), "agent_disappearances": bounded(missing, limit),
                         "unrecorded_blockers": bounded(unresolved, limit),
                         "agent_records_without_known_occupancy": unknown_occupancy},
            "limits": ["Findings apply only to recorded fields and declared point-agent semantics; no topology or fractional-speed validation.",
                       "A same-tick blocked_by cycle is not a deadlock proof. Missing release hints do not mean permanent blocking.",
                       "Missing agents are unrecorded, not inferred to have exited. Sparse frames conceal intervening events.",
                       "Unchanged positions do not establish waiting duration or performance loss. malfunction is not interpreted.",
                       "No recorded conflict or divergence does not prove safety, complete agreement, or optimality."]}


def slice_trace(data, start, end, context):
    validate_trace(data)
    require(start >= 0 and end >= start and context >= 0, "Require 0 <= start <= end and context >= 0")
    frames = data["frames"]
    selected = [i for i, frame in enumerate(frames) if start <= frame["tick"] <= end]
    require(bool(selected), "Requested interval contains no recorded frame")
    lo, hi = max(0, selected[0] - context), min(len(frames), selected[-1] + context + 1)
    result = copy.deepcopy(data)
    result["frames"] = copy.deepcopy(frames[lo:hi])
    result["slice"] = {"requested_start": start, "requested_end": end, "context_frames_each_side": context,
                       "selected_ticks": [frames[i]["tick"] for i in selected],
                       "included_ticks": [f["tick"] for f in frames[lo:hi]],
                       "source_frame_count": len(frames), "is_simulation": False,
                       "complete_checkpoint": False,
                       "limits": "Recorded slice only. Context is observed frames, possibly sparse; positions cannot reconstruct Flatland state."}
    return result


def reservation_key(entry, label):
    require(isinstance(entry, dict), f"{label} must be an object")
    require(nonempty(entry.get("owner")) and nonempty(entry.get("resource")),
            f"{label} needs nonempty owner and resource strings")
    start, end = entry.get("start"), entry.get("end")
    require(integer(start) and integer(end) and 0 <= start < end,
            f"{label} requires integer half-open bounds 0 <= start < end")
    return entry["owner"], entry["resource"], start, end


def reservation_entry(key, count):
    return dict(zip(("owner", "resource", "start", "end", "count"), (*key, count)))


def reservation_table(table):
    return [reservation_entry(key, count) for key, count in sorted(table.items())]


def reservations(data, limit):
    require(isinstance(data, dict) and data.get("schema") == "rail-reservations/v1",
            "Expected schema rail-reservations/v1")
    require(data.get("interval") == "half-open", "interval must be half-open")
    events = data.get("events")
    require(isinstance(events, list), "events must be an array")
    table, checkpoints, issues, duplicates, rollbacks, observations = Counter(), {}, [], [], [], []
    for index, event in enumerate(events):
        require(isinstance(event, dict), f"events[{index}] must be an object")
        op = event.get("op")
        require(op in ("reserve", "release", "checkpoint", "rollback", "observed"),
                f"events[{index}].op is unsupported")
        if op in ("reserve", "release"):
            key = reservation_key(event, f"events[{index}]")
            if op == "reserve":
                if table[key]:
                    duplicates.append({"event": index, "entry": reservation_entry(key, table[key] + 1)})
                for other in sorted(table):
                    if key[0] != other[0] and key[1] == other[1] and key[2] < other[3] and other[2] < key[3]:
                        issues.append({"kind": "overlap", "event": index,
                                       "incoming": reservation_entry(key, table[key] + 1),
                                       "existing": reservation_entry(other, table[other])})
                table[key] += 1
            elif not table[key]:
                issues.append({"kind": "unowned_release", "event": index, "entry": reservation_entry(key, 0)})
            else:
                table[key] -= 1
                if table[key] == 0:
                    del table[key]
        elif op in ("checkpoint", "rollback"):
            name = event.get("name")
            require(nonempty(name), f"events[{index}].name must be a nonempty string")
            if op == "checkpoint":
                require(name not in checkpoints, f"Duplicate checkpoint name: {name}")
                checkpoints[name] = table.copy()
            elif name not in checkpoints:
                issues.append({"kind": "unknown_checkpoint", "event": index, "name": name})
            else:
                table = checkpoints[name].copy()
                rollbacks.append({"event": index, "name": name, "restored_reference_count": sum(table.values())})
        else:
            entries = event.get("entries")
            require(isinstance(entries, list), f"events[{index}].entries must be an array")
            observed = Counter()
            for entry in entries:
                key = reservation_key(entry, f"events[{index}].entries")
                count = entry.get("count")
                require(integer(count) and count > 0, "Observed count must be a positive integer")
                require(key not in observed, "Observed snapshot must have unique owner/resource/interval keys")
                observed[key] = count
            differences = [{"entry": reservation_entry(key, table[key]), "observed_count": observed[key]}
                           for key in sorted(table.keys() | observed.keys()) if table[key] != observed[key]]
            observations.append({"event": index, "matches": not differences, "differences": bounded(differences, limit)})
    return {"schema": "rail-reservation-report/v1", "synthetic": data.get("synthetic") is True,
            "event_count": len(events), "issues": bounded(issues, limit),
            "duplicate_references": bounded(duplicates, limit), "rollbacks": bounded(rollbacks, limit),
            "observations": bounded(observations, limit),
            "observed_equivalence": "not_checked_no_observed_snapshots" if not observations else
                ("all_supplied_snapshots_match" if all(x["matches"] for x in observations) else "supplied_snapshot_mismatch"),
            "final_reference_count": sum(table.values()), "final_table": bounded(reservation_table(table), limit),
            "limits": ["Events replay an initially empty table in listed order using exact-key reference counts and half-open intervals.",
                       "Reported invalid releases or unknown rollbacks leave the table unchanged; overlapping reserves remain represented.",
                       "Named checkpoints retain independent snapshots after rollback. No reservation expires implicitly.",
                       "Observed equality checks supplied normalized snapshots only; missing observations do not prove actual project-state equivalence."]}


def validate_manifest(data):
    require(isinstance(data, dict) and data.get("schema") == "rail-replay/v1", "Expected schema rail-replay/v1")
    for key in ("checkpoint", "runner_requirements", "clock"):
        require(isinstance(data.get(key), dict) and bool(data[key]), f"{key} must be a nonempty object")
    require(isinstance(data.get("actions"), list), "actions must be an array")
    require(integer(data["clock"].get("start_tick")) and data["clock"]["start_tick"] >= 0,
            "clock.start_tick must be a nonnegative integer")
    require(nonempty(data["clock"].get("action_timing")), "clock.action_timing must describe action timing")


def replay_metadata(value, keys):
    """Do not forward arbitrary adapter payloads into the compact report."""
    if not isinstance(value, dict):
        return {}
    summary = {}
    for key in keys:
        item = value.get(key)
        if isinstance(item, str):
            summary[key] = item[:200] + ("..." if len(item) > 200 else "")
        elif type(item) is bool or (integer(item) and len(str(item)) <= 20):
            summary[key] = item
    return summary


def replay(data, adapter, timeout, limit):
    validate_manifest(data)
    adapter = Path(adapter).resolve()
    require(adapter.is_file() and adapter.suffix.lower() == ".py", "--adapter must name an existing explicitly supplied Python file")
    require(timeout > 0 and timeout < float("inf"), "--timeout must be finite and positive")
    try:
        completed = subprocess.run([sys.executable, str(adapter)], input=json.dumps(data, allow_nan=False),
                                   text=True, encoding="utf-8", capture_output=True, shell=False, timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        raise ToolError("runner_timeout", f"Adapter exceeded {timeout:g} seconds: {adapter}") from exc
    except (OSError, UnicodeError) as exc:
        raise ToolError("runner_error", str(exc)) from exc
    if completed.returncode:
        # Do not echo arbitrary runner stderr, which may contain private project data.
        raise ToolError("runner_failed", f"Adapter exited with code {completed.returncode}; inspect the adapter locally for details")
    result = parse_json(completed.stdout, "Adapter stdout")
    require(isinstance(result, dict) and result.get("schema") == "rail-replay-result/v1",
            "Adapter must return schema rail-replay-result/v1 on stdout")
    validate_trace(result.get("trace"))
    require(bool(result["trace"]["frames"]) and result["trace"]["frames"][0]["tick"] == data["clock"]["start_tick"],
            "Adapter trace must include its initial checkpoint frame at clock.start_tick")
    trace = result["trace"]
    report = {"schema": "rail-replay-report/v1", "adapter": str(adapter), "executed": True,
            "timeout_seconds": timeout, "frame_count": len(trace["frames"]),
            "tick_range": [trace["frames"][0]["tick"], trace["frames"][-1]["tick"]],
            "synthetic": trace.get("synthetic") is True,
            "runner": replay_metadata(result.get("runner"), ("engine", "version", "name", "is_flatland", "synthetic")),
            "completion": replay_metadata(result.get("completion"), ("actions_applied", "final_tick", "status")),
            "diagnosis": diagnose(trace, limit),
            "limits": ["This executes the explicitly selected adapter; engine fidelity and checkpoint completeness remain its responsibility.",
                       "Runner/completion summaries retain selected scalar fields only; strings are capped at 200 characters. Use --trace-output to save the full normalized trace.",
                       "No benchmark performance or equivalence to Flatland is inferred from successful protocol execution."]}
    return report, trace


class JsonParser(argparse.ArgumentParser):
    def error(self, message):
        raise ToolError("arguments", message)


def guard_output(output, protected_paths):
    if output is None:
        return
    destination = Path(output).resolve()
    for source in protected_paths:
        source = Path(source).resolve()
        same = destination == source
        try:
            same = same or (destination.exists() and source.exists() and destination.samefile(source))
        except OSError as exc:
            raise ToolError("path_error", str(exc)) from exc
        if same:
            raise ToolError("input_overwrite", f"Output would overwrite input, adapter, or another output: {source}")


def main(argv=None):
    try:
        parser = JsonParser(description=__doc__)
        commands = parser.add_subparsers(dest="command", required=True)
        for name in ("diagnose", "slice", "replay", "reservations"):
            command = commands.add_parser(name)
            command.add_argument("input", help="JSON input path")
            command.add_argument("--output", help="Write JSON here; never the input or adapter path")
            command.add_argument("--limit", type=int, default=20, help="Maximum items per report collection (default 20)")
            if name == "slice":
                command.add_argument("--start", type=int, required=True)
                command.add_argument("--end", type=int, required=True)
                command.add_argument("--context", type=int, default=1, help="Observed frames retained before and after")
            elif name == "replay":
                command.add_argument("--adapter", required=True, help="User-selected Python adapter, never taken from input data")
                command.add_argument("--timeout", type=float, default=10.0)
                command.add_argument("--trace-output", help="Save the full normalized trace separately from the compact report")
        args = parser.parse_args(argv)
        require(args.limit > 0, "--limit must be positive")
        protected = [args.input] + ([args.adapter] if args.command == "replay" else [])
        guard_output(args.output, protected)
        if args.command == "replay":
            guard_output(args.trace_output, protected + ([args.output] if args.output else []))
            if args.trace_output:
                guard_output(args.output, [args.trace_output])
        data = read_json(args.input)
        if args.command == "diagnose":
            result = diagnose(data, args.limit)
        elif args.command == "slice":
            result = slice_trace(data, args.start, args.end, args.context)
        elif args.command == "reservations":
            result = reservations(data, args.limit)
        else:
            result, trace = replay(data, args.adapter, args.timeout, args.limit)
            result["trace_output"] = str(Path(args.trace_output).resolve()) if args.trace_output else None
        raw = json.dumps(result, ensure_ascii=True, allow_nan=False, separators=(",", ":")) + "\n"
        if args.command == "replay" and args.trace_output:
            trace_raw = json.dumps(trace, ensure_ascii=True, allow_nan=False, separators=(",", ":")) + "\n"
            Path(args.trace_output).write_text(trace_raw, encoding="utf-8")
        if args.output:
            Path(args.output).write_text(raw, encoding="utf-8")
        else:
            sys.stdout.write(raw)
        return 0
    except ToolError as exc:
        sys.stderr.write(json.dumps({"error": {"code": exc.code, "message": exc.message}}, ensure_ascii=True) + "\n")
        return 2
    except (OSError, UnicodeError, ValueError, RecursionError) as exc:
        sys.stderr.write(json.dumps({"error": {"code": "io_or_encoding_error", "message": str(exc)}}, ensure_ascii=True) + "\n")
        return 2


if __name__ == "__main__":
    sys.exit(main())
