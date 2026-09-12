#!/usr/bin/env python3
"""Validate SKILL.md files against the Agent Skills specification.

Offline stand-in for `npx skills-ref validate`. Checks the constraints that
actually break agent discovery:
  - frontmatter starts at byte 0 and is properly closed
  - only spec keys: name, description, license, allowed-tools, metadata, compatibility
  - name matches the containing directory
  - description present and non-trivial
  - body non-empty

Usage: python scripts/validate_skill.py
"""
import pathlib
import re
import sys
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
ALLOWED = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}


def check(path):
    errs = []
    raw = path.read_bytes()
    if not raw.startswith(b"---"):
        return ["frontmatter must start at byte 0 with ---"]
    text = raw.decode("utf-8")
    end = text.find("\n---", 3)
    if end == -1:
        return ["frontmatter is not closed with ---"]
    block, body = text[3:end], text[end + 4 :]

    keys = []
    for line in block.splitlines():
        m = re.match(r"^([A-Za-z][A-Za-z0-9-]*):", line)
        if m:
            keys.append(m.group(1))
    unexpected = sorted(set(keys) - ALLOWED)
    if unexpected:
        errs.append(f"unexpected frontmatter keys: {', '.join(unexpected)}")
    for required in ("name", "description"):
        if required not in keys:
            errs.append(f"missing required key: {required}")

    m = re.search(r"^name:\s*(.+)$", block, re.M)
    if m:
        name = m.group(1).strip().strip("'\"")
        slug = path.parent.name
        if unicodedata.normalize("NFKC", name) != unicodedata.normalize("NFKC", slug):
            errs.append(f"name '{name}' does not match directory '{slug}'")

    m = re.search(r"^description:\s*(.*)$", block, re.M)
    if m and len(m.group(1).strip()) < 2 and ">" not in m.group(1):
        errs.append("description is empty")

    if not body.strip():
        errs.append("body is empty")
    return errs


def main():
    skills = sorted(ROOT.glob("skills/*/SKILL.md"))
    if not skills:
        print("no skills found", file=sys.stderr)
        return 1
    failed = False
    for s in skills:
        errs = check(s)
        rel = s.relative_to(ROOT)
        if errs:
            failed = True
            print(f"FAIL {rel}")
            for e in errs:
                print(f"     - {e}")
        else:
            print(f"OK   {rel}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
