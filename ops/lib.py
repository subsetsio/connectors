"""Shared plumbing for operate: R2 reads, GitHub dispatch, observation, policy.

THE DEPENDENCY RULE — operate reads ONLY the production substrates:

  * R2: run records the workflow itself wrote (`<slug>/runs/<run_id>/run.json`),
    the production gate (`production_enabled_sources.txt`, bucket root), and
    operate's own `_operate/status.json`.
  * GitHub API: workflow dispatch + the in-flight run list.
  * The connectors repo tree: per-connector `maintenance.json` contracts
    (local checkout via OPERATE_CONNECTORS_DIR, else the contents API).

Never import factory code, never read factory/data/sources. Operate must give
identical answers from any machine, including a GitHub Actions runner.

Protocol facts mirrored from the connectors repo + workflow (keep in sync):
  * workflow file `run.yml`, run-name `<slug> :: <run_id>`, per-slug
    concurrency group (a duplicate dispatch replaces any still-pending
    duplicate in the group and queues behind a running one; a RUNNING run
    is never cancelled — `cancel-in-progress: false`).
  * dispatch inputs: {slug, run_id, dag_on_failure: "continue"}.
  * run_id format: UTC `%Y%m%d-%H%M%S` (lexicographic == chronological).
  * run.json `status`: done | done_with_failures | failed | needs_continuation.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone

import boto3
import requests

GATE_KEY = "production_enabled_sources.txt"  # bucket root; platform mirrors it
STATUS_KEY = "_operate/status.json"
WORKFLOW_FILE = "run.yml"
RUN_NAME_SEP = " :: "
RUN_ID_FORMAT = "%Y%m%d-%H%M%S"

# How many recent run.json documents to read per connector each tick. Enough
# to see a failure streak; small enough to keep a ~250-connector tick fast.
SCAN_RUNS = 5
# Hard-failure streak that stops dispatching (repair is factory's job).
AUTO_HOLD_AFTER = 3

DEFAULT_CADENCE_DAYS = int(os.environ.get("OPERATE_DEFAULT_CADENCE_DAYS", "7"))
# The dispatch limit exists only to bound a runaway tick, so it is sized well
# ABOVE sustained demand, never below it: ~230 connectors on a 7-day cadence
# is ~34 due per day, and a "wasted" dispatch costs minutes by design. An
# under-demand limit silently starves the fleet into `stale`.
DEFAULT_DISPATCH_LIMIT = int(os.environ.get("OPERATE_DISPATCH_LIMIT", "50"))

# GH Actions is free on the public connectors repo; this prices what the runs
# WOULD cost on paid GH-hosted linux runners ($0.008/min), from the run.json's
# own connector wall-clock (a lower bound of the billed job time — setup steps
# and per-job minute rounding aren't visible from R2).
GHA_LINUX_USD_PER_MIN = 0.008


def env(name: str, *alts: str) -> str:
    for key in (name, *alts):
        val = os.environ.get(key)
        if val:
            return val
    raise SystemExit(f"operate requires the {name} environment variable")


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def parse_iso(iso: str | None) -> datetime | None:
    if not iso:
        return None
    try:
        t = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    return t if t.tzinfo else t.replace(tzinfo=timezone.utc)


def age_days(iso: str | None) -> float | None:
    t = parse_iso(iso)
    if t is None:
        return None
    return (utcnow() - t).total_seconds() / 86400.0


# ---- R2 ---------------------------------------------------------------------


class R2:
    """Minimal R2 (S3-compatible) reader/writer over the connectors bucket."""

    def __init__(self):
        self.bucket = env("R2_BUCKET_NAME")
        self.prefix = os.environ.get("R2_PREFIX", "").strip("/")
        self.client = boto3.client(
            "s3",
            endpoint_url=f"https://{env('R2_ACCOUNT_ID')}.r2.cloudflarestorage.com",
            aws_access_key_id=env("R2_ACCESS_KEY_ID"),
            aws_secret_access_key=env("R2_SECRET_ACCESS_KEY"),
            region_name="auto",
        )

    def _slug_key(self, slug: str, *parts: str) -> str:
        base = f"{self.prefix}/{slug}" if self.prefix else slug
        return "/".join([base, *parts])

    def get_text(self, key: str) -> str | None:
        try:
            body = self.client.get_object(Bucket=self.bucket, Key=key)["Body"].read()
        except self.client.exceptions.NoSuchKey:
            return None
        except self.client.exceptions.ClientError as e:
            if e.response.get("Error", {}).get("Code") in ("404", "NoSuchKey", "NotFound"):
                return None
            raise
        return body.decode("utf-8", errors="replace")

    def get_json(self, key: str) -> dict | None:
        text = self.get_text(key)
        if text is None:
            return None
        try:
            doc = json.loads(text)
        except json.JSONDecodeError:
            return None
        return doc if isinstance(doc, dict) else None

    def put_json(self, key: str, doc: dict) -> None:
        self.client.put_object(
            Bucket=self.bucket, Key=key,
            Body=json.dumps(doc, indent=2).encode(),
            ContentType="application/json",
        )

    def production_gate(self) -> list[str]:
        text = self.get_text(GATE_KEY)
        if text is None:
            raise SystemExit(
                f"no production gate at s3://{self.bucket}/{GATE_KEY} — "
                "nothing is production-enabled (factory scripts/publish_sources.py owns it)"
            )
        return sorted(
            line.strip() for line in text.splitlines()
            if line.strip() and not line.strip().startswith("#")
        )

    def list_run_ids(self, slug: str) -> list[str]:
        """run_ids under `<slug>/runs/`, newest first (ids are UTC timestamps)."""
        prefix = self._slug_key(slug, "runs") + "/"
        ids: list[str] = []
        paginator = self.client.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=self.bucket, Prefix=prefix, Delimiter="/"):
            for cp in page.get("CommonPrefixes", []):
                rid = cp["Prefix"][len(prefix):].strip("/")
                if rid:
                    ids.append(rid)
        return sorted(ids, reverse=True)

    def run_json(self, slug: str, run_id: str) -> dict | None:
        return self.get_json(self._slug_key(slug, "runs", run_id, "run.json"))


# ---- GitHub -----------------------------------------------------------------


class GitHub:
    """Workflow dispatch + in-flight discovery on the connectors repo."""

    def __init__(self):
        self.repo = env("HARNESS_CONNECTORS_REPO")
        token = env("GH_TOKEN", "GITHUB_TOKEN")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        })

    def _req(self, method: str, path: str, **kw):
        r = self.session.request(
            method, f"https://api.github.com/repos/{self.repo}{path}",
            timeout=30, **kw,
        )
        r.raise_for_status()
        return r

    def in_flight(self) -> dict[str, dict]:
        """slug -> {run_id, url} for every queued/in-progress run.yml run.

        Paginated: during a backlog drain more than 100 runs can be queued,
        and a slug missed here would be re-dispatched as a duplicate."""
        out: dict[str, dict] = {}
        for status in ("queued", "in_progress"):
            page = 1
            while True:
                runs = self._req(
                    "GET", f"/actions/workflows/{WORKFLOW_FILE}/runs",
                    params={"status": status, "per_page": 100, "page": page},
                ).json().get("workflow_runs", [])
                for run in runs:
                    name = run.get("name") or ""
                    if RUN_NAME_SEP not in name:
                        continue
                    slug, run_id = name.split(RUN_NAME_SEP, 1)
                    out.setdefault(slug.strip(), {
                        "run_id": run_id.strip(), "url": run.get("html_url"),
                    })
                if len(runs) < 100:
                    break
                page += 1
        return out

    def dispatch(self, slug: str) -> str:
        run_id = utcnow().strftime(RUN_ID_FORMAT)
        self._req("POST", f"/actions/workflows/{WORKFLOW_FILE}/dispatches", json={
            "ref": "main",
            "inputs": {"slug": slug, "run_id": run_id, "dag_on_failure": "continue"},
        })
        return run_id


# ---- maintenance contract -----------------------------------------------------


def maintenance_contract(slug: str, gh: GitHub | None = None) -> dict:
    """The connector's `maintenance.json`, from the local checkout when
    OPERATE_CONNECTORS_DIR is set, else the GitHub contents API. Absent or
    malformed degrades to defaults — a bad contract must never stall the tick."""
    raw: dict = {}
    root = os.environ.get("OPERATE_CONNECTORS_DIR")
    if root:
        path = os.path.join(root, "src", slug, "maintenance.json")
        try:
            with open(path, encoding="utf-8") as f:
                doc = json.load(f)
            raw = doc if isinstance(doc, dict) else {}
        except (OSError, json.JSONDecodeError):
            raw = {}
    elif gh is not None:
        try:
            r = gh._req(
                "GET", f"/contents/src/{slug}/maintenance.json",
                headers={"Accept": "application/vnd.github.raw+json"},
            )
            doc = json.loads(r.text)
            raw = doc if isinstance(doc, dict) else {}
        except (requests.HTTPError, json.JSONDecodeError):
            raw = {}

    days = raw.get("cadence_days")
    if isinstance(days, bool) or not isinstance(days, (int, float)) or days <= 0:
        days = DEFAULT_CADENCE_DAYS
    return {
        "cadence_days": int(days),
        "paused": bool(raw.get("paused")),
        "cadence_note": raw.get("cadence_note") if isinstance(raw.get("cadence_note"), str) else None,
    }


# ---- observation --------------------------------------------------------------


CONCLUDED = ("done", "done_with_failures", "failed")


@dataclass
class Observation:
    slug: str
    runs: list[dict] = field(default_factory=list)  # newest first, scanned window
    last_concluded_at: str | None = None            # done | done_with_failures
    latest: dict | None = None                      # newest scanned run
    consecutive_hard_failures: int = 0
    data_last_changed_at: str | None = None
    never_ran: bool = False
    newest_run_id: str | None = None                # newest run dir on R2, run.json or not


def _data_changed(run_doc: dict) -> bool:
    """Whether this run actually changed published data: any node outcome
    `ran_changed`, or any materialization not marked skip-unchanged."""
    for node in (run_doc.get("dag") or {}).get("nodes") or []:
        if node.get("outcome") == "ran_changed":
            return True
        for m in node.get("materializations") or []:
            if isinstance(m, dict) and "version" in m and not m.get("unchanged"):
                return True
    return False


def observe(r2: R2, slug: str, in_flight_run_id: str | None) -> Observation:
    """Read the newest SCAN_RUNS run records for one connector off R2.

    `needs_continuation` with a live GH run is just "still going" (skipped via
    in_flight_run_id); with no live run it's a dead self-retrigger chain and
    counts as a hard failure. A run dir with no run.json (dispatch that never
    started, or just-started) is skipped — GH in-flight is the authority there.
    """
    obs = Observation(slug=slug)
    run_ids = r2.list_run_ids(slug)
    if not run_ids:
        obs.never_ran = True
        return obs
    obs.newest_run_id = run_ids[0]

    streak_open = True
    for rid in run_ids[:SCAN_RUNS]:
        doc = r2.run_json(slug, rid)
        if doc is None:
            continue
        status = doc.get("status")
        if rid == in_flight_run_id:
            continue  # live run: not evidence of anything yet
        if status == "needs_continuation":
            status = "failed"  # not live on GH: a dead self-retrigger chain
        if status not in CONCLUDED:
            continue

        changed = _data_changed(doc)
        started, finished = parse_iso(doc.get("started_at")), parse_iso(doc.get("finished_at"))
        minutes = ((finished - started).total_seconds() / 60.0
                   if started and finished and finished >= started else None)
        summary = {
            "run_id": rid,
            "status": status,
            "finished_at": doc.get("finished_at"),
            "url": doc.get("github_run_url"),
            "data_changed": changed,
            "minutes": round(minutes, 1) if minutes is not None else None,
        }
        obs.runs.append(summary)
        if obs.latest is None:
            obs.latest = summary
        if status in ("done", "done_with_failures") and obs.last_concluded_at is None:
            obs.last_concluded_at = doc.get("finished_at")
        if changed and obs.data_last_changed_at is None:
            obs.data_last_changed_at = doc.get("finished_at")
        if streak_open:
            if status == "failed":
                obs.consecutive_hard_failures += 1
            else:
                streak_open = False

    if not obs.runs:
        obs.never_ran = in_flight_run_id is None
    return obs


# ---- policy --------------------------------------------------------------------


def dispatch_lost_streak(obs: Observation, in_flight: dict | None,
                         prev_row: dict, dispatched_run_id: str | None) -> int:
    """Consecutive dispatches that vanished: the previous tick dispatched a
    run_id, but no run dir ever appeared on R2 and nothing is live on GH —
    the run died at the GitHub level before the runner could write run.json
    (broken uv sync, bad apt package, secrets, runner infra). Those leave no
    failure record, so `observe`'s streak never sees them; this synthetic
    streak is persisted through the published status document instead.

    Resets the moment a new run dir reaches R2 (evidence flows through
    run.json again); carried unchanged while there is no new evidence either
    way — including while auto-held, so the hold doesn't self-release.
    Run ids are UTC timestamps, so lexicographic order is chronological.
    """
    prev = prev_row.get("dispatch_lost_streak")
    prev = int(prev) if isinstance(prev, (int, float)) and not isinstance(prev, bool) else 0
    if in_flight:
        return prev  # queued/running on GH: no evidence either way yet
    if dispatched_run_id and (obs.newest_run_id is None or obs.newest_run_id < dispatched_run_id):
        return prev + 1  # dispatched last tick; nothing landed, nothing live
    if obs.newest_run_id and obs.newest_run_id != prev_row.get("newest_run_id"):
        return 0  # a new run reached R2 since the last tick
    return prev


def classify(contract: dict, obs: Observation, in_flight: dict | None,
             lost_streak: int = 0) -> dict:
    """One connector's verdict: attention word + whether to dispatch now.

    Attention: paused | in-flight | auto-held | dispatch-lost | failing |
    degraded | never-ran | due | ok. Exactly one per connector;
    needs_attention marks the ones a human (or a factory repair session)
    should look at. Lost dispatches (see dispatch_lost_streak) count toward
    the auto-hold threshold exactly like hard failures — a connector whose
    runs die before writing run.json must not be re-dispatched forever.
    """
    age = age_days(obs.last_concluded_at)
    due = obs.last_concluded_at is None or (age is not None and age >= contract["cadence_days"])
    stale = age is not None and age >= 2 * contract["cadence_days"]

    if contract["paused"]:
        attention, dispatch = "paused", False
    elif in_flight:
        attention, dispatch = "in-flight", False
    elif obs.consecutive_hard_failures + lost_streak >= AUTO_HOLD_AFTER:
        attention, dispatch = "auto-held", False
    elif lost_streak:
        attention, dispatch = "dispatch-lost", True
    elif obs.never_ran:
        attention, dispatch = "never-ran", True
    elif obs.latest and obs.latest["status"] == "failed":
        attention, dispatch = "failing", due
    elif obs.latest and obs.latest["status"] == "done_with_failures":
        attention, dispatch = "degraded", due
    elif due:
        attention, dispatch = "due", True
    else:
        attention, dispatch = "ok", False

    needs_attention = attention in ("auto-held", "dispatch-lost", "failing",
                                    "degraded", "never-ran") or stale
    return {
        "attention": attention,
        "should_dispatch": dispatch,
        "needs_attention": needs_attention,
        "stale": stale,
        "age_days": round(age, 2) if age is not None else None,
    }


def observe_fleet(r2: R2, gh: GitHub,
                  prev_status: dict | None = None) -> tuple[list[dict], dict[str, dict]]:
    """One row per production-gated connector: contract + observation + verdict.
    Returns (rows, in_flight_map). Dispatching is the caller's job.

    `prev_status` is the previously published status document; it carries the
    per-slug `dispatched` list and lost-dispatch streaks that let this tick
    notice a dispatch that never left a trace on R2 (see dispatch_lost_streak).
    """
    gate = r2.production_gate()
    inflight = gh.in_flight()
    prev_rows: dict[str, dict] = {}
    prev_dispatched: dict[str, str] = {}
    if prev_status:
        prev_rows = {r["slug"]: r for r in prev_status.get("connectors") or []
                     if isinstance(r, dict) and r.get("slug")}
        prev_dispatched = {d["slug"]: d["run_id"] for d in prev_status.get("dispatched") or []
                           if isinstance(d, dict) and d.get("slug") and d.get("run_id")}
    rows: list[dict] = []
    for slug in gate:
        contract = maintenance_contract(slug, gh)
        obs = observe(r2, slug, (inflight.get(slug) or {}).get("run_id"))
        lost = dispatch_lost_streak(obs, inflight.get(slug),
                                    prev_rows.get(slug) or {}, prev_dispatched.get(slug))
        verdict = classify(contract, obs, inflight.get(slug), lost)
        scanned_minutes = sum(r["minutes"] for r in obs.runs if r["minutes"] is not None)
        rows.append({
            "slug": slug,
            **contract,
            "last_ok_at": obs.last_concluded_at,
            "latest": obs.latest,
            "consecutive_failures": obs.consecutive_hard_failures,
            "dispatch_lost_streak": lost,
            "newest_run_id": obs.newest_run_id,
            "data_last_changed_at": obs.data_last_changed_at,
            "in_flight": inflight.get(slug),
            "run_minutes_scanned": round(scanned_minutes, 1),
            "runs_scanned": len(obs.runs),
            **verdict,
        })
    return rows, inflight


def gha_cost(rows: list[dict]) -> dict:
    """Fleet compute footprint over each connector's scanned run window (the
    newest SCAN_RUNS concluded runs): total connector wall-clock minutes and
    what they would cost on paid GH-hosted linux runners. The repo is public,
    so the real bill is $0 — this is the 'what are we consuming' number."""
    minutes = sum(r.get("run_minutes_scanned") or 0 for r in rows)
    runs = sum(r.get("runs_scanned") or 0 for r in rows)
    return {
        "runs_scanned": runs,
        "run_minutes": round(minutes, 1),
        "hypothetical_usd": round(minutes * GHA_LINUX_USD_PER_MIN, 2),
        "usd_per_min": GHA_LINUX_USD_PER_MIN,
        "note": "connector wall-clock from run.json; lower bound of billed job time; public repo → actual cost $0",
    }


# ---- rendering -------------------------------------------------------------------


_ATTENTION_ORDER = ("auto-held", "dispatch-lost", "failing", "degraded", "never-ran",
                    "due", "in-flight", "paused", "ok")


def sort_rows(rows: list[dict]) -> list[dict]:
    rank = {a: i for i, a in enumerate(_ATTENTION_ORDER)}
    return sorted(rows, key=lambda r: (rank.get(r["attention"], 99), r["slug"]))


def render(rows: list[dict]) -> str:
    header = (f"{'connector':34} {'last-ok':>8} {'cad':>5} {'chg':>8} {'min':>7} "
              f"{'fails':>5} {'attention':10}  note")
    lines = [header, "-" * len(header)]
    for r in sort_rows(rows):
        last = f"{r['age_days']:.1f}d" if r["age_days"] is not None else "never"
        chg_age = age_days(r["data_last_changed_at"])
        chg = f"{chg_age:.1f}d" if chg_age is not None else "-"
        latest_min = (r.get("latest") or {}).get("minutes")
        mins = f"{latest_min:.0f}m" if latest_min is not None else "-"
        note = r.get("cadence_note") or ""
        lines.append(
            f"{r['slug']:34} {last:>8} {str(r['cadence_days']) + 'd':>5} {chg:>8} {mins:>7} "
            f"{r['consecutive_failures'] or '-':>5} {r['attention']:10}  {note:.60}"
        )
    tally: dict[str, int] = {}
    for r in rows:
        tally[r["attention"]] = tally.get(r["attention"], 0) + 1
    lines += ["", " · ".join(f"{n} {a}" for a, n in sorted(tally.items(), key=lambda kv: -kv[1]))]
    cost = gha_cost(rows)
    lines.append(
        f"compute (last {SCAN_RUNS} runs/connector): {cost['runs_scanned']} runs · "
        f"{cost['run_minutes']:.0f} min · ~${cost['hypothetical_usd']:.2f} at GH-hosted rates "
        f"(public repo → actually $0)")
    flagged = [r["slug"] for r in rows if r["needs_attention"]]
    if flagged:
        lines.append("needs attention: " + ", ".join(sorted(flagged)))
    return "\n".join(lines)
