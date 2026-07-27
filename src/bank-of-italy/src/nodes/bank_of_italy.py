"""Banca d'Italia — Base Dati Statistica (BDS), via the InfoStat inquiry app.

One download node per BDS table (a leaf-bearing CUBESET such as `AGGM0100`),
each grouping 1..1316 member time series (leaf CUBEs).

Mechanism — research's `inquiry_rest`, with the data fetch resolved here. Every
service is a form-urlencoded POST to `home?calltype=asin&service=<S>` returning
JSON (mislabelled `text/html`, sometimes BOM-prefixed):

  1. `GET home` + `GET home?service=HOMEPAGE` seed the JSESSIONID the data
     services require. Without it they answer 500 with the "Risorsa Protetta"
     error page — which is what made research read them as broken.
  2. `GETNODESBYCUBEIDS {CUBEID: <localId>}` resolves a table id to its node.
     `CUBEID` takes **localIds** (`AGGM0100`), not the fully-qualified
     `BANKITALIA:DIFF:CUBE:AGGM0100`: the latter silently returns `[]`, and
     feeding those ids to PROSPETTODATI is the other half of the 500.
  3. `SUBTREENODES` on that node in **survey-tree** mode (`surveytree=true`,
     `nodePath` from `parentAbsPath`) lists the table's member CUBEs. The
     taxonomy tree is unusable here: collect's `abs_path` is a phantom chain for
     ~30 tables (TDB10224, TRI30021, TFR*) that resolves to no node, whereas the
     survey tree resolves every table from its id alone. Enumerating members
     live also means a series added upstream is picked up on the next run rather
     than frozen into a baked-in id list.
  4. `PROSPETTODATI {CUBEIDS: <;-joined localIds>, VIEW_MODE: table}` returns,
     under `GRAPHDATA.observations`, the complete history of every requested
     series as flat records. The `table` pivot in the same payload is
     server-paginated; the observations are not. `DOMAINELEMENTS` carries the
     id -> label map per dimension, denormalized onto the rows as `<DIM>_label`.
  5. The observations are only *fully keyed* when every dimension sits on the
     pivot's row or column axis. 128 of the 453 tables are multidimensional
     cubes (`cubeStatType: UP_TSCUBE`) whose default layout parks dimensions on
     `AXIS_OUT`: TDB10224 then returns 124752 cells carrying only DATA_OSS,
     FENEC and VALORE — its region, sector and economic-activity coordinates are
     simply gone, and the rows are unattributable. `_rekey` detects this
     (AXIS_OUT minus the row/column axes is non-empty) and re-requests with those
     dimensions moved onto AXIS_ROWS and `keepTableRequest=true`, without which
     the server silently recomputes its default layout. The re-request answers
     with a composite column — key `"DATA_OSS|ATECO_CTP|CUBEID|..."`, value
     `"2010-06-30 00:00:00|F|TDB10224_52000139|..."` — which `_split_composite`
     unpacks back into one column per dimension.

EXPORTDATA/CSVONLINE is the app's other data path, but it needs a `dataSelector`
built from a prior in-session response and is capped at 10 cubes / 6500 rows per
call. PROSPETTODATI has no such cap: one call returns all 1316 series of
TFAA0000 (14.5MB). `limits.view.timeSeries` advertises 104 but is not enforced
on this path.

Two observation shapes exist, and both are written through verbatim (the
transform stage owns reshaping); on top of them we stamp four canonical columns
— `table_id`, `series_id`, `date`, `value` — so every table can be asserted
against the same test vocabulary:

  * standard (450 tables): `CUBEID` + `DATA_OSS` + `VALORE` plus SDMX dimensions.
  * measure-named (PRINC_IND_01_01, PUBBL_00_04_01_02, PUBBL_00_02_01_04_03):
    ECB rate-decision registries with no VALORE/DATA_OSS. Each row's `MEASURES`
    field names the column holding its value, and the date is in DATA_DECOR /
    DATA_DECOR_RIFPRI / DATA_PROV. Rows within these tables carry different key
    sets, so the raw schema is unioned per table.

Sizing. Observation volume per call is (series x periods), and periods vary by
four orders of magnitude across tables — TFAA0000 is 1316 annual series x 31
periods, TRI30021 is 5 daily series x ~368k periods (1.8M observations). Chunking
on series count alone therefore bounds nothing, so `_chunk_size` probes one
series first and sizes the chunk to an observation budget. Rows stream straight
to gzipped NDJSON, so peak memory is one chunk's parsed response.

Stateless full re-pull: 453 tables / ~13.2k series, and the source exposes no
delta query (each CUBE carries LAST_UPD, but there is no server-side
"changed since" filter). Revisions and restatements — routine in banking
statistics — are therefore picked up for free. No MAINTAIN_SPECS: the only
freshness signal is per-series LAST_UPD, and reading it costs one HTTP call per
table, i.e. the same round trips a refetch costs, so gating on it buys nothing.

Convergence (2026-07-26, problems 089/007). Two failure modes wedged the
continuation chain for 17 days and both are handled here rather than by
retrying harder:

  * A multi-chunk table that could not finish inside one leg used to restart
    from chunk 0 every leg (the single `raw_writer` covered the whole table).
    Chunked tables now write one NAMED raw fragment per chunk
    (`part-<idx>`), check the leg's remaining time between chunks, and return
    True (the orchestrator's pagination hand-off) when the per-node slice of
    the budget is spent — the staged fragments commit, and the next leg
    resumes past them via `list_raw_fragments` scoped to this run_id. This is
    the statistics-denmark pattern; the chain guard reads the growing raw
    listing as progress.
  * The rekey of the biggest multidimensional cubes is INFEASIBLE upstream:
    InfoStat computes the rekeyed pivot server-side and 500s after ~360s
    (measured on TDB20290, 502k cells, from a cold IP with zero load — it is
    deterministic, not rate limiting; date-range and pagination hints in
    TABLEREQUEST are ignored). The old retry stack (6 transient_retry x 4
    http-client attempts x 600s read timeout) turned each such cube into a
    multi-hour burn that ate the whole leg. Now: HTTP-layer retries are
    disabled for this connector (HTTP_RETRY_ATTEMPTS=1 — the decorators here
    own the policy), the rekey request gets ONE slow attempt (a 500 after
    >120s of server compute is the ceiling, not a lapsed session, and raises
    RekeyInfeasible immediately), and a single-series cube whose observation
    count already exceeds REKEY_MAX_SINGLE_SERIES fails before issuing the
    doomed request at all. Cubes that prove infeasible are `waive-spec`
    material (precedent: tdb10295).
"""

