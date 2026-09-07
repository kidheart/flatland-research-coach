#!/usr/bin/env python3
"""SYNTHETIC protocol demonstration; a tiny line railway, not a Flatland engine."""

import copy
import json
import sys

from rail_trace import ToolError, integer, nonempty, parse_json, require, validate_manifest


def run(manifest):
    validate_manifest(manifest)
    require(manifest.get("synthetic") is True, "This runner accepts explicitly synthetic manifests only")
    require(manifest["runner_requirements"] == {"engine": "synthetic-line/v1"},
            "runner_requirements must identify synthetic-line/v1")
    require(manifest["clock"]["action_timing"] == "before_step", "Synthetic actions apply before_step")
    checkpoint = copy.deepcopy(manifest["checkpoint"])
    tick, length = checkpoint.get("tick"), checkpoint.get("track_length")
    require(integer(tick) and tick == manifest["clock"]["start_tick"], "Checkpoint and clock ticks must match")
    require(integer(length) and length >= 2, "track_length must be an integer >= 2")
    records = checkpoint.get("agents")
    require(isinstance(records, list), "checkpoint.agents must be an array")
    agents, cells = {}, set()
    for agent in records:
        require(isinstance(agent, dict) and nonempty(agent.get("id")), "Synthetic agent needs an id")
        aid, cell = agent["id"], agent.get("cell")
        require(aid not in agents, "Duplicate synthetic agent id")
        require(integer(cell) and 0 <= cell < length and cell not in cells, "Agent cells must be unique and on track")
        require(integer(agent.get("direction")) and agent["direction"] in (1, 3), "Direction must be 1=east or 3=west")
        period, phase = agent.get("move_period"), agent.get("phase")
        require(integer(period) and period >= 1 and integer(phase) and 0 <= phase < period,
                "Require move_period >= 1 and 0 <= phase < move_period")
        remaining = agent.get("malfunction_remaining")
        require(integer(remaining) and remaining >= 0, "malfunction_remaining must be a nonnegative integer")
        agents[aid], cells = agent, cells | {cell}

    def frame(at, blocked=None):
        blocked = blocked or {}
        return {"tick": at, "agents": [
            {"id": aid, "position": [0, a["cell"]], "direction": a["direction"], "occupies": True,
             "blocked_by": blocked.get(aid, []), "malfunction": {"remaining": a["malfunction_remaining"]},
             "synthetic_motion_phase": a["phase"]}
            for aid, a in sorted(agents.items())]}

    frames = [frame(tick)]
    for index, action in enumerate(manifest["actions"]):
        require(isinstance(action, dict) and integer(action.get("tick")) and action["tick"] == tick,
                f"actions[{index}].tick must equal next execution tick {tick}")
        commands = action.get("commands")
        require(isinstance(commands, dict) and set(commands) == set(agents),
                "Each action must supply commands for exactly the checkpoint agents")
        require(all(value in ("go", "hold") for value in commands.values()), "Commands must be go or hold")
        occupied = {a["cell"]: aid for aid, a in agents.items()}
        proposals, blocked = {}, {}
        for aid, agent in agents.items():
            if agent["malfunction_remaining"]:
                agent["malfunction_remaining"] -= 1
                continue
            if commands[aid] == "hold":
                continue
            agent["phase"] += 1
            if agent["phase"] < agent["move_period"]:
                continue
            destination = agent["cell"] + (1 if agent["direction"] == 1 else -1)
            agent["phase"] = agent["move_period"] - 1
            if not 0 <= destination < length:
                continue
            if destination in occupied:
                blocked[aid] = [occupied[destination]]
            else:
                proposals[aid] = destination
        for aid, destination in proposals.items():
            competitors = sorted(other for other, cell in proposals.items() if cell == destination and other != aid)
            if competitors:
                blocked[aid] = competitors
            else:
                agents[aid]["cell"], agents[aid]["phase"] = destination, 0
        tick += 1
        frames.append(frame(tick, blocked))
    return {"schema": "rail-replay-result/v1", "synthetic": True,
            "runner": {"engine": "synthetic-line/v1", "is_flatland": False},
            "completion": {"actions_applied": len(manifest["actions"]), "final_tick": tick},
            "trace": {"schema": "rail-trace/v1", "synthetic": True,
                      "semantics": {"agent_model": "point", "vertex": "exclusive", "edge_swap": "forbidden"},
                      "frames": frames}}


def main():
    try:
        result = run(parse_json(sys.stdin.read(), "Manifest stdin"))
        print(json.dumps(result, allow_nan=False, separators=(",", ":")))
        return 0
    except (ToolError, ValueError, TypeError) as exc:
        print(json.dumps({"error": {"code": "synthetic_runner_input", "message": str(exc)}}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
