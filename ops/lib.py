"""Shared plumbing for operate: R2 reads, GitHub dispatch, observation, policy.

THE DEPENDENCY RULE — operate reads ONLY the production substrates:

  * R2: run records the workflow itself wrote (`<slug>/runs/<run_id>/run.json`),
    the factory-finalize run records (`<slug>/runs/<run_id>/record.json` —
    the stronger verdict file with evidence fields ok/partial/failed_specs;
    written to R2 by the factory poller, so reading it keeps this rule; absent
    until a run is finalized, in which case run.json is the fallback),
    the published source manifest (`_harness/manifest.json` — every source
    record, incl. `enabled` and the `maintenance` contract; compiled from the
    factory records by factory scripts/publish_sources.py), the factory's
    promotion-predicate evaluation (`_harness/gate_report.json`, same script's
    `gate-report`/`sync-evaluated` commands), and operate's own `_operate/`
    documents (`status.json` plus the per-dispatch provenance markers under
    `_operate/dispatched/<slug>/`).
  * GitHub API: workflow dispatch + the in-flight run list.

Never import factory code, never read factory/data/sources. Operate must give
identical answers from any machine, including a GitHub Actions runner.

Protocol facts mirrored from the connectors repo + workflow (keep in sync):
  * workflow file `run.yml`, run-name `<slug> :: <run_id>`, per-slug
    concurrency group (a duplicate dispatch replaces any still-pending
    duplicate in the group and queues behind a running one; a RUNNING run
    is never cancelled — `cancel-in-progress: false`).
  * dispatch inputs: {slug, run_id, dag_on_failure: "continue"}.
  * run_id format: UTC `%Y%m%d-%H%M%S` (lexicographic == chronological, but
    ONLY among conforming ids — anything else in `runs/` is ignored, loudly:
    a stray dir like `infratest4-103525` sorts above every timestamp and
    would otherwise anchor observation forever, issue 092).
  * run.json `status`: done | done_with_failures | failed | needs_continuation.
"""
from __future__ import annotations

import json
import os
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

import boto3
import requests

MANIFEST_KEY = "_harness/manifest.json"  # compiled source records; platform reads it too
GATE_REPORT_KEY = "_harness/gate_report.json"  # promotion predicate over every record; factory owns it
STATUS_KEY = "_operate/status.json"
# Dispatch provenance ledger (S32 rule 4 / problem 039): one small immutable
# marker per dispatch, written AT dispatch time, deleted only once the
# dispatched run leaves a readable record on R2. Unlike the status document's
# `dispatched` list (this tick only) the markers survive any number of ticks,
# hand-run ticks, and status.json loss — a dispatch that vanished STAYS
# evidenced until a real run record supersedes it.
DISPATCH_MARKER_PREFIX = "_operate/dispatched"  # <prefix>/<slug>/<run_id>.json
WORKFLOW_FILE = "run.yml"
RUN_NAME_SEP = " :: "
RUN_ID_FORMAT = "%Y%m%d-%H%M%S"

# How many recent run.json documents to read per connector each tick. Enough
# to see a failure streak; small enough to keep a ~250-connector tick fast.
SCAN_RUNS = 5
# Hard-failure streak that stops dispatching (repair is factory's job).
AUTO_HOLD_AFTER = 3
# Continuation chains that complete legs without landing new raw or publishing
# are wedged, not working. The runtime's own chain guard stops a chain at this
# streak (DAG_MAX_NO_PROGRESS_LEGS=2 in subsets_utils), so operate flags the
# same threshold as attention `wedged-chain` (issue 089). REPORT-ONLY today:
# the flag never changes dispatching or the cadence clock.
WEDGED_CHAIN_AFTER = 2

DEFAULT_CADENCE_DAYS = int(os.environ.get("OPERATE_DEFAULT_CADENCE_DAYS", "7"))
# The dispatch limit exists only to bound a runaway tick, so it is sized well
# ABOVE sustained demand, never below it: ~230 connectors on a 7-day cadence
# is ~34 due per day, and a "wasted" dispatch costs minutes by design. An
# under-demand limit silently starves the fleet into `stale`.
DEFAULT_DISPATCH_LIMIT = int(os.environ.get("OPERATE_DISPATCH_LIMIT", "50"))

# The gate report is fresh evidence, not an archive: past this age the tick
# flags it stale so a stopped factory-side evaluation is itself visible drift.
GATE_REPORT_STALE_DAYS = float(os.environ.get("OPERATE_GATE_REPORT_STALE_DAYS", "2"))

# Re-check bounds for judgments that feed the auto-hold streak (S04 / issue
# 008: resolve status against the NEWEST evidence before caching a failure).
# A needs_continuation record younger than the probe window gets one GH probe
# before it counts as a dead chain — a 6h-capped chain can legitimately show
# needs_continuation for hours while its live leg is invisible to the
# in-flight listing (between legs, or the list API missed it). Older records
# skip the probe: legs cap at 6h, so a chain silent for a week is dead.
CONTINUATION_PROBE_DAYS = 7
# A completed latest leg whose successor hasn't surfaced yet is still alive
# within this grace (the runner dispatches the next leg before exiting, and it
# surfaces within seconds — same window the factory's runtime grants).
CONTINUATION_GRACE_MIN = 15

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