import json
import os
import time

from constants import TABLE_BY_SPEC
from subsets_utils import NodeSpec, get, list_raw_fragments, post, raw_writer, transient_retry
from subsets_utils import raw_manifest

# The shared http client retries 429/5xx and transient network errors
# HTTP_RETRY_ATTEMPTS times per request. InfoStat's failure modes are either
# cheap (lapsed session — reseed and go) or deterministic (the rekey compute
# ceiling), so blind per-request retries only multiply the burn; the
# decorators in this module own the whole retry policy. setdefault: an
# operator can still override per run.
os.environ.setdefault("HTTP_RETRY_ATTEMPTS", "1")

SLUG = "bank-of-italy"
HOME = "https://infostat.bancaditalia.it/inquiry/home"

# Target observations per PROSPETTODATI call. Peak RSS is dominated by the
# parsed response, so this is the real memory knob; series-per-call is derived.
OBS_BUDGET = 300_000
MAX_SERIES_PER_CALL = 200

# Cubes whose default layout drops dimensions must be re-requested rekeyed,
# and the rekeyed pivot is a server-side compute that hard-500s at ~360s.
# tdb10224 (124k cells) completes; TDB20290 (502k) does not. Chunks for
# rekey-class tables are sized to this smaller budget, and a SINGLE series
# past REKEY_MAX_SINGLE_SERIES is failed upfront as upstream-impractical
# instead of burning a leg discovering it again.
REKEY_OBS_BUDGET = 100_000
REKEY_MAX_SINGLE_SERIES = 200_000

