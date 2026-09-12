#!/usr/bin/env python3
"""Is the current user allowed to write these paths?

Usage: python scripts/check_owner.py recipes/bread/foo.md [more paths...]
       python scripts/check_owner.py --self-check

Exit 0 when every path is owned by the current user, 1 otherwise. The whitelist is
.github/CODEOWNERS — the same file GitHub enforces on pull requests, so there is no
second list to keep in sync.

This is a guardrail, not security: anyone with a clone can ignore it. Real enforcement
is branch protection with required Code Owner review.
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CODEOWNERS = ROOT / ".github" / "CODEOWNERS"


def rules(text):
    """[(pattern, [owners])] in file order."""
    out = []
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        pattern, *owners = line.split()
        if owners:
            out.append((pattern, owners))
    return out


def matches(pattern, path):
    # ponytail: `*` and directory prefixes only — the forms this repo's CODEOWNERS uses.
    # A real glob (`*.md`, `**/x`) would silently not match; reach for pathspec if you
    # ever write one.
    if pattern == "*":
        return True
    p = pattern.lstrip("/")
    if p.endswith("/"):
        return path.startswith(p)
    return path == p or path.startswith(p + "/")


def owners_for(path, rs):
    """Last matching rule wins, as GitHub does."""
    found = []
    for pattern, owners in rs:
        if matches(pattern, path):
            found = owners
    return found


def whoami():
    for cmd in (
        ["gh", "api", "user", "--jq", ".login"],
        ["git", "config", "github.user"],
    ):
        try:
            handle = subprocess.run(
                cmd, capture_output=True, text=True, timeout=15
            ).stdout.strip()
        except (OSError, subprocess.SubprocessError):
            continue
        if handle:
            return "@" + handle.lstrip("@")
    return None


def self_check():
    rs = rules(
        """
        *            @aviv
        /recipes/    @aviv @dana
        /skills/     @aviv
        # comment    @nobody
        /kitchens/dana/  @dana
        """
    )
    assert owners_for("README.md", rs) == ["@aviv"]
    assert owners_for("recipes/bread/x.md", rs) == ["@aviv", "@dana"]
    assert owners_for("skills/recipe-authoring/SKILL.md", rs) == ["@aviv"]
    assert owners_for("kitchens/dana/x.md", rs) == ["@dana"]
    assert owners_for("kitchens/other/x.md", rs) == ["@aviv"]
    assert "@nobody" not in [o for _, owners in rs for o in owners]
    print("self-check OK")


def main(argv):
    if "--self-check" in argv:
        return self_check()
    if not argv:
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        return 1

    me = whoami()
    if me is None:
        print("cannot resolve a GitHub handle: run `gh auth login`, or "
              "`git config github.user <handle>`", file=sys.stderr)
        return 1

    rs = rules(CODEOWNERS.read_text(encoding="utf-8"))
    bad = 0
    for path in argv:
        path = pathlib.Path(path).as_posix().lstrip("./")
        owners = owners_for(path, rs)
        if me in owners:
            continue
        bad = 1
        print(f"{me} may not write {path} — owned by {' '.join(owners) or 'nobody'}",
              file=sys.stderr)
    if bad:
        print("add a line to .github/CODEOWNERS, or write under kitchens/<handle>/",
              file=sys.stderr)
    return bad


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)