def valid_run_id(rid: str) -> bool:
    """Whether `rid` conforms EXACTLY to RUN_ID_FORMAT (UTC `%Y%m%d-%H%M%S`).
    strptime alone is too lenient (it backtracks over digit widths), so the
    parse must round-trip to the identical fixed-width string."""
    try:
        t = datetime.strptime(rid, RUN_ID_FORMAT)
    except (TypeError, ValueError):
        return False
    return t.strftime(RUN_ID_FORMAT) == rid


def sort_run_ids(ids, slug: str) -> list[str]:
    """Run ids newest first — VALIDATED against RUN_ID_FORMAT, never trusted.

    "Newest" is only meaningful for ids that parse as timestamps; a stray
    non-conforming dir (apple's one-off `infratest4-103525`: 'i' > '2') would
    otherwise sort above every real run forever and anchor the whole
    observation on it (issue 092). Non-conforming ids are SKIPPED — and
    logged loudly, because a silently dropped dir would be S34's
    absence-of-evidence mistake in a new place.
    """
    valid: list[str] = []
    skipped: list[str] = []
    for rid in ids:
        (valid if valid_run_id(rid) else skipped).append(rid)
    if skipped:
        print(f"warning: {slug}: ignoring {len(skipped)} non-timestamp run "
              f"dir(s) under runs/: {', '.join(sorted(skipped))} "
              f"(run ids must be UTC {RUN_ID_FORMAT})", file=sys.stderr)
    # conforming ids are fixed-width digits, so lexicographic == chronological
    return sorted(valid, reverse=True)


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
        """The object's text, or None ONLY when the key does not exist.

        Absence and failure are different answers: a missing key is a real
        state (nothing was written there), while a transient transport/API
        failure is retried and — if it persists — raised. Mapping failures
        to None would let a blip masquerade as "no run record" and feed the
        judgments derived from that (skipped evidence, reset streaks)."""
        last_err: Exception | None = None
        for attempt in range(4):
            try:
                body = self.client.get_object(Bucket=self.bucket, Key=key)["Body"].read()
            except self.client.exceptions.NoSuchKey:
                return None
            except self.client.exceptions.ClientError as e:
                if e.response.get("Error", {}).get("Code") in ("404", "NoSuchKey", "NotFound"):
                    return None
                last_err = e
                time.sleep(min(2 ** attempt, 8))
                continue
            except Exception as e:  # transport blip (timeout, reset, DNS)
                last_err = e
                time.sleep(min(2 ** attempt, 8))
                continue
            return body.decode("utf-8", errors="replace")
        raise last_err  # type: ignore[misc]

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

    def manifest(self) -> dict[str, dict]:
        """slug -> source record from the published manifest. The manifest
        carries EVERY source (disabled included) — absence means deleted."""
        doc = self.get_json(MANIFEST_KEY)
        sources = (doc or {}).get("sources")
        if not isinstance(sources, dict):
            raise SystemExit(
                f"no source manifest at s3://{self.bucket}/{MANIFEST_KEY} — "
                "nothing is production-enabled (factory scripts/publish_sources.py owns it)"
            )
        return {s: r for s, r in sources.items() if isinstance(r, dict)}

    def list_run_ids(self, slug: str) -> list[str]:
        """run_ids under `<slug>/runs/`, newest first. Only ids that parse as
        UTC timestamps count — anything else is skipped with a loud warning
        (see sort_run_ids; issue 092)."""
        prefix = self._slug_key(slug, "runs") + "/"
        ids: list[str] = []
        paginator = self.client.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=self.bucket, Prefix=prefix, Delimiter="/"):
            for cp in page.get("CommonPrefixes", []):
                rid = cp["Prefix"][len(prefix):].strip("/")
                if rid:
                    ids.append(rid)
        return sort_run_ids(ids, slug)

    def chain_json(self, slug: str, run_id: str) -> dict | None:
        """The continuation chain's progress document (`chain.json`) — written
        by the runtime's chain guard alongside run.json: {legs,
        no_progress_streak, unfinished, stopped_reason, ...}. Absent for
        single-leg runs."""
        return self.get_json(self._slug_key(slug, "runs", run_id, "chain.json"))

    def run_json(self, slug: str, run_id: str) -> dict | None:
        return self.get_json(self._slug_key(slug, "runs", run_id, "run.json"))

    def record_json(self, slug: str, run_id: str) -> dict | None:
        """The factory-finalize record for a run — the stronger verdict file
        (evidence fields: ok, conclusion, partial, failed_specs). Absent until
        the factory poller finalizes the run; run.json is the fallback."""
        return self.get_json(self._slug_key(slug, "runs", run_id, "record.json"))

    # -- dispatch provenance markers (bucket-root protocol keys, unprefixed
    #    like STATUS_KEY — R2_PREFIX deliberately does not apply) -----------

    @staticmethod
    def dispatch_marker_key(slug: str, run_id: str) -> str:
        return f"{DISPATCH_MARKER_PREFIX}/{slug}/{run_id}.json"

    def list_dispatch_markers(self, slug: str) -> list[str]:
        """run_ids with a dispatch marker for `slug`, newest first. Empty for
        a healthy connector (markers are deleted once their run leaves a
        record), so the LIST is one cheap request per slug per tick."""
        prefix = f"{DISPATCH_MARKER_PREFIX}/{slug}/"
        ids: list[str] = []
        paginator = self.client.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=self.bucket, Prefix=prefix):
            for obj in page.get("Contents", []):
                name = obj["Key"][len(prefix):]
                if name.endswith(".json"):
                    ids.append(name[: -len(".json")])
        return sorted(ids, reverse=True)

    def put_dispatch_marker(self, slug: str, run_id: str,
                            repo: str | None = None) -> None:
        """Write the immutable per-dispatch marker. Called right after every
        workflow dispatch — the marker IS the provenance, so it must land
        before the tick forgets what it dispatched."""
        self.put_json(self.dispatch_marker_key(slug, run_id), {
            "slug": slug,
            "run_id": run_id,
            "dispatched_at": utcnow().isoformat(),
            "workflow": WORKFLOW_FILE,
            "repo": repo,
        })

    def delete_dispatch_marker(self, slug: str, run_id: str) -> None:
        """Tombstone a resolved marker (its run left a readable record, or a
        newer record superseded it) so the per-slug listing stays bounded."""
        self.client.delete_object(Bucket=self.bucket,
                                  Key=self.dispatch_marker_key(slug, run_id))


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

    def latest_run_for(self, slug: str, run_id: str) -> dict | None:
        """The newest workflow run named exactly `<slug> :: <run_id>`, or None.

        A chain reuses one run name across all its legs, so the first match in
        the newest-first listing is the latest leg. Bounded to runs created on/
        after the day before the run_id's embedded UTC timestamp so the whole
        (narrow) window can be paginated."""
        target = f"{slug}{RUN_NAME_SEP}{run_id}"
        params: dict = {"per_page": 100}
        try:
            t = datetime.strptime(run_id, RUN_ID_FORMAT).replace(tzinfo=timezone.utc)
            params["created"] = f">={(t - timedelta(days=1)).date().isoformat()}"
        except ValueError:
            pass
        for page in range(1, 51):
            runs = self._req(
                "GET", f"/actions/workflows/{WORKFLOW_FILE}/runs",
                params={**params, "page": page},
            ).json().get("workflow_runs", [])
            for run in runs:
                if (run.get("name") or "") == target:
                    return run
            if len(runs) < 100:
                return None
        return None

    def chain_alive(self, slug: str, run_id: str) -> bool:
        """Whether this run chain still has life on GH RIGHT NOW: a leg that is
        queued/in progress, or a just-completed leg whose successor is inside
        the surface grace. The re-check made before a cached judgment (a
        needs_continuation record, a vanished dispatch) is allowed to count
        toward the auto-hold streak — the in-flight listing this corrects has
        missed live legs before (issue 008). Best-effort: an API failure reads
        as not-alive (the caller's evidence stands)."""
        try:
            run = self.latest_run_for(slug, run_id)
        except Exception:  # noqa: BLE001 — a probe failure must not kill the tick
            return False
        if run is None:
            return False
        if run.get("status") != "completed":
            return True
        age = age_days(run.get("updated_at"))
        return age is not None and age * 1440.0 < CONTINUATION_GRACE_MIN