# A single series that alone blows this many observations means the source grew
# a shape we have never seen (the current worst is ~368k). Raise rather than
# silently OOM or truncate.
MAX_OBS_PER_SERIES = 2_000_000

# Leg-budget continuation (see module docstring). One node may spend at most
# _LEG_FRACTION of the leg's DAG_TIME_BUDGET, and never schedule a new chunk
# request inside the last _DEADLINE_MARGIN_S before the parent's deadline.
_RUN_STARTED_AT_ENV = "BOI_RUN_STARTED_AT"  # exported by src/main.py per leg
_DEFAULT_TIME_BUDGET_S = 20_700.0
_LEG_FRACTION = 0.5
_DEADLINE_MARGIN_S = 15 * 60


class RekeyInfeasible(RuntimeError):
    """The rekeyed pivot for this cube exceeds InfoStat's server compute
    ceiling — permanent for the cube at its current size; waive-spec it."""


def _leg_deadline() -> float:
    """`time.time()` after which this node must stop starting new chunk
    requests, commit what it has, and hand off for a continuation leg."""
    try:
        budget = float(os.environ.get("DAG_TIME_BUDGET", "") or 0) or _DEFAULT_TIME_BUDGET_S
    except ValueError:
        budget = _DEFAULT_TIME_BUDGET_S
    nominal = budget * _LEG_FRACTION
    try:
        started = float(os.environ.get(_RUN_STARTED_AT_ENV, "") or 0) or None
    except ValueError:
        started = None
    if started is None:
        return time.time() + nominal
    remaining = budget - max(0.0, time.time() - started) - _DEADLINE_MARGIN_S
    return time.time() + max(0.0, min(nominal, remaining))


def _current_run_fragments(asset: str) -> set[str]:
    """Named fragments of this asset already COMMITTED under this run_id —
    the resume done-set. Never a directory listing (an uncommitted object
    does not exist; see list_raw_fragments)."""
    run_id = os.environ.get("RUN_ID", "unknown")
    return {
        key for key, meta in list_raw_fragments(asset, "ndjson.gz").items()
        if meta.get("run_id") == run_id
    }

_CUBEID, _VALUE = "CUBEID", "VALORE"
# Date columns, most authoritative first. Standard tables carry DATA_OSS; the
# measure-named registries carry the others.
_DATE_KEYS = ("DATA_OSS", "DATA_DECOR", "DATA_DECOR_RIFPRI", "DATA_PROV")
# Never emit a `<DIM>_label` twin for these — they are the value and the date,
# not coded dimensions.
_NO_LABEL = {_CUBEID, _VALUE, *_DATE_KEYS}

NO_GRAPH_SERIES = {
    # RTIT0100: the catalog includes this member, but PROSPETTODATI returns
    # ERROR 900/no GRAPHDATA for it even as a single-series request.
    "MFN_RTIT.M.020.202.922",
}

UPSTREAM_IMPRACTICAL_TABLES = {
    # TDB10295's default PROSPETTODATI response drops required coordinates; the
    # coordinate-complete rekey request ran for hours in CI without returning.
    "TDB10295",
}


def _seed_session() -> None:
    """Establish the JSESSIONID that every data service requires."""
    get(HOME, timeout=(10.0, 60.0))
    get(HOME, params={"service": "HOMEPAGE"}, timeout=(10.0, 60.0))


@transient_retry(attempts=4, min_wait=2, max_wait=30)
def _service(service: str, data, timeout=(10.0, 480.0)):
    resp = post(HOME, params={"calltype": "asin", "service": service}, data=data, timeout=timeout)
    if resp.status_code == 500:
        # "Risorsa Protetta" — the session lapsed. Reseed, then let the retry fire.
        _seed_session()
    resp.raise_for_status()
    body = resp.content.decode("utf-8-sig").strip()
    return json.loads(body) if body else None


