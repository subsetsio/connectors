"""Per-connector RAW MANIFEST — a commit-log resolution layer over raw outputs.

Raw objects are run-scoped in cloud (`<connector>/runs/<run_id>/raw/...`), so
a path alone cannot answer "what is the current raw for asset X?" across runs:
a fresh run's raw dir starts empty, a maintain-skipped fetch leaves nothing in
it, and partial runs never compose. The manifest is the connector-level answer:
one JSON document at the connector root mapping each logical asset to the
fragment objects that currently constitute it, wherever (whichever run dir)
they live.

    {
      "version": 1,
      "assets": {
        "<asset_key>": {                  # entity-prefixed like the path layout
          "ext": "parquet",
          "fragments": {
            "<fragment_key>": {           # "full" unless a named fragment
              "path": "<object key (cloud) or data-dir relpath (dev)>",
              "hash": "<sha256 of written bytes, or null for streamed writes>",
              "size": 123,
              "run_id": "20260701-010203",
              "fetched_at": "2026-07-01T01:02:03+00:00"
            }
          }
        }
      }
    }

Commit-log discipline
---------------------
Raw OBJECT writes happen first (unchanged: run-scoped, immutable). The manifest
entry is committed strictly AFTER the object exists. Readers trust ONLY the
manifest: an object not referenced by it does not exist. A `"full"`-fragment
write replaces the asset's entire fragments map; a named-fragment write
replaces just that key (siblings stand).

Concurrency
-----------
DAG nodes run as separate (possibly parallel) subprocesses. Children never
write the shared manifest — they would lose each other's updates. Instead each
child STAGES its pending entries to a per-node file under the run dir
(`runs/<run_id>/raw/.manifest/<node_id>.json` in cloud, the analogous path
under the local raw dir in dev), and the single-threaded PARENT orchestrator
merges a node's staged entries into the connector manifest when it observes
that node complete successfully (`orchestrator._apply_result`), committing
with one PUT (cloud) / atomic rename (dev). A failed node's staged entries are
discarded. Within one node process the staged entries also live in an
in-memory pending overlay so read-after-write inside the same node resolves to
the fresh object, not a prior run's committed entry.

Back-compat
-----------
When the manifest has no entry for an asset, every reader falls back to
today's behavior (run-scoped path / glob). A connector's first full run under
this code fully populates its manifest — no backfill migration. The harness's
`reconcile-raw <connector>` command can rebuild a manifest from run records.
"""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from .config import (
    get_bucket_name,
    get_data_dir,
    get_r2_prefix,
    get_connector_name,
    get_r2_run_base,
    is_cloud,
)
from .storage import backend
from . import tracking

FULL = "full"

# In-process pending overlay: entries staged by THIS process, not yet committed
# by the parent. Each entry carries "_node" (the staging node id) so a process
# that simulates several nodes (tests) stages each node's file separately.
_pending: list[dict] = []

# Committed-manifest cache, keyed by manifest URI (so a DATA_DIR change — e.g.
# per-test tempdirs — naturally misses). Children are spawn-fresh per node, so
# one read per node process; the parent invalidates on every commit.
_cache: dict = {"uri": None, "doc": None}


# =============================================================================
# Locations
# =============================================================================

def manifest_uri() -> str:
    """The connector's manifest: `s3://<bucket>/[<prefix>/]<connector>/raw_manifest.json`
    in cloud; `<data_dir>/raw_manifest.json` (sibling of the raw dir) in dev."""
    if is_cloud():
        prefix = get_r2_prefix()
        base = f"{prefix}/{get_connector_name()}" if prefix else get_connector_name()
        return f"s3://{get_bucket_name()}/{base}/raw_manifest.json"
    return str(Path(get_data_dir()) / "raw_manifest.json")


def staging_uri(node_id: str) -> str:
    """Per-node staging file, under the run's raw dir so it is run-scoped like
    the objects it describes (cloud) / under the local raw dir (dev). The
    dot-directory keeps it out of every `<dep>.*` / `<dep>-*` glob."""
    safe = node_id.replace("/", "_")
    if is_cloud():
        return f"s3://{get_bucket_name()}/{get_r2_run_base()}/raw/.manifest/{safe}.json"
    return str(Path(get_data_dir()) / "raw" / ".manifest" / f"{safe}.json")


# =============================================================================
# Keys / refs
# =============================================================================

def asset_key(asset_id: str, entity_id: str | None = None) -> str:
    """Manifest key for an asset — entity-prefixed exactly like the path layout."""
    return f"{entity_id}/{asset_id}" if entity_id is not None else asset_id