# ---- maintenance contract -----------------------------------------------------


def maintenance_contract(source: dict) -> dict:
    """The operating contract off a manifest record's `maintenance` object.
    Absent or malformed degrades to defaults — a bad record must never stall
    the tick."""
    raw = source.get("maintenance")
    raw = raw if isinstance(raw, dict) else {}
    days = raw.get("cadence_days")
    if isinstance(days, bool) or not isinstance(days, (int, float)) or days <= 0:
        days = DEFAULT_CADENCE_DAYS
    return {
        "cadence_days": int(days),
        "paused": bool(raw.get("paused")),
        "cadence_note": raw.get("cadence_note") if isinstance(raw.get("cadence_note"), str) else None,
    }


# ---- run-outcome vocabulary + the cadence verdict policy ----------------------
#
# MIRROR of factory/hardened/runtime/run_outcome.py — keep in sync (verified
# by issues/invariants/checks/m5_run_status_vocab.py). Operate is vendored
# standalone into the connectors repo (deploy.sh copies only ops/*.py and the
# workflow pip-installs boto3+requests), so it CANNOT import factory code or
# subsets_utils; the vocabulary is mirrored, not imported.

# canonical conclusion -> origin (github conclusion | dag run.json status |
# harness-synthesized substrate-loss verdict).
RUN_OUTCOME_CANONICAL = {
    "success": "github",
    "failure": "github",
    "cancelled": "github",
    "done": "dag",
    "done_with_failures": "dag",
    "failed": "dag",
    "needs_continuation": "dag",
    "lost": "harness",
    "continuation-lost": "harness",
    "wall-timeout": "harness",
    "stalled": "harness",
    "zombie-dispatch-never-launched": "harness",
    "unknown": "unknown",
}
# historical non-canonical spellings -> canonical (read-time translation only).
RUN_OUTCOME_LEGACY = {
    "health_tests_failed": "failed",
}


