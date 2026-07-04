#!/usr/bin/env python3
"""Collect ALL assistant text from a `claude -p --output-format stream-json` transcript.

`claude -p` prints only the FINAL assistant message. A turn that goes
answer -> blocked tool call -> short follow-up loses the answer entirely,
which punishes any multi-message turn in the bench. This collector joins
every assistant text block in order, which is what an interactive user
actually sees.

Usage: collect_text.py <stream_json_file>
Prints the joined text to stdout. Exits 1 if no assistant text found.
"""
import json
import sys

def main() -> int:
    if len(sys.argv) != 2:
        sys.stderr.write("usage: collect_text.py <stream_json_file>\n")
        return 1
    parts: list[str] = []
    with open(sys.argv[1], encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            if d.get("type") != "assistant":
                continue
            content = (d.get("message") or {}).get("content")
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        t = (block.get("text") or "").strip()
                        if t:
                            parts.append(t)
            elif isinstance(content, str) and content.strip():
                parts.append(content.strip())
    if not parts:
        # fall back to the result field if present (e.g., error runs)
        with open(sys.argv[1], encoding="utf-8", errors="replace") as fh:
            for line in fh:
                try:
                    d = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if d.get("type") == "result" and d.get("result"):
                    parts.append(str(d["result"]))
                    break
    if not parts:
        return 1
    print("\n\n".join(parts))
    return 0

if __name__ == "__main__":
    sys.exit(main())