def object_id(asset_id: str, fragment: str | None) -> str:
    """The on-disk asset name for a write: `<asset>` for the full asset,
    `<asset>-<fragment>` for a named fragment (matching the existing batch
    layout `<asset>-*`, which the glob fallback already understands)."""
    if fragment is None:
        return asset_id
    if not isinstance(fragment, str) or not fragment.strip() or "/" in fragment:
        raise ValueError(f"fragment must be a non-empty string without '/': {fragment!r}")
    return f"{asset_id}-{fragment}"


def content_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _ref_from_uri(uri: str) -> str:
    """Manifest path form: full object key (cloud) / data-dir relpath (dev)."""
    if uri.startswith("s3://"):
        return uri.split("/", 3)[3]
    try:
        return str(Path(uri).resolve().relative_to(Path(get_data_dir()).resolve()))
    except ValueError:
        return str(uri)


def _uri_from_ref(ref: str) -> str:
    if is_cloud():
        return f"s3://{get_bucket_name()}/{ref}"
    p = Path(ref)
    return str(p) if p.is_absolute() else str(Path(get_data_dir()).resolve() / ref)


# =============================================================================
# Committed manifest — load / commit (commit is PARENT-only)
# =============================================================================

def load(force: bool = False) -> dict:
    """The committed manifest (cached per URI). A missing or corrupt manifest
    reads as empty — readers then fall back to path resolution; never crash a
    run over the resolution layer."""
    uri = manifest_uri()
    if not force and _cache["uri"] == uri and _cache["doc"] is not None:
        return _cache["doc"]
    doc = {"version": 1, "assets": {}}
    data = backend.read_bytes(uri)
    if data:
        try:
            parsed = json.loads(data)
            if isinstance(parsed, dict) and isinstance(parsed.get("assets"), dict):
                doc = parsed
            else:
                print(f"[raw-manifest] WARN: malformed manifest at {uri} — treating as empty")
        except json.JSONDecodeError:
            print(f"[raw-manifest] WARN: unparseable manifest at {uri} — treating as empty")
    _cache["uri"], _cache["doc"] = uri, doc
    return doc


def invalidate_cache() -> None:
    _cache["uri"], _cache["doc"] = None, None


def _write_manifest(doc: dict) -> None:
    """Commit the manifest: single PUT in cloud, atomic tmp+rename locally."""
    uri = manifest_uri()
    payload = json.dumps(doc, indent=2, sort_keys=True).encode("utf-8")
    if uri.startswith("s3://"):
        backend.write_bytes(uri, payload)
    else:
        path = Path(uri)
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
        try:
            with os.fdopen(fd, "wb") as f:
                f.write(payload)
            os.replace(tmp, path)
        except Exception:
            try:
                os.unlink(tmp)
            except OSError:
                pass
            raise
    invalidate_cache()


def merge_entries(assets: dict, entries: list[dict]) -> None:
    """Apply staged entries to an assets map, in order.

    A "full" write replaces the asset's whole fragments map; a named-fragment
    write replaces only its key. An ext change replaces the whole asset (one
    format per asset — sql_transform enforces the same). A delete op removes
    the asset entirely."""
    for e in entries:
        key = e.get("asset")
        if not isinstance(key, str):
            continue
        if e.get("op") == "delete":
            assets.pop(key, None)
            continue
        frag = e.get("fragment") or FULL
        frag_entry = {
            "path": e.get("path"),
            "hash": e.get("hash"),
            "size": e.get("size"),
            "run_id": e.get("run_id"),
            "fetched_at": e.get("fetched_at"),
        }
        ext = e.get("ext")
        asset = assets.get(key)
        if frag == FULL or not isinstance(asset, dict) or asset.get("ext") != ext:
            assets[key] = {"ext": ext, "fragments": {frag: frag_entry}}
        else:
            fragments = asset.setdefault("fragments", {})
            fragments[frag] = frag_entry


def commit_node(node_id: str) -> bool:
    """PARENT-only: merge a completed node's staged entries into the connector
    manifest and commit. Returns True when anything was merged. Deletes the
    staging file afterwards (a re-run of the node re-stages from scratch)."""
    uri = staging_uri(node_id)
    data = backend.read_bytes(uri)
    if data is None:
        return False  # node staged nothing (e.g. wrote no raw)
    try:
        entries = json.loads(data).get("entries") or []
    except (json.JSONDecodeError, AttributeError):
        entries = []
    if entries:
        manifest = load(force=True)  # fresh read: prior commits this run must be kept
        assets = manifest.setdefault("assets", {})
        merge_entries(assets, entries)
        _write_manifest(manifest)
    backend.delete(uri)
    return bool(entries)


