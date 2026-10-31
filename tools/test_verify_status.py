import os
import pathlib
import shutil
import subprocess
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import verify_status as vs  # noqa: E402

SCRIPT = os.path.join(HERE, "verify_status.py")
TEMPLATE = os.path.join(HERE, "..", "templates", "docs", "backlog.md")

HEADER = ("| ID | Title | Type | Status | Owner | Risk tier | Blocked by | Evidence "
          "| Evidence kind | Approvals |\n|---|---|---|---|---|---|---|---|---|---|\n")
DEFAULTS = dict(id="B-1", title="t", type="build", status="ready", owner="alice",
                tier="local", blocked="", evidence="", kind="computational", approvals="")


@pytest.fixture
def tmp_path(request):
    """Scratch folder inside the repo, removed after the test."""
    path = os.path.join(HERE, ".test-scratch", request.node.name.replace("/", "_"))
    shutil.rmtree(path, ignore_errors=True)
    os.makedirs(path)
    yield pathlib.Path(path)
    shutil.rmtree(os.path.join(HERE, ".test-scratch"), ignore_errors=True)


def table(*rows):
    lines = []
    for r in rows:
        d = {**DEFAULTS, **r}
        lines.append("| {id} | {title} | {type} | {status} | {owner} | {tier} | {blocked} "
                     "| {evidence} | {kind} | {approvals} |".format(**d))
    return HEADER + "\n".join(lines) + "\n"


def problems(*rows, **kw):
    return vs.check_rows(vs.parse_backlog(table(*rows)), **kw)


def run(path, *extra):
    return subprocess.run([sys.executable, SCRIPT, str(path), *extra],
                          capture_output=True, text=True)


DONE_LOCAL = dict(status="done", evidence="https://ci.example.com/runs/1",
                  approvals="change:alice@2026-10-01")


# Rule: IDs unique and present

def test_unique_ids_pass():
    assert problems(dict(id="B-1"), dict(id="B-2")) == []


def test_duplicate_id_fails():
    assert problems(dict(id="B-1"), dict(id="B-1")) == ["B-1: duplicate ID"]


def test_missing_id_fails():
    assert any("missing ID" in p for p in problems(dict(id="")))


# Rule: status values are exact

@pytest.mark.parametrize("status", vs.STATUSES)
def test_every_valid_status_passes(status):
    row = dict(status=status, blocked="X since 2026-10-01", **{
        k: v for k, v in DONE_LOCAL.items() if k != "status"})
    assert problems(row) == []


@pytest.mark.parametrize("status", ["Done", "in progress", "deployed", "done (verified)", ""])
def test_invalid_status_fails(status):
    assert any("invalid status" in p for p in problems(dict(status=status)))


def test_invalid_type_tier_and_kind_fail():
    out = problems(dict(type="feature", tier="high", kind="vibes"))
    assert len(out) == 3


# Rule: done needs evidence that is a link or path

@pytest.mark.parametrize("evidence", [
    "https://ci.example.com/runs/1",
    "[run](https://ci.example.com/runs/1)",
    "`evidence/B-1.txt`",
    "reports/check.log",
    "[proof](proof.md#section)",
])
def test_done_with_link_or_path_passes(evidence):
    assert problems({**DONE_LOCAL, "evidence": evidence}) == []


@pytest.mark.parametrize("evidence,msg", [
    ("", "done without evidence"),
    ("it works, checked by the pipeline", "is not a link or path"),
])
def test_done_without_usable_evidence_fails(evidence, msg):
    out = problems({**DONE_LOCAL, "evidence": evidence})
    assert len(out) == 1 and msg in out[0]


def test_check_paths(tmp_path):
    (tmp_path / "evidence").mkdir()
    (tmp_path / "evidence" / "ok.txt").write_text("ok")
    rows = vs.parse_backlog(table({**DONE_LOCAL, "evidence": "evidence/ok.txt"},
                                  {**DONE_LOCAL, "id": "B-2", "evidence": "evidence/no.txt"}))
    out = vs.check_rows(rows, check_paths=True, backlog_dir=str(tmp_path), root=str(tmp_path))
    assert out == ["B-2: evidence path 'evidence/no.txt' does not exist"]
    # Without --check-paths the missing file is not reported.
    assert vs.check_rows(rows) == []


def test_check_paths_ignores_urls(tmp_path):
    rows = vs.parse_backlog(table(DONE_LOCAL))
    assert vs.check_rows(rows, check_paths=True, backlog_dir=str(tmp_path),
                         root=str(tmp_path)) == []