def _service_rekey(data) -> dict | None:
    """The rekey POST, with its own policy instead of the layered retries.

    A 500 answered FAST is a lapsed session — reseed and try once more. A 500
    after minutes of server compute is InfoStat's pivot ceiling (measured:
    ~360s then 500, deterministically, for cubes past ~200k cells) — retrying
    is pure burn, so it raises RekeyInfeasible immediately."""
    for attempt in (1, 2):
        started = time.monotonic()
        resp = post(HOME, params={"calltype": "asin", "service": "PROSPETTODATI"},
                    data=data, timeout=(10.0, 480.0))
        if resp.status_code == 500:
            elapsed = time.monotonic() - started
            if elapsed > 120.0:
                raise RekeyInfeasible(
                    f"rekeyed PROSPETTODATI computed for {elapsed:.0f}s then 500 — "
                    "the cube exceeds InfoStat's server-side pivot ceiling "
                    "(upstream-impractical; waive-spec this table)"
                )
            _seed_session()
            if attempt == 2:
                resp.raise_for_status()
            continue
        resp.raise_for_status()
        body = resp.content.decode("utf-8-sig").strip()
        return json.loads(body) if body else None


def _resolve_table(table_id: str) -> dict:
    nodes = _service("GETNODESBYCUBEIDS", {"CUBEID": table_id}, timeout=(10.0, 120.0))
    if not nodes:
        raise RuntimeError(f"{table_id}: GETNODESBYCUBEIDS resolved no node")
    return nodes[0]


def _member_series(node: dict) -> list[str]:
    ref_path = node.get("nodePath") or node["parentAbsPath"].replace("\\", "/", 1)
    kids = _service(
        "SUBTREENODES",
        {
            "surveytree": node.get("nodePath") is None,
            "id": node["id"],
            "taxoSurveyId": node.get("taxoSurveyId"),
            "nodeType": node["nodeType"],
            "nodePath": ref_path,
            "childrenNumber": node.get("childrenNumber") or 0,
            "NUMITEMS": 20000,
            "STARTINDEX": 0,
            "localId": node["localId"],
        },
    )
    return [k["localId"] for k in (kids or []) if k.get("nodeType") == "CUBE"]


# The pivot layout echoed back as TABLEREQUEST: the response minus the fields
# the app itself strips before re-sending it.
_NOT_A_LAYOUT = {"result", "graphResponse", "descriptions"}


def _post_prospetto(cube_ids: list[str], extra: dict | None = None, *, rekey: bool = False) -> dict:
    body = {"CUBEIDS": ";".join(cube_ids), "VIEW_MODE": "table", "GRAPH_MODE": "false"}
    body.update(extra or {})
    payload = _service_rekey(body) if rekey else _service("PROSPETTODATI", body)
    if (payload or {}).get("GRAPHDATA") is None:
        raise RuntimeError(f"PROSPETTODATI returned no GRAPHDATA for {len(cube_ids)} series")
    return payload


def _dropped_dims(payload: dict) -> list[str]:
    """Dimensions the pivot aggregated away, so the observations cannot name them."""
    axis = payload["table"]["axis"]
    placed = set(axis.get("AXIS_ROWS") or []) | set(axis.get("AXIS_COLUMNS") or [])
    return sorted(set(axis.get("AXIS_OUT") or []) - placed)


