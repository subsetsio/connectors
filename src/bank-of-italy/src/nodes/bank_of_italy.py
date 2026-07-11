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
"""

import json

from constants import TABLE_BY_SPEC
from subsets_utils import NodeSpec, get, post, raw_writer, transient_retry

SLUG = "bank-of-italy"
HOME = "https://infostat.bancaditalia.it/inquiry/home"

# Target observations per PROSPETTODATI call. Peak RSS is dominated by the
# parsed response, so this is the real memory knob; series-per-call is derived.
OBS_BUDGET = 300_000
MAX_SERIES_PER_CALL = 200

# A single series that alone blows this many observations means the source grew
# a shape we have never seen (the current worst is ~368k). Raise rather than
# silently OOM or truncate.
MAX_OBS_PER_SERIES = 2_000_000

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


def _seed_session() -> None:
    """Establish the JSESSIONID that every data service requires."""
    get(HOME, timeout=(10.0, 60.0))
    get(HOME, params={"service": "HOMEPAGE"}, timeout=(10.0, 60.0))


@transient_retry()
def _service(service: str, data, timeout=(10.0, 600.0)):
    resp = post(HOME, params={"calltype": "asin", "service": service}, data=data, timeout=timeout)
    if resp.status_code == 500:
        # "Risorsa Protetta" — the session lapsed. Reseed, then let the retry fire.
        _seed_session()
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


def _post_prospetto(cube_ids: list[str], extra: dict | None = None) -> dict:
    body = {"CUBEIDS": ";".join(cube_ids), "VIEW_MODE": "table", "GRAPH_MODE": "false"}
    body.update(extra or {})
    payload = _service("PROSPETTODATI", body)
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
        cube_ids, {"TABLEREQUEST": json.dumps(layout), "keepTableRequest": "true"}
    )
    still_dropped = _dropped_dims(rekeyed)
    if still_dropped:
        raise RuntimeError(
            f"PROSPETTODATI kept {still_dropped} off the pivot axes after a rekey — "
            "its observations would be unattributable"
        )
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
    """Size the chunk to OBS_BUDGET by measuring one series first.

    Returns the chunk size and the probe's payload, so the probe is not wasted.
    """
    probe = _prospetto(cube_ids[:1])
    per_series = len(probe["GRAPHDATA"].get("observations", [])) or 1
    if per_series > MAX_OBS_PER_SERIES:
        raise RuntimeError(
            f"{table_id}: one series carries {per_series} observations, past the "
            f"{MAX_OBS_PER_SERIES} ceiling — the source changed shape"
        )
    return max(1, min(MAX_SERIES_PER_CALL, OBS_BUDGET // per_series)), probe


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


def fetch_one(node_id: str) -> None:
    asset = node_id
    table_id = TABLE_BY_SPEC[node_id.removeprefix(f"{SLUG}-")]

    _seed_session()
    cube_ids = _member_series(_resolve_table(table_id))
    if not cube_ids:
        raise RuntimeError(f"{table_id}: table resolved but exposes no member series")

    size, probe = _chunk_size(table_id, cube_ids)

    written = 0
    schema = label_dims = None
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as out:
        for start in range(0, len(cube_ids), size):
            chunk = cube_ids[start : start + size]
            # The probe already fetched the first series; reuse it when it is the
            # whole first chunk, otherwise re-request the chunk as a unit.
            payload = probe if (start == 0 and size == 1) else _prospetto(chunk)
            if schema is None:
                label_dims = _label_dims(payload)
                schema = _schema(payload, label_dims)
            for row in _rows(table_id, payload, schema, label_dims):
                out.write(json.dumps(row, separators=(",", ":")) + "\n")
                written += 1

    if not written:
        raise RuntimeError(f"{table_id}: {len(cube_ids)} series resolved but no observations returned")


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{suffix}", fn=fetch_one, kind="download") for suffix in sorted(TABLE_BY_SPEC)
]