def classify_staged_change(node_id: str) -> str | None:
    """PARENT-only: classify a node's STAGED raw writes against the manifest's
    PREVIOUS committed entries — the "did this download actually change?" signal.

    Call BEFORE commit_node (which consumes the staging and overwrites the
    previous entries). Compares each staged fragment's content hash against the
    committed entry that stands right now:

        "ran_unchanged" — every staged fragment matched a previous fragment of
                          the same asset with an identical, present hash (and no
                          fragment was added).
        "ran_changed"   — some staged fragment differs from, or is new relative
                          to, the previous entry (hashes present on both sides).
        "ran"           — the change is unknowable: a streamed write staged
                          hash=None, or there is no previous entry / fragment to
                          compare against.
        None            — the node staged no raw writes (not a download node).

    Removed-fragment detection is limited to the full-replace case (a "full"
    write replaces the whole fragments map); a named-fragment write only touches
    its own key, so its siblings standing is not a change.
    """
    data = backend.read_bytes(staging_uri(node_id))
    if data is None:
        return None
    try:
        entries = json.loads(data).get("entries") or []
    except (json.JSONDecodeError, AttributeError):
        entries = []
    puts = [e for e in entries if e.get("op") != "delete"]
    if not puts:
        return None

    committed = load().get("assets") or {}

    # Group staged fragments per asset so a "full" write can be compared against
    # the whole previous fragments map (full replaces it).
    staged_by_asset: dict[str, dict[str, str | None]] = {}
    for e in puts:
        key = e.get("asset")
        if not isinstance(key, str):
            continue
        staged_by_asset.setdefault(key, {})[e.get("fragment") or FULL] = e.get("hash")

    all_unchanged = True
    for key, staged_frags in staged_by_asset.items():
        if any(h is None for h in staged_frags.values()):
            return "ran"  # streamed write — no content hash to compare
        prev = committed.get(key)
        if not isinstance(prev, dict):
            return "ran"  # no previous entry for this asset
        prev_frags = prev.get("fragments") or {}
        if FULL in staged_frags:
            # A full write replaces the entire fragments map — the asset is
            # unchanged only if the prior map was exactly {full: same-hash}.
            prev_full = prev_frags.get(FULL)
            if set(prev_frags) != {FULL} or not isinstance(prev_full, dict):
                all_unchanged = False
                continue
            if prev_full.get("hash") is None:
                return "ran"
            if prev_full.get("hash") != staged_frags[FULL]:
                all_unchanged = False
            continue
        for frag, h in staged_frags.items():
            prev_frag = prev_frags.get(frag)
            if prev_frag is None:
                all_unchanged = False  # new fragment relative to previous
                continue
            if not isinstance(prev_frag, dict) or prev_frag.get("hash") is None:
                return "ran"  # previous hash unavailable
            if prev_frag.get("hash") != h:
                all_unchanged = False
    return "ran_unchanged" if all_unchanged else "ran_changed"


def discard_node(node_id: str) -> None:
    """PARENT-only: drop a failed node's staged entries (best-effort)."""
    try:
        backend.delete(staging_uri(node_id))
    except Exception:
        pass


# =============================================================================
# Staging — called by io.py on every raw write (child side)
# =============================================================================

def _stage(entry: dict) -> None:
    """Record a pending entry: in-memory overlay always; per-node staging file
    when running under a DAG node (the parent commits it on node success).
    Outside a node (ad-hoc scripts) the overlay alone keeps read-after-write
    consistent and the manifest is simply never updated."""
    node = tracking.current_task()
    entry["_node"] = node
    _pending.append(entry)
    if node is None:
        return
    doc = {
        "version": 1,
        "node": node,
        "entries": [
            {k: v for k, v in e.items() if k != "_node"}
            for e in _pending
            if e.get("_node") == node
        ],
    }
    backend.write_bytes(staging_uri(node), json.dumps(doc, indent=2).encode("utf-8"))


def stage_write(asset_id: str, ext: str, uri: str, *, size: int | None,
                hash: str | None, entity_id: str | None = None,
                fragment: str | None = None) -> None:
    """Stage a manifest entry for a raw object that was just written at `uri`.

    Also records the write into run-record lineage (run.json `raw_writes`) —
    staging is the single bookkeeping point for raw writes; io's save fns make
    one call, not two parallel ones."""
    tracking.record_write("raw/" + uri.split("/raw/", 1)[-1])
    _stage({
        "op": "put",
        "asset": asset_key(asset_id, entity_id),
        "ext": ext,
        "fragment": fragment or FULL,
        "path": _ref_from_uri(uri),
        "hash": hash,
        "size": size,
        "run_id": os.environ.get("RUN_ID", "unknown"),
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    })


def stage_delete(asset_id: str, ext: str, *, entity_id: str | None = None) -> None:
    """Stage removal of an asset's manifest entry (mirrors delete_raw_file)."""
    _stage({"op": "delete", "asset": asset_key(asset_id, entity_id), "ext": ext})