# Rule: approvals cover the gates for the status and risk tier

PLAN = "plan:alice@2026-10-01"
CHANGE = "change:bob@2026-10-02"
REL2 = "release:carol@2026-10-03; release:dave@2026-10-03"


@pytest.mark.parametrize("tier,approvals", [
    ("local", CHANGE),
    ("shared", f"{PLAN}; {CHANGE}"),
    ("shared", "plan:alice@2026-10-01; change:alice@2026-10-02"),
    ("irreversible", f"{PLAN}; {CHANGE}; {REL2}"),
])
def test_done_approvals_cover_tier_pass(tier, approvals):
    assert problems({**DONE_LOCAL, "tier": tier, "approvals": approvals}) == []


@pytest.mark.parametrize("tier,approvals,msg", [
    ("local", "", "needs a 'change' (or expedite) approval"),
    ("local", PLAN, "needs a 'change' (or expedite) approval"),
    ("shared", CHANGE, "needs a 'plan' (or expedite) approval"),
    ("irreversible", f"{PLAN}; {CHANGE}", "needs a 'release' (or expedite) approval"),
    ("", PLAN, "done without a risk tier"),
    ("", PLAN, "needs a 'change' (or expedite) approval"),
])
def test_done_approvals_short_of_tier_fail(tier, approvals, msg):
    out = problems({**DONE_LOCAL, "tier": tier, "approvals": approvals})
    assert any(msg in p for p in out), out


def test_release_needs_two_distinct_release_approvers():
    # Two distinct approvers overall is not enough; they must both approve the release.
    one_releaser = f"{PLAN}; {CHANGE}; release:carol@2026-10-03"
    out = problems({**DONE_LOCAL, "tier": "irreversible", "approvals": one_releaser})
    assert out == ["B-1: irreversible tier needs release or expedite approvals from at least "
                   "2 distinct approvers, found 1"]
    same_twice = f"{PLAN}; {CHANGE}; release:carol@2026-10-03; release:carol@2026-10-04"
    out = problems({**DONE_LOCAL, "tier": "irreversible", "approvals": same_twice})
    assert any("found 1" in p for p in out), out


@pytest.mark.parametrize("tier,approvals", [
    ("local", "expedite:erin@2026-10-05"),
    ("shared", "expedite:erin@2026-10-05"),
    ("irreversible", f"expedite:erin@2026-10-05; {REL2}"),
    ("shared", f"{PLAN}; expedite:erin@2026-10-05"),
])
def test_expedite_counts_as_plan_change_and_release(tier, approvals):
    assert problems({**DONE_LOCAL, "tier": tier, "approvals": approvals}) == []


def test_irreversible_expedite_plus_second_human_release_passes():
    approvals = "expedite:alice@2026-10-05; release:bob@2026-10-06"
    assert problems({**DONE_LOCAL, "tier": "irreversible", "approvals": approvals}) == []


def test_irreversible_expedite_alone_fails():
    out = problems({**DONE_LOCAL, "tier": "irreversible",
                    "approvals": "expedite:alice@2026-10-05"})
    assert out == ["B-1: irreversible tier needs release or expedite approvals from at least "
                   "2 distinct approvers, found 1"]


def test_irreversible_expedite_and_release_by_same_human_fails():
    approvals = "expedite:alice@2026-10-05; release:alice@2026-10-06"
    out = problems({**DONE_LOCAL, "tier": "irreversible", "approvals": approvals})
    assert any("found 1" in p for p in out), out


def test_inferential_done_needs_evidence_gate():
    row = {**DONE_LOCAL, "kind": "inferential"}
    assert problems(row) == ["B-1: inferential evidence needs an 'evidence' approval"]
    row["approvals"] = f"{CHANGE}; evidence:frank@2026-10-06"
    assert problems(row) == []


def test_inferential_not_done_needs_no_evidence_gate():
    assert problems(dict(status="in-review", kind="inferential")) == []


@pytest.mark.parametrize("tier", ["local", "shared", "irreversible"])
def test_merged_needs_change(tier):
    out = problems(dict(status="merged", tier=tier, approvals=PLAN))
    assert out == [f"B-1: merged item with {tier} risk tier needs a 'change' (or expedite) "
                   "approval"]
    assert problems(dict(status="merged", tier=tier, approvals=f"{PLAN}; {CHANGE}")) == []


