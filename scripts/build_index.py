#!/usr/bin/env python3
"""Regenerate INDEX.md from the frontmatter of every recipe and guide.

Usage: python scripts/build_index.py
No dependencies beyond the standard library.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIRS = ["recipes", "guides"]
STATUS_MARK = {"favorite": "★", "tested": "✓", "untested": "·"}


def parse_frontmatter(text):
    """Minimal YAML-ish reader. Handles the flat keys this repo uses."""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block, out, current_list = text[3:end], {}, None
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if re.match(r"^\s*-\s", line):
            if current_list is not None:
                out.setdefault(current_list, []).append(line.strip()[2:])
            continue
        m = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if not m:
            continue
        key, value = m.group(1), m.group(2).strip()
        if value == "":
            current_list = key
        else:
            current_list = None
            out[key] = value.strip("'\"")
    return out


def main():
    rows = []
    for d in DIRS:
        for path in sorted((ROOT / d).rglob("*.md")):
            fm = parse_frontmatter(path.read_text(encoding="utf-8"))
            if not fm.get("title_he"):
                print(f"skipped (no frontmatter): {path.relative_to(ROOT)}", file=sys.stderr)
                continue
            rows.append(
                {
                    "he": fm.get("title_he", ""),
                    "en": fm.get("title", ""),
                    "type": fm.get("type", ""),
                    "cuisine": fm.get("cuisine", ""),
                    "status": fm.get("status", "untested"),
                    "time": fm.get("total_time_h", ""),
                    "path": path.relative_to(ROOT).as_posix(),
                }
            )

    rows.sort(key=lambda r: (r["type"], r["he"]))

    lines = [
        "# INDEX",
        "",
        "נוצר אוטומטית על ידי `scripts/build_index.py`. לא לערוך ידנית.",
        "",
        f"סה\"כ: {len(rows)} · ★ מועדף · ✓ נבדק · · לא נבדק",
        "",
        "| | מנה | Title | סוג | מטבח | שעות | קובץ |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        mark = STATUS_MARK.get(r["status"], "·")
        lines.append(
            f"| {mark} | {r['he']} | {r['en']} | {r['type']} | {r['cuisine']} | "
            f"{r['time']} | [{r['path']}]({r['path']}) |"
        )
    lines.append("")

    (ROOT / "INDEX.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"INDEX.md: {len(rows)} entries")


if __name__ == "__main__":
    main()
