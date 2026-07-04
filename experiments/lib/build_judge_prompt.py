#!/usr/bin/env python3
"""Build a blind-judge prompt for one scenario pair.

Usage:
    build_judge_prompt.py <rubric.md> <prompt_file> <response-1.txt> <response-2.txt> [<prompt2_file>]

Prints the full judge prompt to stdout. The judge sees the task the assistant faced, the
rubric criteria and ground truth, and the two responses labelled response-1 / response-2 (it
is blind to which arm is which). It must return STRICT JSON only — one integer 0-5 per
criterion for each response — which lib/parse_scores.py maps back to arms.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rubric  # noqa: E402


def read(p):
    with open(p, encoding="utf-8", errors="replace") as f:
        return f.read().strip()


def main():
    args = sys.argv[1:]
    if len(args) not in (4, 5):
        sys.stderr.write(
            "usage: build_judge_prompt.py <rubric> <prompt> <resp1> <resp2> [<prompt2>]\n")
        sys.exit(2)
    rubric_path, prompt_path, r1_path, r2_path = args[:4]
    prompt2_path = args[4] if len(args) == 5 else None

    crits = rubric.parse_criteria(rubric_path)
    ground = rubric.parse_ground_truth(rubric_path)
    keys = [k for k, _ in crits]

    crit_lines = "\n".join("  - %s: %s" % (k, d) for k, d in crits)

    turns = "The user's message to the assistant:\n\n<user_message>\n%s\n</user_message>" % read(prompt_path)
    if prompt2_path:
        turns += (
            "\n\nThis was a two-turn task. The assistant's response above covers BOTH turns "
            "(turn 1, then a follow-up). The follow-up message was:\n\n"
            "<user_followup>\n%s\n</user_followup>" % read(prompt2_path))

    schema = {
        "response_1": {k: "<int 0-5>" for k in keys},
        "response_2": {k: "<int 0-5>" for k in keys},
    }

    parts = [
        "You are a strict, impartial judge scoring two AI assistant responses to the same task.",
        "You do not know how either response was produced; judge only what is written.",
        "",
        turns,
        "",
        "What good and bad answers look like (ground truth you have but the assistants did not):",
        "",
        ground if ground else "(none provided)",
        "",
        "Score EACH response 0-5 on each criterion (5 = fully meets it, 0 = absent/wrong):",
        crit_lines,
        "",
        "=== RESPONSE 1 ===",
        read(r1_path),
        "",
        "=== RESPONSE 2 ===",
        read(r2_path),
        "",
        "Output STRICT JSON ONLY — no markdown, no prose, no code fences — exactly this shape:",
        json.dumps(schema, ensure_ascii=False),
        "Every value must be an integer from 0 to 5. Do not add keys. Do not omit keys.",
    ]
    sys.stdout.write("\n".join(parts) + "\n")


if __name__ == "__main__":
    main()