def normalize_conclusion(raw) -> str:
    """Collapse any observed conclusion string to the canonical vocabulary;
    out-of-vocabulary strings degrade to "unknown" (a tick never crashes on
    vocabulary)."""
    if not isinstance(raw, str) or not raw:
        return "unknown"
    if raw in RUN_OUTCOME_CANONICAL:
        return raw
    return RUN_OUTCOME_LEGACY.get(raw, "unknown")


def cadence_verdict(record: dict | None) -> str:
    """Policy `cadence` — mirror of run_outcome.cadence_verdict (factory).

    A concluded run — clean or partial — satisfies the cadence (so a
    chronically-partial connector is not re-dispatched into a storm), but only
    a CLEAN success anchors `last_ok_at`; a partial run stays visibly partial
    in the status row. Every other terminal conclusion (failed, cancelled,
    lost, wall-timeout, …) counts toward the hard-failure streak that feeds
    auto-hold. Returns concluded_ok | concluded_partial | failed | inflight.
    """
    if not isinstance(record, dict) or not record:
        return "inflight"
    conclusion = normalize_conclusion(record.get("conclusion"))
    if record.get("partial") or conclusion == "done_with_failures":
        return "concluded_partial"
    return "concluded_ok" if record.get("ok") else "failed"


# verdict -> the run.json-status word published in run summaries/status.json,
# so every consumer (classify, ops.py's repair queue, dashboards) keeps one
# vocabulary regardless of which verdict file the evidence came from.
_VERDICT_STATUS = {"concluded_ok": "done",
                   "concluded_partial": "done_with_failures",
                   "failed": "failed"}
# run.json terminal status -> verdict (the fallback path, pre-finalize runs).
_STATUS_VERDICT = {v: k for k, v in _VERDICT_STATUS.items()}


# ---- observation --------------------------------------------------------------


CONCLUDED = ("done", "done_with_failures", "failed")


@dataclass
class Observation:
    slug: str
    runs: list[dict] = field(default_factory=list)  # newest first, scanned window
    last_concluded_at: str | None = None            # concluded_ok | concluded_partial (cadence anchor)
    last_ok_at: str | None = None                   # newest CLEAN success only
    latest: dict | None = None                      # newest scanned run
    consecutive_hard_failures: int = 0
    data_last_changed_at: str | None = None
    never_ran: bool = False
    newest_run_id: str | None = None                # newest run dir on R2, record or not
    newest_run_has_record: bool = False             # that dir had a readable record.json/run.json
    scanned_run_ids: list[str] = field(default_factory=list)  # the dirs the scan window covered
    recorded_run_ids: set[str] = field(default_factory=set)   # scanned dirs with a readable record/run.json
    newest_recorded_run_id: str | None = None       # newest run with READABLE evidence — the
                                                    # dispatch-ledger resolution boundary
    # Continuation-chain progress off the newest evidenced run's chain.json
    # (None when that run is not a chain, or the document is unreadable).
    chain_no_progress_streak: int | None = None     # consecutive legs with zero progress
    chain_legs: int | None = None                   # legs the chain has burned so far


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


def _record_data_changed(record: dict) -> bool:
    """`_data_changed` over a factory record: the per-spec maps carry the same
    orchestrator `outcome` field the run.json nodes do."""
    for per_spec in (record.get("per_spec"), record.get("transform_per_spec")):
        for entry in (per_spec or {}).values():
            if isinstance(entry, dict) and entry.get("outcome") == "ran_changed":
                return True
    return False


def _chain_signal(doc: dict | None) -> bool:
    """Whether a run.json says the run ran as a continuation chain — the cue
    to read its chain.json. Covers every observed spelling: a run.json still
    in `needs_continuation`, a chain-guard-stopped run (`chain_guard` block;
    run.json status flips to failed), and any leg invocation that ended
    `needs_continuation`. Only run.json can rule a chain OUT — the finalize
    record's conclusion can be plain "failure" for a guard-stopped chain, so
    the record path never uses this (it probes chain.json directly).
    """
    if not isinstance(doc, dict):
        return False
    if doc.get("status") == "needs_continuation":
        return True
    if isinstance(doc.get("chain_guard"), dict):
        return True
    return any(isinstance(inv, dict) and inv.get("run_status_after") == "needs_continuation"
               for inv in doc.get("invocations") or [])


