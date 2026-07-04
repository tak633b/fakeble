"""Shared parser for scenario RUBRIC.md files.

The RUBRIC.md contract (also documented in experiments/README.md):
  - a `## Criteria (0-5 each)` section whose `- key: description` bullets define the
    machine-readable criterion keys (text before the first colon), in order;
  - a `## Ground truth` section whose prose is handed to the judge as context.

Both the judge-prompt builder and the score parser read criteria from here, so the keys
have exactly one source of truth.
"""
import re


def _sections(text):
    """Split markdown into {heading_lower: body} by `## ` headings."""
    out = {}
    cur = None
    buf = []
    for line in text.splitlines():
        m = re.match(r"^##\s+(.*?)\s*$", line)
        if m:
            if cur is not None:
                out[cur] = "\n".join(buf).strip()
            cur = m.group(1).strip().lower()
            buf = []
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        out[cur] = "\n".join(buf).strip()
    return out


def parse_criteria(rubric_path):
    """Return [(key, description), ...] in document order."""
    with open(rubric_path, encoding="utf-8") as f:
        secs = _sections(f.read())
    body = None
    for head, b in secs.items():
        if head.startswith("criteria"):
            body = b
            break
    if body is None:
        raise ValueError("RUBRIC.md has no '## Criteria' section: %s" % rubric_path)
    crits = []
    for line in body.splitlines():
        m = re.match(r"^-\s+([A-Za-z0-9_]+)\s*:\s*(.*)$", line)
        if m:
            crits.append((m.group(1), m.group(2).strip()))
    if not crits:
        raise ValueError("no '- key: desc' criteria found in %s" % rubric_path)
    return crits


def parse_ground_truth(rubric_path):
    """Return the ground-truth prose (may be empty string)."""
    with open(rubric_path, encoding="utf-8") as f:
        secs = _sections(f.read())
    for head, body in secs.items():
        if head.startswith("ground truth"):
            return body
    return ""
