#!/usr/bin/env python3
"""Average several parse_scores.py outputs into one (for --double-judge).

Usage:
    merge_judges.py <scores1.json> <scores2.json> [<scores3.json> ...]

Each input is a parse_scores.py result. Averages per-arm, per-criterion across all inputs
(position-bias control: pass 1 and pass 2 present opposite orderings). Per-criterion values
and totals are rounded to one decimal. Prints the merged JSON with the same shape.
"""
import json
import sys


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def main():
    if len(sys.argv) < 2:
        sys.stderr.write("usage: merge_judges.py <scores1.json> [<scores2.json> ...]\n")
        sys.exit(2)
    inputs = [load(p) for p in sys.argv[1:]]
    base = inputs[0]
    keys = base["criteria"]
    arms = [a for a in base if a not in ("criteria", "max_per_arm")]

    out = {"criteria": keys, "max_per_arm": base["max_per_arm"], "judges": len(inputs)}
    for arm in arms:
        merged = {}
        total = 0.0
        for k in keys:
            vals = [d[arm][k] for d in inputs]
            avg = round(sum(vals) / len(vals), 1)
            merged[k] = avg
            total += avg
        merged["total"] = round(total, 1)
        out[arm] = merged
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