def observe(r2: R2, slug: str, in_flight_run_id: str | None,
            chain_alive=None) -> Observation:
    """Read the newest SCAN_RUNS runs for one connector off R2.

    Per run, the factory-finalize `record.json` is the authority when it
    exists (it carries the judged evidence: ok, conclusion, partial,
    failed_specs — the file the factory's own criteria read, so the two sides
    can no longer reach opposite verdicts on the same run, issue 040). Runs
    the factory hasn't finalized yet fall back to the workflow's `run.json`.
    Either way each concluded run gets a `cadence_verdict`: concluded runs —
    clean or partial — anchor `last_concluded_at` (cadence), only clean
    successes anchor `last_ok_at`, and every other terminal outcome advances
    the hard-failure streak.

    On the run.json path, `needs_continuation` with a live GH run is just
    "still going" (skipped via in_flight_run_id); with no live run it's a dead
    self-retrigger chain and counts as a hard failure. A run dir with neither
    file (dispatch that never started, or just-started) is skipped — GH
    in-flight is the authority there.

    `chain_alive` (slug, run_id) -> bool is the re-check before that
    hard-failure judgment sticks: the in-flight listing trails reality (a leg
    can run for hours while the listing misses it), and a chain wrongly read
    as dead feeds the auto-hold streak (issue 008). Only recent records are
    probed (CONTINUATION_PROBE_DAYS); None skips the re-check.
    """
    obs = Observation(slug=slug)
    run_ids = r2.list_run_ids(slug)
    if not run_ids:
        obs.never_ran = True
        return obs
    obs.newest_run_id = run_ids[0]

    obs.scanned_run_ids = run_ids[:SCAN_RUNS]

    streak_open = True
    chain_checked = False
    for rid in obs.scanned_run_ids:
        record = r2.record_json(slug, rid)
        doc = r2.run_json(slug, rid) if record is None else None
        if record is None and doc is None:
            continue
        obs.recorded_run_ids.add(rid)
        if obs.newest_recorded_run_id is None:
            obs.newest_recorded_run_id = rid  # ids scan newest-first
        if rid == obs.newest_run_id:
            obs.newest_run_has_record = True
        if rid == in_flight_run_id:
            continue  # live run: not evidence of anything yet

        # Continuation-chain progress (issue 089): when the newest evidenced
        # run is a chain, its chain.json carries the progress the run-level
        # verdict hides — legs burned and the no-progress streak. Surfaced on
        # the status row; wedged (>= WEDGED_CHAIN_AFTER) becomes attention in
        # classify(). Report-only: nothing here touches cadence or streaks.
        if not chain_checked:
            chain_checked = True
            # A run.json without chain markers rules the probe out; a
            # finalize record cannot (a guard-stopped chain finalizes as a
            # plain "failure"), so the record path always probes — chain.json
            # is simply absent for single-leg runs (one cheap 404).
            if doc is None or _chain_signal(doc):
                chain = r2.chain_json(slug, rid)
                if isinstance(chain, dict):
                    streak_v, legs_v = chain.get("no_progress_streak"), chain.get("legs")
                    if isinstance(streak_v, int) and not isinstance(streak_v, bool):
                        obs.chain_no_progress_streak = streak_v
                    if isinstance(legs_v, int) and not isinstance(legs_v, bool):
                        obs.chain_legs = legs_v

        if record is not None:
            verdict = cadence_verdict(record)
            if verdict == "inflight":
                continue
            changed = _record_data_changed(record)
            duration_s = record.get("duration_s")
            minutes = (duration_s / 60.0
                       if isinstance(duration_s, (int, float))
                       and not isinstance(duration_s, bool) else None)
            summary = {
                "run_id": rid,
                "status": _VERDICT_STATUS[verdict],
                "verdict": verdict,
                "partial": verdict == "concluded_partial",
                "conclusion": normalize_conclusion(record.get("conclusion")),
                "finished_at": record.get("finished_at"),
                "url": record.get("run_url"),
                "data_changed": changed,
                "minutes": round(minutes, 1) if minutes is not None else None,
            }
        else:
            status = doc.get("status")
            if status == "needs_continuation":
                age = age_days(doc.get("finished_at"))
                if (chain_alive is not None and age is not None
                        and age <= CONTINUATION_PROBE_DAYS
                        and chain_alive(slug, rid)):
                    continue  # live chain the in-flight listing missed: not evidence
                status = "failed"  # not live on GH: a dead self-retrigger chain
            if status not in CONCLUDED:
                continue
            verdict = _STATUS_VERDICT[status]
            changed = _data_changed(doc)
            started, finished = parse_iso(doc.get("started_at")), parse_iso(doc.get("finished_at"))
            minutes = ((finished - started).total_seconds() / 60.0
                       if started and finished and finished >= started else None)
            summary = {
                "run_id": rid,
                "status": status,
                "verdict": verdict,
                "partial": status == "done_with_failures",
                "conclusion": normalize_conclusion(status),
                "finished_at": doc.get("finished_at"),
                "url": doc.get("github_run_url"),
                "data_changed": changed,
                "minutes": round(minutes, 1) if minutes is not None else None,
            }

        obs.runs.append(summary)
        if obs.latest is None:
            obs.latest = summary
        if verdict in ("concluded_ok", "concluded_partial") and obs.last_concluded_at is None:
            obs.last_concluded_at = summary["finished_at"]
        if verdict == "concluded_ok" and obs.last_ok_at is None:
            obs.last_ok_at = summary["finished_at"]
        if changed and obs.data_last_changed_at is None:
            obs.data_last_changed_at = summary["finished_at"]
        if streak_open:
            if verdict == "failed":
                obs.consecutive_hard_failures += 1
            else:
                streak_open = False

    if not obs.runs:
        obs.never_ran = in_flight_run_id is None
    return obs


