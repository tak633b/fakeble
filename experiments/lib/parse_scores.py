#!/usr/bin/env python3
"""Parse a judge's raw output into per-arm scores.

Usage:
    parse_scores.py <judge_raw.txt> <mapping.json> <rubric.md>

Extracts the STRICT JSON the judge was asked for (tolerant of stray prose or code fences
around it), maps response-1/response-2 back to arm-a/arm-b via the mapping file, validates the
criterion keys against the rubric, and prints per-arm scores as JSON:

    {"arm-a": {"<crit>": int, ..., "total": int},
     "arm-b": {...},
     "criteria": [...], "max_per_arm": int}

Missing or non-integer scores are clamped to 0 and noted on stderr, so a malformed judge
response degrades to a low score rather than crashing the whole run.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rubric  # noqa: E402


def extract_json(text):
    """Find the first balanced {...} object in text and parse it."""
    start = text.find("{")
    while start != -1:
        depth = 0
        in_str = False
        esc = False
        for i in range(start, len(text)):
            c = text[i]
            if in_str:
                if esc:
                    esc = False
                elif c == "\\":
                    esc = True
                elif c == '"':
                    in_str = False
            else:
                if c == '"':
                    in_str = True
                elif c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                    if depth == 0:
                        chunk = text[start:i + 1]
                        try:
                            return json.loads(chunk)
                        except ValueError:
                            break
        start = text.find("{", start + 1)
    raise ValueError("no parseable JSON object found in judge output")


def clamp_int(v):
    try:
        n = int(round(float(v)))
    except (TypeError, ValueError):
        return None
    return max(0, min(5, n))


def main():
    if len(sys.argv) != 4:
        sys.stderr.write("usage: parse_scores.py <judge_raw> <mapping.json> <rubric.md>\n")
        sys.exit(2)
    raw_path, map_path, rubric_path = sys.argv[1:4]

    with open(raw_path, encoding="utf-8", errors="replace") as f:
        raw = f.read()
    with open(map_path, encoding="utf-8") as f:
        mapping = json.load(f)
    keys = [k for k, _ in rubric.parse_criteria(rubric_path)]

    data = extract_json(raw)

    slot_to_arm = {"response_1": mapping["response-1"], "response_2": mapping["response-2"]}
    out = {"criteria": keys, "max_per_arm": 5 * len(keys)}

    for slot, arm in slot_to_arm.items():
        block = data.get(slot) or data.get(slot.replace("_", "-")) or {}
        scores = {}
        total = 0
        for k in keys:
            v = clamp_int(block.get(k))
            if v is None:
                sys.stderr.write("parse_scores.py: %s.%s missing/invalid -> 0\n" % (slot, k))
                v = 0
            scores[k] = v
            total += v
        scores["total"] = total
        out[arm] = scores

    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