@pytest.mark.parametrize("status", ["in-progress", "in-review", "merged"])
@pytest.mark.parametrize("tier", ["shared", "irreversible"])
def test_started_shared_or_irreversible_needs_plan(status, tier):
    out = problems(dict(status=status, tier=tier, approvals=CHANGE))
    assert any("needs a 'plan' (or expedite) approval" in p for p in out), out
    assert problems(dict(status=status, tier=tier, approvals=f"{PLAN}; {CHANGE}")) == []
    assert problems(dict(status=status, tier=tier,
                         approvals="expedite:erin@2026-10-05")) == []


@pytest.mark.parametrize("status", ["in-progress", "in-review"])
def test_started_local_needs_no_plan(status):
    assert problems(dict(status=status, tier="local")) == []


@pytest.mark.parametrize("status", ["proposed", "ready", "blocked", "dropped"])
def test_no_approvals_needed_before_work_starts(status):
    assert problems(dict(status=status, tier="irreversible",
                         blocked="B-9 since 2026-10-01")) == []


@pytest.mark.parametrize("approvals,msg", [
    ("change alice 2026-10-01", "malformed approval"),
    ("change:alice@01-10-2026", "malformed approval"),
    ("build:alice@2026-10-01", "unknown gate 'build'"),
    ("review:alice@2026-10-01", "unknown gate 'review'"),
])
def test_malformed_approvals_fail_on_any_row(approvals, msg):
    out = problems(dict(status="ready", approvals=approvals))
    assert any(msg in p for p in out), out


@pytest.mark.parametrize("gate", vs.GATES)
def test_every_gate_name_parses(gate):
    entries, errors = vs.parse_approvals(f"{gate}:alice@2026-10-01")
    assert errors == [] and entries == [(gate, "alice", "2026-10-01")]


# Rule: blocked rows have Blocked by with a date

def test_blocked_with_date_passes():
    assert problems(dict(status="blocked", blocked="B-7, external request since 2026-10-04")) == []


@pytest.mark.parametrize("blocked,msg", [
    ("", "blocked without Blocked by"),
    ("waiting on B-7", "has no date"),
])
def test_blocked_without_date_fails(blocked, msg):
    out = problems(dict(status="blocked", blocked=blocked))
    assert len(out) == 1 and msg in out[0]


# Rule: done decision items reference an ADR

def test_done_decision_with_adr_passes():
    row = {**DONE_LOCAL, "type": "decision",
           "evidence": "[ADR](docs/decisions/0001-choose-identity-provider.md)"}
    assert problems(row) == []


def test_done_decision_without_adr_fails():
    out = problems({**DONE_LOCAL, "type": "decision"})
    assert out == ["B-1: done decision item does not reference an ADR (decisions/NNNN-title.md)"]


def test_open_decision_needs_no_adr():
    assert problems(dict(type="decision", status="in-progress")) == []


# Parsing and exit codes

def test_summary_table_is_skipped():
    text = "| Status | Count |\n|---|---|\n| done | 1 |\n\n" + table(DONE_LOCAL)
    assert len(vs.parse_backlog(text)) == 1


def test_escaped_pipe_in_cell():
    rows = vs.parse_backlog(table(dict(title="a \\| b")))
    assert rows[0].get("title") == "a | b"


def test_exit_codes(tmp_path):
    good = tmp_path / "good.md"
    good.write_text(table(DONE_LOCAL))
    assert run(good).returncode == 0

    bad = tmp_path / "bad.md"
    bad.write_text(table(dict(status="finished")))
    result = run(bad)
    assert result.returncode == 1
    assert result.stdout.startswith("B-1: invalid status 'finished'")

    assert run(tmp_path / "missing.md").returncode == 2

    no_table = tmp_path / "none.md"
    no_table.write_text("# Backlog\n\nnothing here\n")
    assert run(no_table).returncode == 2

    missing_col = tmp_path / "cols.md"
    missing_col.write_text("| ID | Status |\n|---|---|\n| B-1 | done |\n")
    result = run(missing_col)
    assert result.returncode == 2 and "missing columns" in result.stderr

    ragged = tmp_path / "ragged.md"
    ragged.write_text(HEADER + "| B-1 | t |\n")
    assert run(ragged).returncode == 2

    assert run(good, "--no-such-flag").returncode == 2


def test_template_backlog_passes():
    result = run(TEMPLATE)
    assert result.returncode == 0, result.stdout + result.stderr