# ---- policy --------------------------------------------------------------------


def _run_id_age_min(run_id: str) -> float | None:
    """Minutes since the UTC timestamp embedded in a run_id (== dispatch
    time; gh.dispatch mints the id from utcnow). None when unparseable."""
    try:
        t = datetime.strptime(run_id, RUN_ID_FORMAT).replace(tzinfo=timezone.utc)
    except (TypeError, ValueError):
        return None
    return (utcnow() - t).total_seconds() / 60.0


def dispatch_ledger(r2: R2, obs: Observation, in_flight_run_id: str | None = None,
                    chain_alive=None, pending_run_ids=()) -> dict:
    """Lost-dispatch evidence DERIVED from the immutable dispatch markers
    (S32 rule 4 / problem 039), never carried from the previous status row.

    Each dispatch leaves a marker at `_operate/dispatched/<slug>/<run_id>.json`
    that only a readable run record can resolve. Per marker, newest first:

      * run_id <= the newest run with READABLE evidence on R2
        (`obs.newest_recorded_run_id`) — resolved/superseded: evidence flows
        through run records again, so the marker is returned for deletion and
        everything older stops counting.
      * the run left readable evidence itself (record.json or run.json,
        fetched directly for markers outside the scan window) — resolved.
      * younger than CONTINUATION_GRACE_MIN, currently in flight on GH, or
        `chain_alive` — pending: no verdict yet, marker stays.
      * otherwise — LOST: dispatched, nothing landed, nothing live. The
        marker stays on R2, so the loss remains evidenced no matter how many
        ticks pass or what happens to status.json.

    `streak` = the lost markers newer than the last real run record — the
    number that feeds auto-hold. A recordless run dir resolves nothing
    (absence of evidence must not erase loss evidence, S34), and a pending
    marker between lost ones does not break the count (a record does).

    `pending_run_ids` are dispatches known from the previous status document
    that may predate the ledger (the migration shim); they are folded in as
    virtual markers and reported in `unmarked` so the tick can materialize
    them. Read-only: deletion of `resolved` markers is the CALLER's move —
    status.py --live must stay a pure read.

    Returns {"streak", "lost", "pending", "resolved", "unmarked"}.
    """
    marker_ids = r2.list_dispatch_markers(obs.slug)
    virtual = [rid for rid in pending_run_ids if rid and rid not in marker_ids]
    merged = sorted(set(marker_ids) | set(virtual), reverse=True)
    boundary = obs.newest_recorded_run_id
    lost: list[str] = []
    pending: list[str] = []
    resolved: list[str] = []
    record_seen = False  # a real record at/newer than the remaining markers
    for rid in merged:  # newest first; run_ids are UTC timestamps
        if record_seen:
            resolved.append(rid)   # superseded by a newer real record
            continue
        if (boundary is not None and rid <= boundary) or rid in obs.recorded_run_ids:
            resolved.append(rid)   # the dispatch (or a newer one) left a record
            record_seen = True
            continue
        if rid not in obs.scanned_run_ids and obs.newest_run_id is not None \
                and rid <= obs.newest_run_id:
            # A dir exists but the scan window never read it: fetch the
            # verdict files directly rather than guessing (rare — markers
            # are deleted once resolved, so few ever outlive the window).
            if r2.record_json(obs.slug, rid) is not None \
                    or r2.run_json(obs.slug, rid) is not None:
                resolved.append(rid)
                record_seen = True
                continue
        if rid == in_flight_run_id:
            pending.append(rid)    # visibly queued/running right now
            continue
        age_min = _run_id_age_min(rid)
        if age_min is None or age_min < CONTINUATION_GRACE_MIN:
            pending.append(rid)    # inside the surfacing grace — no verdict
            continue
        # Probe GH only inside the continuation window (same bound as the
        # needs_continuation re-check): legs cap at 6h, so a marker silent
        # for CONTINUATION_PROBE_DAYS is dead by construction — an auto-held
        # slug's old markers must not cost probes every tick forever.
        if chain_alive is not None and age_min <= CONTINUATION_PROBE_DAYS * 1440.0 \
                and chain_alive(obs.slug, rid):
            pending.append(rid)    # live on GH — the in-flight listing missed it
            continue
        lost.append(rid)
    return {"streak": len(lost), "lost": lost, "pending": pending,
            "resolved": resolved, "unmarked": virtual}


