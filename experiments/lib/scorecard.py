#!/usr/bin/env python3
"""Render the final scorecard markdown from per-scenario result files.

Usage:
    scorecard.py --model <m> --judge-model <jm> --timestamp <ts> \
        [--double] [--dry-run] <results-*.json> ...

Each results file (written by bench.sh) has shape:
    {"scenario": str,
     "judged": {"arm-a": {...,"total"}, "arm-b": {...}, "criteria":[...], "max_per_arm": int},
     "mechanical": {"state_file": str,
                    "arm-a": [{"desc":str,"matched":bool}, ...],
                    "arm-b": [...]}   # optional
    }

Prints one markdown scorecard: a per-scenario criterion table (arm B = Fakeble, arm A =
vanilla), any mechanical checks, and a totals table. arm-b is the Fakeble arm.
"""
import argparse
import json


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def fmt(v):
    if isinstance(v, float):
        return ("%.1f" % v).rstrip("0").rstrip(".")
    return str(v)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--judge-model", required=True)
    ap.add_argument("--timestamp", required=True)
    ap.add_argument("--double", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("results", nargs="*")
    a = ap.parse_args()

    out = []
    out.append("# Fakeble bench — %s" % a.timestamp)
    out.append("")
    out.append("- model (both arms): `%s`" % a.model)
    out.append("- judge model: `%s`%s" % (a.judge_model, "  (double-judged, position-swapped)" if a.double else ""))
    out.append("- arm A = vanilla (scenario files only) · arm B = Fakeble (+ CLAUDE.md + skills)")
    out.append("- isolated: `--setting-sources project --strict-mcp-config`; blind-shuffled, mapping-verified")
    if a.dry_run:
        out.append("")
        out.append("> DRY RUN — no `claude -p` calls were made; scores below are absent by design.")
    out.append("")

    results = [load(p) for p in a.results]

    totals = []  # (scenario, max, arm_a_total, arm_b_total)
    for r in results:
        scen = r["scenario"]
        out.append("## %s" % scen)
        out.append("")
        j = r.get("judged")
        if j:
            keys = j["criteria"]
            out.append("| criterion | vanilla (A) | Fakeble (B) |")
            out.append("|---|---|---|")
            for k in keys:
                out.append("| %s | %s | %s |" % (k, fmt(j["arm-a"][k]), fmt(j["arm-b"][k])))
            out.append("| **total** | **%s** | **%s** | " % (
                fmt(j["arm-a"]["total"]), fmt(j["arm-b"]["total"])))
            out.append("")
            out.append("_max per arm: %d_" % j["max_per_arm"])
            out.append("")
            totals.append((scen, j["max_per_arm"], j["arm-a"]["total"], j["arm-b"]["total"]))
        m = r.get("mechanical")
        if m:
            out.append("Mechanical checks on `%s` (no judge):" % m.get("state_file", "?"))
            out.append("")
            out.append("| check | vanilla (A) | Fakeble (B) |")
            out.append("|---|---|---|")
            checks_a = m.get("arm-a", [])
            checks_b = m.get("arm-b", [])
            for i in range(max(len(checks_a), len(checks_b))):
                desc = (checks_a[i] if i < len(checks_a) else checks_b[i])["desc"]
                va = "PASS" if (i < len(checks_a) and checks_a[i]["matched"]) else "—"
                vb = "PASS" if (i < len(checks_b) and checks_b[i]["matched"]) else "—"
                out.append("| %s | %s | %s |" % (desc, va, vb))
            out.append("")

    if totals:
        out.append("## Totals (judged)")
        out.append("")
        out.append("| scenario | max | vanilla (A) | Fakeble (B) | Δ (B−A) |")
        out.append("|---|---|---|---|---|")
        sa = sb = smax = 0.0
        for scen, mx, ta, tb in totals:
            out.append("| %s | %d | %s | %s | %s |" % (
                scen, mx, fmt(ta), fmt(tb), fmt(round(tb - ta, 1))))
            sa += ta
            sb += tb
            smax += mx
        out.append("| **all** | **%s** | **%s** | **%s** | **%s** |" % (
            fmt(smax), fmt(round(sa, 1)), fmt(round(sb, 1)), fmt(round(sb - sa, 1))))
        out.append("")

    print("\n".join(out))


if __name__ == "__main__":
    main()
