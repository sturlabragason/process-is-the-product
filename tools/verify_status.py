#!/usr/bin/env python3
"""Status verification for a markdown backlog (stage 8 of the method).

Usage:
    python3 tools/verify_status.py [BACKLOG] [--check-paths] [--root DIR]

BACKLOG defaults to docs/backlog.md. The script reads the first markdown table
whose header has both an ``ID`` and a ``Status`` column. Header names are
matched case-insensitively. Other tables (such as the status summary) are
ignored.

Required columns: ID, Type, Status, Risk tier, Blocked by, Evidence, Approvals.
The full field list is in PLAN.md and docs/05-work-item-procedure.md.

Rules (one ``ID: problem`` line is printed per violation):

1. IDs are non-empty and unique.
2. Status is exactly one of: proposed, ready, in-progress, in-review, merged,
   done, blocked, dropped (lower case, no extra words).
3. Type, when filled in, is one of: build, decision, discovery, compliance, ops.
   Risk tier, when filled in, is one of: local, shared, irreversible.
   Evidence kind, when the column exists and is filled in, is computational or
   inferential.
4. A ``done`` row has non-empty Evidence that looks like a link or a path:
   a URL (http or https), a markdown link ``[text](target)``, or a token that
   contains a ``/`` or ends in a file extension. With ``--check-paths`` every
   relative path target must exist, either relative to the backlog file's
   folder or relative to ``--root`` (default: current directory). URLs are not
   fetched.
5. A ``done`` row has a Risk tier.
6. Approvals match the status and the risk tier (see docs/05-work-item-procedure.md, status
   transitions):
       in-progress, in-review, merged, done  shared or irreversible  plan
       merged, done                          every tier              change
       done                                  irreversible            release, from at least
                                                                     two distinct approvers
                                                                     across release and
                                                                     expedite entries
   An ``expedite`` entry (incident path) stands in for ``plan``, ``change`` and
   ``release``. On an irreversible item the backfill adds a second human's
   ``release`` approval, so ``expedite:alice; release:bob`` passes and
   ``expedite:alice`` alone does not.
   A ``blocked`` row is not checked for approvals, because the script cannot see the status it
   had before.
7. A ``done`` row whose Evidence kind is ``inferential`` has an ``evidence`` approval.
8. A ``blocked`` row has a non-empty Blocked by that contains a date
   (YYYY-MM-DD).
9. A ``decision`` row that is ``done`` references an ADR path in its Evidence,
   matching ``decisions/NNNN-title.md``.

Approvals format (the Approvals cell is a compact index):

    gate:who@YYYY-MM-DD; gate:who@YYYY-MM-DD

    gate  one of plan, change, release, launch-readiness, expedite, evidence
    who   the approver's handle, letters, digits, dot, dash or underscore
    date  ISO date of the approval

Example: ``plan:alice@2026-10-01; change:bob@2026-10-02``. Entries are
separated by ``;``. A malformed entry or an unknown gate is a violation on any
row. The full record for each approval, one line
``gate | item | who | when | what exactly was approved | link``, lives in the
approval log docs/approvals.md (template: templates/docs/approvals.md).

What the script cannot check:

- History. It checks the current state of each row, so it cannot prove that
  transitions happened in order or that an approval is dated before the action
  it approves.
- Expedite backfill. A done row whose only plan, change or release coverage
  is an ``expedite`` entry passes (given two distinct humans on an
  irreversible item); whether the rest of the backfill (baseline, evidence,
  retrospective change review, rule from the incident) was completed within
  the window is left to the change approver and the stage 9 audit.
- Launch readiness. Whether a release is the first production release, and so
  needs a ``launch-readiness`` entry, is not visible in the backlog.
- That the second release approver is not the owner or the author.
- That the evidence proves the claim; only that it is a link or a path.

Exit codes: 0 no violations, 1 violations found, 2 usage or parse error.
Python 3 standard library only.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass, field

STATUSES = (
    "proposed", "ready", "in-progress", "in-review",
    "merged", "done", "blocked", "dropped",
)
TYPES = ("build", "decision", "discovery", "compliance", "ops")
RISK_TIERS = ("local", "shared", "irreversible")
EVIDENCE_KINDS = ("computational", "inferential")
GATES = ("plan", "change", "release", "launch-readiness", "expedite", "evidence")
# Gates a done row needs, by risk tier.
REQUIRED_GATES = {
    "local": ("change",),
    "shared": ("plan", "change"),
    "irreversible": ("plan", "change", "release"),
}
PLAN_STATUSES = ("in-progress", "in-review", "merged", "done")
PLAN_TIERS = ("shared", "irreversible")
CHANGE_STATUSES = ("merged", "done")
MIN_RELEASE_APPROVERS = 2
# An expedite record replaces the plan, change and release records on the incident path.
EXPEDITE_COVERS = ("plan", "change", "release")
# Gates whose approvers count toward MIN_RELEASE_APPROVERS.
RELEASE_GATES = ("release", "expedite")

REQUIRED_COLUMNS = (
    "id", "type", "status", "risk tier", "blocked by", "evidence", "approvals",
)

DATE_RE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
APPROVAL_RE = re.compile(
    r"^(?P<gate>[a-z-]+)\s*:\s*(?P<who>[A-Za-z0-9._-]+)\s*@\s*(?P<date>\d{4}-\d{2}-\d{2})$"
)
MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
URL_RE = re.compile(r"https?://\S+")
ADR_RE = re.compile(r"decisions/\d{4}-[A-Za-z0-9._-]+\.md")
PATHLIKE_RE = re.compile(r"^[\w.~-][\w./~#-]*(/[\w.#-]+|\.[A-Za-z0-9]{1,6})(#[\w-]*)?$")


class ParseError(Exception):
    pass


@dataclass
class Row:
    line: int
    cells: dict = field(default_factory=dict)

    def get(self, name: str) -> str:
        return self.cells.get(name, "").strip()


def split_row(line: str) -> list[str]:
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    parts = re.split(r"(?<!\\)\|", s)
    return [p.strip().replace("\\|", "|") for p in parts]


def is_separator(line: str) -> bool:
    cells = split_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", c) for c in cells)


def parse_backlog(text: str) -> list[Row]:
    lines = text.splitlines()
    i = 0
    while i < len(lines) - 1:
        if lines[i].lstrip().startswith("|") and is_separator(lines[i + 1]):
            header = [h.lower().strip("* `") for h in split_row(lines[i])]
            if "id" in header and "status" in header:
                missing = [c for c in REQUIRED_COLUMNS if c not in header]
                if missing:
                    raise ParseError(
                        "backlog table is missing columns: " + ", ".join(missing))
                rows = []
                j = i + 2
                while j < len(lines) and lines[j].lstrip().startswith("|"):
                    cells = split_row(lines[j])
                    if len(cells) != len(header):
                        raise ParseError(
                            f"line {j + 1}: expected {len(header)} cells, got {len(cells)}")
                    rows.append(Row(line=j + 1, cells=dict(zip(header, cells))))
                    j += 1
                return rows
        i += 1
    raise ParseError("no markdown table with ID and Status columns found")


def strip_code(value: str) -> str:
    return value.replace("`", "").strip()


def evidence_targets(evidence: str) -> list[str]:
    """Return the link or path targets found in an Evidence cell."""
    targets = MD_LINK_RE.findall(evidence)
    rest = MD_LINK_RE.sub(" ", evidence)
    targets += URL_RE.findall(rest)
    rest = URL_RE.sub(" ", rest)
    for token in re.split(r"[\s,;]+", strip_code(rest)):
        if token and PATHLIKE_RE.match(token):
            targets.append(token)
    return targets


def parse_approvals(cell: str) -> tuple[list[tuple[str, str, str]], list[str]]:
    entries, errors = [], []
    for raw in cell.split(";"):
        item = strip_code(raw)
        if not item:
            continue
        m = APPROVAL_RE.match(item)
        if not m:
            errors.append(f"malformed approval '{item}' (expected gate:who@YYYY-MM-DD)")
            continue
        if m["gate"] not in GATES:
            errors.append(f"unknown gate '{m['gate']}' in approval '{item}'")
            continue
        entries.append((m["gate"], m["who"], m["date"]))
    return entries, errors


def path_exists(target: str, backlog_dir: str, root: str) -> bool:
    path = target.split("#", 1)[0]
    if not path:
        return True
    if os.path.isabs(path):
        return os.path.exists(path)
    return any(os.path.exists(os.path.join(base, path)) for base in (backlog_dir, root))


def check_rows(rows: list[Row], check_paths: bool = False,
               backlog_dir: str = ".", root: str = ".") -> list[str]:
    problems: list[str] = []
    seen: set[str] = set()

    for row in rows:
        rid = strip_code(row.get("id"))
        label = rid or f"line {row.line}"

        def bad(msg: str) -> None:
            problems.append(f"{label}: {msg}")

        if not rid:
            bad("missing ID")
        elif rid in seen:
            bad("duplicate ID")
        seen.add(rid)

        status = strip_code(row.get("status"))
        rtype = strip_code(row.get("type"))
        tier = strip_code(row.get("risk tier"))
        kind = strip_code(row.get("evidence kind"))
        evidence = row.get("evidence")
        blocked_by = row.get("blocked by")

        if status not in STATUSES:
            bad(f"invalid status '{status}' (allowed: {', '.join(STATUSES)})")
        if rtype and rtype not in TYPES:
            bad(f"invalid type '{rtype}' (allowed: {', '.join(TYPES)})")
        if tier and tier not in RISK_TIERS:
            bad(f"invalid risk tier '{tier}' (allowed: {', '.join(RISK_TIERS)})")
        if kind and kind not in EVIDENCE_KINDS:
            bad(f"invalid evidence kind '{kind}' (allowed: {', '.join(EVIDENCE_KINDS)})")

        approvals, approval_errors = parse_approvals(row.get("approvals"))
        for err in approval_errors:
            bad(err)
        have = {g for g, _, _ in approvals}

        if status == "done":
            targets = evidence_targets(evidence)
            if not evidence:
                bad("done without evidence")
            elif not targets:
                bad(f"evidence '{evidence}' is not a link or path")
            elif check_paths:
                for t in targets:
                    if not URL_RE.match(t) and not path_exists(t, backlog_dir, root):
                        bad(f"evidence path '{t}' does not exist")

            if not tier:
                bad("done without a risk tier")
            if kind == "inferential" and "evidence" not in have:
                bad("inferential evidence needs an 'evidence' approval")

        if status == "done" and tier in REQUIRED_GATES:
            needed = list(REQUIRED_GATES[tier])
        else:
            needed = []
            if status in PLAN_STATUSES and tier in PLAN_TIERS:
                needed.append("plan")
            if status in CHANGE_STATUSES:
                needed.append("change")
        for gate in needed:
            if gate in have or (gate in EXPEDITE_COVERS and "expedite" in have):
                continue
            alt = " (or expedite)" if gate in EXPEDITE_COVERS else ""
            bad(f"{status} item with {tier or 'no'} risk tier needs a '{gate}'{alt} approval")
        if status == "done" and tier == "irreversible":
            release_by = {who for g, who, _ in approvals if g in RELEASE_GATES}
            if len(release_by) < MIN_RELEASE_APPROVERS:
                bad(f"irreversible tier needs release or expedite approvals from at least "
                    f"{MIN_RELEASE_APPROVERS} distinct approvers, found {len(release_by)}")

        if status == "done" and rtype == "decision" and not ADR_RE.search(evidence):
            bad("done decision item does not reference an ADR (decisions/NNNN-title.md)")

        if status == "blocked":
            if not blocked_by:
                bad("blocked without Blocked by")
            elif not DATE_RE.search(blocked_by):
                bad("Blocked by has no date (YYYY-MM-DD)")

    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify backlog status values, evidence and approvals.")
    parser.add_argument("backlog", nargs="?", default="docs/backlog.md")
    parser.add_argument("--check-paths", action="store_true",
                        help="check that relative evidence paths exist")
    parser.add_argument("--root", default=".",
                        help="project root for resolving evidence paths (default: .)")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code == 0 else 2

    try:
        with open(args.backlog, encoding="utf-8") as fh:
            text = fh.read()
    except OSError as exc:
        print(f"error: cannot read {args.backlog}: {exc.strerror}", file=sys.stderr)
        return 2
    try:
        rows = parse_backlog(text)
    except ParseError as exc:
        print(f"error: {args.backlog}: {exc}", file=sys.stderr)
        return 2

    problems = check_rows(rows, args.check_paths,
                          os.path.dirname(os.path.abspath(args.backlog)), args.root)
    for p in problems:
        print(p)
    if problems:
        print(f"{len(problems)} problem(s) in {len(rows)} row(s)", file=sys.stderr)
        return 1
    print(f"ok: {len(rows)} row(s) checked", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