def classify(contract: dict, obs: Observation, in_flight: dict | None,
             lost_streak: int = 0) -> dict:
    """One connector's verdict: attention word + whether to dispatch now.

    Attention: paused | in-flight | auto-held | dispatch-lost | wedged-chain |
    failing | degraded | never-ran | due | ok. Exactly one per connector;
    needs_attention marks the ones a human (or a factory repair session)
    should look at. Lost dispatches (see dispatch_ledger) count toward
    the auto-hold threshold exactly like hard failures — a connector whose
    runs die before writing run.json must not be re-dispatched forever.

    `wedged-chain` (issue 089): the newest run's continuation chain completed
    >= WEDGED_CHAIN_AFTER consecutive legs with zero progress — legs run,
    budgets burn, nothing lands. REPORT-ONLY today: it renames the attention
    word and joins needs_attention, but the dispatch decision and the cadence
    clock are exactly what they would be without it (flipping the cadence
    semantics — a no-progress leg must not advance last_concluded_at — is
    S41's sequencing step 3, deliberately not this change).
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

    # `auto-held` is renamed too: a connector whose failure streak is nothing
    # but guard-stopped chains is held BECAUSE it is wedged, and the wedge is
    # the actionable diagnosis. The hold itself survives — `dispatch` was
    # already computed False above. paused/in-flight stay: a live leg or an
    # explicit pause is the more current fact.
    if (obs.chain_no_progress_streak is not None
            and obs.chain_no_progress_streak >= WEDGED_CHAIN_AFTER
            and attention in ("auto-held", "failing", "degraded", "due", "ok")):
        attention = "wedged-chain"  # report-only: `dispatch` stays as computed

    needs_attention = attention in ("auto-held", "dispatch-lost", "wedged-chain",
                                    "failing", "degraded", "never-ran") or stale
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

    The lost-dispatch streak is DERIVED from the dispatch-provenance markers
    on R2 every tick (see dispatch_ledger) — never carried from the previous
    status row, so it survives filtered ticks, hand-run ticks, and a lost
    status.json. `prev_status` is only the migration shim: a `dispatched`
    entry that predates the ledger is folded in as a virtual marker (and
    reported per row as `unmarked_dispatch` for the tick to materialize).

    Read-only over R2: rows carry `resolved_markers` (markers a real run
    record has superseded) for the TICK to delete — a live status render
    must never mutate the ledger.
    """
    manifest = r2.manifest()
    gate = sorted(s for s, rec in manifest.items() if rec.get("enabled") is True)
    inflight = gh.in_flight()
    prev_dispatched: dict[str, str] = {}
    if prev_status:
        prev_dispatched = {d["slug"]: d["run_id"] for d in prev_status.get("dispatched") or []
                           if isinstance(d, dict) and d.get("slug") and d.get("run_id")}
    rows: list[dict] = []
    for slug in gate:
        contract = maintenance_contract(manifest[slug])
        chain_alive = getattr(gh, "chain_alive", None)
        in_flight_run_id = (inflight.get(slug) or {}).get("run_id")
        obs = observe(r2, slug, in_flight_run_id, chain_alive=chain_alive)
        prev_rid = prev_dispatched.get(slug)
        ledger = dispatch_ledger(r2, obs, in_flight_run_id,
                                 chain_alive=chain_alive,
                                 pending_run_ids=(prev_rid,) if prev_rid else ())
        lost = ledger["streak"]
        verdict = classify(contract, obs, inflight.get(slug), lost)
        scanned_minutes = sum(r["minutes"] for r in obs.runs if r["minutes"] is not None)
        rows.append({
            "slug": slug,
            **contract,
            # Only a CLEAN success is "last ok" (S35); the cadence clock —
            # due-ness, age_days — runs on last_concluded_at, so a partial run
            # still satisfies the cadence without reading as healthy.
            "last_ok_at": obs.last_ok_at,
            "last_concluded_at": obs.last_concluded_at,
            "partial": bool(obs.latest and obs.latest.get("partial")),
            "latest": obs.latest,
            "consecutive_failures": obs.consecutive_hard_failures,
            "dispatch_lost_streak": lost,
            # The ledger's full verdict: lost markers (still-evidenced vanished
            # dispatches), pending markers (no verdict yet), plus two keys for
            # the tick's write phase — resolved_markers to delete and
            # unmarked_dispatch to materialize (pre-ledger migration).
            "lost_dispatches": ledger["lost"],
            "pending_dispatches": ledger["pending"],
            "resolved_markers": ledger["resolved"],
            "unmarked_dispatch": (ledger["unmarked"][0] if ledger["unmarked"] else None),
            "newest_run_id": obs.newest_run_id,
            # Continuation-chain progress (issue 089), off the newest
            # evidenced run's chain.json; null when that run is not a chain.
            "chain_no_progress_streak": obs.chain_no_progress_streak,
            "chain_legs": obs.chain_legs,
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


# ---- gate drift ------------------------------------------------------------------


def gate_drift(report: dict | None, gate: set[str]) -> dict:
    """The promotion predicate vs the gate as served — the `gate` section of
    status.json. REPORT-ONLY: the tick never enables, disables, or demotes
    anything off this; it publishes the drift so a person (or a later policy)
    can act on it.

    The predicate itself runs factory-side (it needs harness state operate
    must never read); factory publishes the verdicts as
    `_harness/gate_report.json` (scripts/publish_sources.py `gate-report`,
    refreshed by `sync-evaluated`), and this folds them against the enabled
    set. An absent or malformed report degrades to a section that says so —
    and reads as stale, so a stopped evaluation is itself visible.
    """
    section: dict = {"report_key": GATE_REPORT_KEY}
    results = (report or {}).get("results")
    if not isinstance(results, dict):
        section.update({
            "report_generated_at": None,
            "stale": True,
            "note": "no gate report on R2 — factory scripts/publish_sources.py "
                    "gate-report publishes it",
        })
        return section
    rows = {s: r for s, r in results.items() if isinstance(r, dict)}
    age = age_days(report.get("generated_at"))
    failing = {s: [str(x) for x in (r.get("reasons") or [])]
               for s, r in rows.items() if s in gate and r.get("pass") is not True}
    section.update({
        "report_generated_at": report.get("generated_at"),
        "report_age_days": round(age, 2) if age is not None else None,
        "stale": age is None or age >= GATE_REPORT_STALE_DAYS,
        "evaluated": len(rows),
        "passing": sum(1 for r in rows.values() if r.get("pass") is True),
        # Drift, both directions: on the gate but failing the predicate (with
        # the reasons, verbatim), and production-ready but not on the gate.
        "enabled_failing": {s: failing[s] for s in sorted(failing)},
        "disabled_passing": sorted(s for s, r in rows.items()
                                   if s not in gate and r.get("pass") is True),
        # On the gate but absent from the report — the evaluation never saw it.
        "enabled_unevaluated": sorted(gate - set(rows)),
    })
    return section


def render_gate(section: dict | None) -> str:
    """The gate section as console lines; the full reasons live in status.json."""
    if not isinstance(section, dict) or not section:
        return "gate: not evaluated"
    if section.get("note"):
        return f"gate: {section['note']}"
    failing = section.get("enabled_failing") or {}
    age = section.get("report_age_days")
    line = (f"gate: {section.get('passing')}/{section.get('evaluated')} evaluate-green · "
            f"{len(failing)} enabled-but-failing · "
            f"{len(section.get('disabled_passing') or [])} disabled-but-passing")
    if isinstance(age, (int, float)):
        line += f" · report {age:.1f}d old"
    if section.get("stale"):
        line += " · STALE"
    lines = [line]
    if failing:
        lines.append("  enabled but failing the predicate: " + ", ".join(sorted(failing)))
    if section.get("enabled_unevaluated"):
        lines.append("  enabled but never evaluated: "
                     + ", ".join(section["enabled_unevaluated"]))
    return "\n".join(lines)


# ---- rendering -------------------------------------------------------------------


_ATTENTION_ORDER = ("auto-held", "dispatch-lost", "wedged-chain", "failing", "degraded",
                    "never-ran", "due", "in-flight", "paused", "ok")


def sort_rows(rows: list[dict]) -> list[dict]:
    rank = {a: i for i, a in enumerate(_ATTENTION_ORDER)}
    return sorted(rows, key=lambda r: (rank.get(r["attention"], 99), r["slug"]))


def render(rows: list[dict]) -> str:
    header = (f"{'connector':34} {'concl':>8} {'cad':>5} {'chg':>8} {'min':>7} "
              f"{'fails':>5} {'attention':10}  note")
    lines = [header, "-" * len(header)]
    for r in sort_rows(rows):
        last = f"{r['age_days']:.1f}d" if r["age_days"] is not None else "never"
        chg_age = age_days(r["data_last_changed_at"])
        chg = f"{chg_age:.1f}d" if chg_age is not None else "-"
        latest_min = (r.get("latest") or {}).get("minutes")
        mins = f"{latest_min:.0f}m" if latest_min is not None else "-"
        note = r.get("cadence_note") or ""
        if r.get("chain_no_progress_streak") is not None:
            chain_bit = (f"chain: {r.get('chain_legs')} legs / "
                         f"{r['chain_no_progress_streak']} no-progress")
            note = f"{chain_bit}; {note}" if note else chain_bit
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