def _rekey(cube_ids: list[str], payload: dict) -> dict:
    """Re-request with the dropped dimensions pinned onto the row axis."""
    dropped = _dropped_dims(payload)
    if not dropped:
        return payload

    layout = {k: v for k, v in payload.items() if k not in _NOT_A_LAYOUT}
    axis = layout["table"]["axis"]
    axis["AXIS_ROWS"] = list(axis.get("AXIS_ROWS") or []) + dropped
    axis["AXIS_OUT"] = []
    axis["AXIS_FILTERS"] = []
    rekeyed = _post_prospetto(
        cube_ids, {"TABLEREQUEST": json.dumps(layout), "keepTableRequest": "true"},
        rekey=True,
    )
    still_dropped = _dropped_dims(rekeyed)
    if still_dropped:
        raise RuntimeError(
            f"PROSPETTODATI kept {still_dropped} off the pivot axes after a rekey — "
            "its observations would be unattributable"
        )
    # Tag the payload so callers can tell the cube is rekey-class even though
    # the rekeyed response itself no longer shows dropped dims.
    rekeyed["_REKEYED"] = True
    return rekeyed


def _prospetto(cube_ids: list[str]) -> dict:
    try:
        return _rekey(cube_ids, _post_prospetto(cube_ids))
    except RuntimeError as exc:
        if "returned no GRAPHDATA" not in str(exc):
            raise
        if len(cube_ids) == 1:
            if cube_ids[0] in NO_GRAPH_SERIES:
                return {
                    "GRAPHDATA": {"observations": []},
                    "DOMAINELEMENTS": {
                        _CUBEID: [{"id": cube_ids[0], "name": cube_ids[0]}]
                    },
                }
            raise

        # Some otherwise valid tables fail only when too many series are sent
        # together. Split recursively and let the caller stream the subchunks.
        mid = max(1, len(cube_ids) // 2)
        left = _prospetto(cube_ids[:mid])
        right = _prospetto(cube_ids[mid:])
        observations = left["GRAPHDATA"].setdefault("observations", [])
        observations.extend(right["GRAPHDATA"].get("observations", []))
        for dim, elems in (right.get("DOMAINELEMENTS") or {}).items():
            left.setdefault("DOMAINELEMENTS", {}).setdefault(dim, [])
            seen = {
                e.get("id")
                for e in left["DOMAINELEMENTS"][dim]
                if isinstance(e, dict)
            }
            left["DOMAINELEMENTS"][dim].extend(
                e
                for e in elems
                if not isinstance(e, dict) or e.get("id") not in seen
            )
        return left


def _split_composite(values: dict) -> dict:
    """Unpack the pivot's composite row key: {"A|B": "1|2"} -> {"A": "1", "B": "2"}."""
    if not any("|" in k for k in values):
        return values
    out = {}
    for key, value in values.items():
        if "|" not in key:
            out[key] = value
            continue
        names = key.split("|")
        parts = (value or "").split("|")
        if len(names) != len(parts):
            raise RuntimeError(f"composite key {key!r} does not match value {value!r}")
        out.update(zip(names, parts))
    return out


def _chunk_size(table_id: str, cube_ids: list[str]) -> tuple[int, dict]:
    """Size the chunk by measuring one series first (OBS_BUDGET, or the
    smaller REKEY_OBS_BUDGET when the probe shows the cube needs a rekey).

    Returns the chunk size and the probe's payload, so the probe is not wasted.
    The probe runs BEFORE the infeasibility check on purpose: a rekey-class
    single series past REKEY_MAX_SINGLE_SERIES fails here in ~1 cheap request
    instead of discovering the server's pivot ceiling the slow way. NOTE the
    probe itself is rekeyed by `_prospetto`; for a single-member cube past the
    ceiling that one rekey attempt raises RekeyInfeasible first — also fine,
    also fast."""
    probe = _prospetto(cube_ids[:1])
    per_series = len(probe["GRAPHDATA"].get("observations", [])) or 1
    if per_series > MAX_OBS_PER_SERIES:
        raise RuntimeError(
            f"{table_id}: one series carries {per_series} observations, past the "
            f"{MAX_OBS_PER_SERIES} ceiling — the source changed shape"
        )
    rekey_class = bool(probe.get("_REKEYED"))
    budget = REKEY_OBS_BUDGET if rekey_class else OBS_BUDGET
    if rekey_class and per_series > REKEY_MAX_SINGLE_SERIES:
        raise RekeyInfeasible(
            f"{table_id}: a single series carries {per_series} rekey-class "
            f"observations (> {REKEY_MAX_SINGLE_SERIES}) — the rekeyed pivot "
            "exceeds InfoStat's server ceiling (upstream-impractical; "
            "waive-spec this table)"
        )
    return max(1, min(MAX_SERIES_PER_CALL, budget // per_series)), probe


def _clean(raw):
    """The app serialises SQL NULL as the four-character string 'null'."""
    return None if raw in (None, "", "null") else raw


def _as_float(raw):
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def _label_dims(payload: dict) -> list[str]:
    """Dimensions whose DOMAINELEMENTS carry a description distinct from the code."""
    out = []
    for dim, elems in (payload.get("DOMAINELEMENTS") or {}).items():
        if dim in _NO_LABEL:
            continue
        if any(isinstance(e, dict) and e.get("name") not in (None, e.get("id")) for e in elems):
            out.append(dim)
    return sorted(out)


def _labels(payload: dict) -> dict[str, dict[str, str]]:
    return {
        dim: {e["id"]: e.get("name") for e in elems if isinstance(e, dict) and "id" in e}
        for dim, elems in (payload.get("DOMAINELEMENTS") or {}).items()
    }


def _rows(table_id: str, payload: dict, schema: list[str], label_dims: list[str]):
    known = set(schema)
    labels = _labels(payload)
    series_names = labels.get(_CUBEID, {})
    for obs in payload["GRAPHDATA"].get("observations", []):
        values = {k: _clean(v) for k, v in _split_composite(obs["values"]).items()}

        # `MEASURES` names the column holding this row's value on the registry
        # tables; standard tables put it in VALORE.
        measure = values.get("MEASURES")
        value = values.get(_VALUE) if _VALUE in values else (values.get(measure) if measure else None)
        date = next((values[k] for k in _DATE_KEYS if values.get(k)), None)
        series_id = values.get(_CUBEID) or table_id

        row = dict.fromkeys(schema)
        row.update(values)
        row["table_id"] = table_id
        row["series_id"] = series_id
        row["series_name"] = series_names.get(series_id)
        row["date"] = date[:10] if date else None
        row["value"] = _as_float(value)
        for dim in label_dims:
            row[f"{dim}_label"] = labels.get(dim, {}).get(values.get(dim))

        extra = row.keys() - known
        if extra:
            raise RuntimeError(f"{table_id}: observation grew unexpected keys {sorted(extra)}")
        yield row


def _schema(payload: dict, label_dims: list[str]) -> list[str]:
    """Column union for the table, fixed from its first chunk.

    Standard tables have exactly one observation key-set; the registry tables
    vary row to row, but they are small enough that the first chunk is the whole
    table, so its union is complete. Later drift raises in `_rows` rather than
    writing a ragged file that DuckDB's schema inference would silently
    under-read (a column absent from the leading sample fails to bind).
    """
    keys = {"table_id", "series_id", "series_name", "date", "value"}
    keys |= {f"{d}_label" for d in label_dims}
    for obs in payload["GRAPHDATA"].get("observations", []):
        keys |= _split_composite(obs["values"]).keys()
    return sorted(keys)


def _write_payload(asset: str, table_id: str, payload: dict, schema: list[str],
                   label_dims: list[str], fragment: str | None) -> int:
    """Stream one payload's rows to a raw NDJSON object (whole asset when
    `fragment` is None, a named fragment otherwise). Returns rows written."""
    written = 0
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip", fragment=fragment) as out:
        for row in _rows(table_id, payload, schema, label_dims):
            out.write(json.dumps(row, separators=(",", ":")) + "\n")
            written += 1
    return written


def fetch_one(node_id: str) -> bool | None:
    """Fetch one table. Returns True when this node's slice of the leg budget
    is spent with chunks still unfetched — the orchestrator's pagination
    hand-off: the fragments staged so far commit, the run finalizes as
    needs_continuation, and the next leg (same run_id) resumes past them.
    Returns None when the table is fully drained."""
    asset = node_id
    table_id = TABLE_BY_SPEC[node_id.removeprefix(f"{SLUG}-")]
    if table_id in UPSTREAM_IMPRACTICAL_TABLES:
        raise RuntimeError(
            f"{table_id}: upstream-impractical PROSPETTODATI rekey; see active waiver"
        )

    _seed_session()
    # Sorted for a deterministic chunk -> fragment mapping across legs. A
    # membership change BETWEEN legs of one run can shift chunk boundaries
    # (accepted risk, same as statistics-denmark: upstream adds mid-run are
    # rare, and the next full run re-pulls everything anyway).
    cube_ids = sorted(_member_series(_resolve_table(table_id)))
    if not cube_ids:
        raise RuntimeError(f"{table_id}: table resolved but exposes no member series")

    size, probe = _chunk_size(table_id, cube_ids)
    chunks = [cube_ids[start:start + size] for start in range(0, len(cube_ids), size)]

    # Schema fixed from the probe so every fragment of the asset carries the
    # same column set (DuckDB reads them as one relation). Standard tables
    # have one key-set table-wide and DOMAINELEMENTS is cube-level, so the
    # probe's single series determines both; drift raises in `_rows`.
    label_dims = _label_dims(probe)
    schema = _schema(probe, label_dims)

    if len(chunks) == 1:
        # Single-chunk table (the 175 light tables and the registry tables):
        # one whole-asset write, exactly the pre-2026-07-26 behavior. The
        # registry tables vary keys row-to-row, so their schema comes from the
        # full payload rather than the probe.
        payload = probe if size == 1 else _prospetto(chunks[0])
        label_dims = _label_dims(payload)
        schema = _schema(payload, label_dims)
        written = _write_payload(asset, table_id, payload, schema, label_dims, None)
        if not written:
            raise RuntimeError(
                f"{table_id}: {len(cube_ids)} series resolved but no observations returned"
            )
        return None

    done = _current_run_fragments(asset)
    if not done:
        # Fresh (re)fetch of a chunked table: stage removal of the asset's
        # previous manifest entry (a prior run's whole-asset object, or stale
        # part-* keys from a run with more chunks) so the committed fragment
        # set is exactly this run's chunks — never a mix of vintages. Ops are
        # applied in order on node success: delete first, then this run's
        # puts. Objects themselves are untouched (run-scoped, gc-raw's job).
        raw_manifest.stage_delete(asset, "ndjson.gz")
    deadline = _leg_deadline()
    written = 0
    requests_this_leg = 0
    for idx, chunk in enumerate(chunks):
        fragment = f"part-{idx:05d}"
        if fragment in done:
            continue
        # Out of this leg's slice with chunks still to fetch: commit what
        # landed and request a continuation leg. Always make at least one
        # request first so every leg advances (guards the chain-guard
        # no-progress brake).
        if requests_this_leg and time.time() >= deadline:
            print(f"  -> {table_id}: leg budget spent at chunk {idx}/{len(chunks)} "
                  f"— committing {requests_this_leg} fragment(s) and requesting continuation")
            return True
        payload = probe if (idx == 0 and size == 1) else _prospetto(chunk)
        requests_this_leg += 1
        if payload["GRAPHDATA"].get("observations"):
            written += _write_payload(asset, table_id, payload, schema, label_dims, fragment)
        # else: no fragment written — an empty NDJSON object would break the
        # multi-file DuckDB read; the chunk is simply re-asked next leg (cheap).
        time.sleep(0.5)  # be polite: InfoStat load-sheds under sustained hammering

    if not written and not done:
        raise RuntimeError(
            f"{table_id}: {len(cube_ids)} series resolved but no observations returned"
        )
    return None


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{suffix}", fn=fetch_one, kind="download") for suffix in sorted(TABLE_BY_SPEC)
]