def reset_pending() -> None:
    """Clear the in-memory overlay (child entry / tests). Staging files are
    not touched — the parent owns their lifecycle."""
    _pending.clear()


# =============================================================================
# Resolution — the read side
# =============================================================================

def _effective_asset(key: str) -> dict | None:
    """The asset entry as this process sees it: committed manifest with this
    process's own pending entries overlaid (read-after-write inside a node)."""
    committed = (load().get("assets") or {}).get(key)
    relevant = [e for e in _pending if e.get("asset") == key]
    if not relevant:
        return committed if isinstance(committed, dict) else None
    assets: dict = {}
    if isinstance(committed, dict):
        assets[key] = {
            "ext": committed.get("ext"),
            "fragments": dict(committed.get("fragments") or {}),
        }
    merge_entries(assets, relevant)
    return assets.get(key)


def asset_entry(asset_id: str, ext: str, *, entity_id: str | None = None) -> dict | None:
    """The manifest entry for (asset, ext), pending overlay included, or None.
    An entry recorded under a different ext is treated as absent — readers
    address by (id, ext), matching the path layout."""
    a = _effective_asset(asset_key(asset_id, entity_id))
    if not a or a.get("ext") != ext or not a.get("fragments"):
        return None
    return a


def resolve_read_uri(asset_id: str, ext: str, *, entity_id: str | None = None) -> str | None:
    """URI of the asset's "full" fragment, or None (no entry / only named
    fragments → caller falls back to the legacy run-scoped path)."""
    a = asset_entry(asset_id, ext, entity_id=entity_id)
    if not a:
        return None
    frag = (a.get("fragments") or {}).get(FULL)
    if not isinstance(frag, dict) or not frag.get("path"):
        return None
    return _uri_from_ref(frag["path"])


def newest_fetched_at(entry: dict) -> datetime | None:
    """Latest fragment `fetched_at` of an asset entry — 'when was this asset
    last (partially) refetched'. None when no fragment carries a timestamp."""
    newest = None
    for frag in (entry.get("fragments") or {}).values():
        ts = (frag or {}).get("fetched_at")
        if not ts:
            continue
        try:
            dt = datetime.fromisoformat(ts)
        except (TypeError, ValueError):
            continue
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        if newest is None or dt > newest:
            newest = dt
    return newest


def fetched_this_run(node_id: str) -> bool:
    """True iff the COMMITTED manifest already holds this node's raw, fetched
    under the CURRENT run id — i.e. an earlier continuation leg of this very
    run landed it. Same asset resolution as dep_fragments (exact key, else
    the flat `<node_id>-*` batch layout). Every fragment must carry the
    current run_id: mixed or older run ids mean the asset's raw was not
    (fully) produced by this run, so the node must execute.

    This is the durable-evidence half of the leg-skip: the orchestrator pairs
    it with the prior leg's explicit per-node completion record, so neither a
    stale manifest nor a stale run.json can cause a skip on its own."""
    run_id = os.environ.get("RUN_ID")
    if not run_id:
        return False
    assets = load().get("assets") or {}
    hit = assets.get(node_id)
    matches = {node_id: hit} if isinstance(hit, dict) else {
        k: v for k, v in assets.items()
        if isinstance(v, dict) and "/" not in k and k.startswith(f"{node_id}-")
    }
    frags = [f for m in matches.values()
             for f in (m.get("fragments") or {}).values() if isinstance(f, dict)]
    if not frags:
        return False
    return all(f.get("run_id") == run_id for f in frags)


def dep_fragments(dep_id: str) -> list[tuple[str, str]] | None:
    """Resolve a SqlNodeSpec dep's raw file set from the COMMITTED manifest.

    Exact asset-key match wins; otherwise flat assets named `<dep>-*` are
    unioned (the batch layout — also what `reconcile-raw` reconstructs named
    fragments as). Returns [(ref, uri), ...] sorted for a deterministic
    FROM-clause, or None when the manifest knows nothing about the dep (the
    caller then falls back to the legacy run-scoped glob)."""
    assets = load().get("assets") or {}
    hit = assets.get(dep_id)
    matches = {dep_id: hit} if isinstance(hit, dict) else {
        k: v for k, v in assets.items()
        if isinstance(v, dict) and "/" not in k and k.startswith(f"{dep_id}-")
    }
    out: list[tuple[str, str]] = []
    for k in sorted(matches):
        fragments = matches[k].get("fragments") or {}
        for fk in sorted(fragments):
            ref = (fragments[fk] or {}).get("path")
            if ref:
                out.append((ref, _uri_from_ref(ref)))
    return out or None
