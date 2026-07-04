#!/usr/bin/env python3
"""Assemble one scenario's results JSON for the scorecard.

Usage:
    mk_result.py --scenario <name> [--judged <judged.json>] \
        [--state-file <f>] [--mech-a <tsv>] [--mech-b <tsv>]

Mechanical TSV lines are `<0|1><TAB><description>` (written by bench.sh after grepping the
state file). Emits the results object consumed by lib/scorecard.py to stdout.
"""
import argparse
import json


def read_mech(path):
    rows = []
    if not path:
        return rows
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                if not line:
                    continue
                matched, _, desc = line.partition("\t")
                rows.append({"matched": matched.strip() == "1", "desc": desc})
    except OSError:
        pass
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenario", required=True)
    ap.add_argument("--judged")
    ap.add_argument("--state-file")
    ap.add_argument("--mech-a")
    ap.add_argument("--mech-b")
    a = ap.parse_args()

    out = {"scenario": a.scenario}
    if a.judged:
        with open(a.judged, encoding="utf-8") as f:
            out["judged"] = json.load(f)
    mech_a = read_mech(a.mech_a)
    mech_b = read_mech(a.mech_b)
    if mech_a or mech_b:
        out["mechanical"] = {
            "state_file": a.state_file or "",
            "arm-a": mech_a,
            "arm-b": mech_b,
        }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
