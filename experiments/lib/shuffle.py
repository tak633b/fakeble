#!/usr/bin/env python3
"""Blind-shuffle two arm responses into response-1 / response-2 slots.

Usage:
    shuffle.py <arm_a_response> <arm_b_response> <out_dir> [--force ab|ba]

Writes into <out_dir>:
    response-1.txt, response-2.txt  — the two responses in the chosen order
    mapping.json                    — which slot holds which arm (+ the seed)

Order is random per call (seeded from os.urandom) unless --force pins it, which
the double-judge pass uses to present the opposite ordering. The mapping file is
written and then re-read to VERIFY it landed before the caller trusts it; a missing
or unreadable mapping is a hard error (exit 2), because a lost mapping means a judged
score cannot be attributed back to an arm — the exact positional-bias failure the
original RESULTS.md flagged.
"""
import json
import os
import random
import sys


def die(msg, code=2):
    sys.stderr.write("shuffle.py: " + msg + "\n")
    sys.exit(code)


def main():
    args = sys.argv[1:]
    force = None
    if "--force" in args:
        i = args.index("--force")
        try:
            force = args[i + 1]
        except IndexError:
            die("--force needs an argument (ab|ba)")
        if force not in ("ab", "ba"):
            die("--force must be 'ab' or 'ba', got %r" % force)
        del args[i:i + 2]

    if len(args) != 3:
        die("usage: shuffle.py <arm_a_response> <arm_b_response> <out_dir> [--force ab|ba]")
    resp_a_path, resp_b_path, out_dir = args

    for p in (resp_a_path, resp_b_path):
        if not os.path.isfile(p):
            die("response file not found: %s" % p)

    os.makedirs(out_dir, exist_ok=True)

    seed = int.from_bytes(os.urandom(8), "big")
    if force == "ab":
        order = ["arm-a", "arm-b"]
    elif force == "ba":
        order = ["arm-b", "arm-a"]
    else:
        rng = random.Random(seed)
        order = ["arm-a", "arm-b"]
        rng.shuffle(order)

    src = {"arm-a": resp_a_path, "arm-b": resp_b_path}
    with open(src[order[0]], encoding="utf-8", errors="replace") as f:
        r1 = f.read()
    with open(src[order[1]], encoding="utf-8", errors="replace") as f:
        r2 = f.read()

    with open(os.path.join(out_dir, "response-1.txt"), "w", encoding="utf-8") as f:
        f.write(r1)
    with open(os.path.join(out_dir, "response-2.txt"), "w", encoding="utf-8") as f:
        f.write(r2)

    mapping = {
        "seed": seed,
        "forced": force,
        "response-1": order[0],
        "response-2": order[1],
    }
    map_path = os.path.join(out_dir, "mapping.json")
    with open(map_path, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)

    # VERIFY the mapping actually landed and round-trips.
    try:
        with open(map_path, encoding="utf-8") as f:
            back = json.load(f)
    except (OSError, ValueError) as e:
        die("mapping.json failed to write/reload: %s" % e)
    if back.get("response-1") != order[0] or back.get("response-2") != order[1]:
        die("mapping.json verification mismatch")

    print(map_path)


if __name__ == "__main__":
    main()
