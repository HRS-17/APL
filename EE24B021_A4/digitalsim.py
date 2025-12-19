"""Tiny combinational logic simulator producing WaveDrom JSON.

Usage:
  python digitalsim.py path/to/circuit.net [--out out.json]

Input format sections (fixed order): INPUTS, OUTPUTS, GATES, STIMULUS.
Gates: OUT = AND(A, B) | OR(A, B) | XOR(A, B) | NOT(A)
"""

import sys
import argparse
from pathlib import Path
from typing import List, Tuple, Dict
import re
import json


# ------------------------------------------------------------
# 1. Parse the netlist text
# ------------------------------------------------------------
def parse_netlist(text: str):
    lines = [ln.strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln and not ln.startswith("#")]

    def expect(prefix: str, idx: int) -> int:
        if idx >= len(lines) or not lines[idx].startswith(prefix):
            raise ValueError(f"Expected '{prefix}' section")
        return idx

    # ---- INPUTS ----
    i = expect("INPUTS:", 0)
    inputs = lines[i].split(":", 1)[1].strip().split()
    if not inputs:
        raise ValueError("INPUTS section cannot be empty")
    i += 1

    # ---- OUTPUTS ----
    i = expect("OUTPUTS:", i)
    outputs = lines[i].split(":", 1)[1].strip().split()
    if not outputs:
        raise ValueError("OUTPUTS section cannot be empty")
    i += 1

    # ---- GATES ----
    i = expect("GATES:", i)
    i += 1

    gates = []
    defined = set(inputs)

    gate_re = re.compile(
        r"^(?P<out>[A-Za-z_][A-Za-z0-9_]*)\s*=\s*"
        r"(?P<type>AND|OR|XOR|NOT)\s*\(\s*"
        r"(?P<args>[A-Za-z0-9_,\s]+)\s*\)\s*$"
    )

    while i < len(lines) and not lines[i].startswith("STIMULUS:"):
        m = gate_re.match(lines[i])
        if not m:
            raise ValueError(f"Invalid gate line: '{lines[i]}'")

        out = m.group("out")
        typ = m.group("type")
        args = tuple(a.strip() for a in m.group("args").split(","))

        # Validation
        if typ == "NOT" and len(args) != 1:
            raise TypeError(f"Gate {out} of type NOT must have 1 input")
        if typ in {"AND", "OR", "XOR"} and len(args) != 2:
            raise TypeError(f"Gate {out} of type {typ} must have 2 inputs")
        if out in defined:
            raise ValueError(f"Gate {out} defined more than once")

        defined.add(out)
        gates.append({"name": out, "type": typ, "inputs": args})
        i += 1

    if not gates:
        raise ValueError("GATES section cannot be empty")

    # ---- STIMULUS ----
    i = expect("STIMULUS:", i)
    i += 1

    stimuli = []
    last_time = -1

    while i < len(lines):
        parts = lines[i].split()
        if len(parts) != len(inputs) + 1:
            raise ValueError(f"Invalid stimulus line: {lines[i]}")
        t = int(parts[0])
        if t <= last_time:
            raise ValueError("Stimulus times must be strictly increasing")
        vals = tuple(parts[1:])
        if any(v not in {"0", "1"} for v in vals):
            raise ValueError(f"Stimulus values must be 0 or 1: {lines[i]}")
        stimuli.append((t, vals))
        last_time = t
        i += 1

    return inputs, outputs, gates, stimuli


# ------------------------------------------------------------
# 2. Topological sorting for gate evaluation order
# ------------------------------------------------------------
def topo_sort(gates: List[dict], inputs: List[str]) -> List[Tuple[str, str]]:
    deps = {g["name"]: set(g["inputs"]) for g in gates}
    gate_names = {g["name"] for g in gates}

    for g in deps:
        deps[g] = {d for d in deps[g] if d in gate_names}

    type_lookup = {g["name"]: g["type"] for g in gates}

    order: List[Tuple[str, str]] = []
    ready = [g for g in deps if not deps[g]]

    while ready:
        node = ready.pop()
        order.append((node, type_lookup[node]))
        for h in deps:
            if node in deps[h]:
                deps[h].remove(node)
                if not deps[h]:
                    ready.append(h)

    if len(order) != len(gates):
        raise ValueError("Cyclic or unresolved gate dependencies detected")

    return order


# ------------------------------------------------------------
# 3. Gate evaluation logic
# ------------------------------------------------------------
def eval_gate(typ: str, args: List[str]) -> str:
    if typ == "NOT":
        return "0" if args[0] == "1" else "1"
    elif typ == "AND":
        return "1" if args[0] == "1" and args[1] == "1" else "0"
    elif typ == "OR":
        return "1" if args[0] == "1" or args[1] == "1" else "0"
    elif typ == "XOR":
        return "1" if args[0] != args[1] else "0"
    else:
        raise ValueError(f"Unknown gate type: {typ}")


# ------------------------------------------------------------
# 4. Simulation
# ------------------------------------------------------------
def simulate(parsed_netlist):
    inputs, outputs, gates, stimuli = parsed_netlist
    order = topo_sort(gates, inputs)

    signals: Dict[str, str] = {}
    waves = {s: "" for s in inputs + outputs}

    for t, values in stimuli:
        # Set primary inputs
        for name, val in zip(inputs, values):
            signals[name] = val

        # Evaluate gates in dependency-safe order
        for gname, gtype in order:
            g = next(g for g in gates if g["name"] == gname)
            arg_vals = [signals[a] for a in g["inputs"]]
            signals[gname] = eval_gate(gtype, arg_vals)

        # Record input/output values for this time step
        for name in inputs:
            waves[name] += signals[name]
        for name in outputs:
            waves[name] += signals[name]

    return waves


# ------------------------------------------------------------
# 5. Convert results to WaveDrom JSON
# ------------------------------------------------------------
def to_wavedrom_json(inputs, outputs, waves):
    signal_list = []
    for name in inputs + outputs:
        signal_list.append({"name": name, "wave": waves[name]})
    return json.dumps({"signal": signal_list}, indent=2)


# ------------------------------------------------------------
# 6. CLI entry point
# ------------------------------------------------------------
def main(argv: List[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("netlist", help=".net file path")
    ap.add_argument("--out", "-o", help="output JSON path")
    args = ap.parse_args(argv)

    text = Path(args.netlist).read_text()
    parsed = parse_netlist(text)
    waves = simulate(parsed)
    js = to_wavedrom_json(parsed[0], parsed[1], waves)

    out_path = args.out
    if not out_path:
        p = Path(args.netlist)
        out_path = str(p.with_suffix(".json"))

    Path(out_path).write_text(js + "\n")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
