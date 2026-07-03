"""Argo Program connector — Ifremer ERDDAP tabledap/griddap.

Five published subsets, one DOWNLOAD_SPEC + one SQL TRANSFORM each:

  argo-program-argofloats                core T/S vertical profiles (flagship)
  argo-program-argofloats-synthetic-bgc  biogeochemical synthetic profiles
  argo-program-argofloats-reference      DMQC reference profiles (1998-2022)
  argo-program-argofloats-index          per-profile global index/catalog
  argo-program-oacp-argo-global          global mode-water/pycnocline climatology (grid)

Fetch shapes:

  * The three measurement datasets (ArgoFloats, BGC, reference) are
    record-stream firehoses — billions of (profile x pressure-level) rows over
    1997-present. We can't pull them whole, so we batch by time window
    (`time>=start & time<end`), one parquet file per window, advancing a
    monotonic ISO-timestamp watermark in state. No self-imposed run budget: the
    loop walks windows until it reaches the present (or the dataset's fixed end
    for the historical reference set); the supervisor caps wall-clock and the
    next run resumes from the saved watermark. Window sizes are picked to stay
    under ERDDAP's per-response cap (one recent ArgoFloats week ~250MB CSV).
    Empty windows (early years, gaps) return ERDDAP 404 "no matching results" —
    treated as empty, not an error, and the watermark still advances.

  * The index (~3.4M rows) and the OACP climatology grid (~65k cells) are small
    enough to re-pull whole every run (stateless overwrite).

All time vars are kept as ISO strings in raw parquet; the SQL transforms cast
them. Numeric columns are typed at fetch (empty / "NaN" -> null).
"""

import csv
import io
from contextlib import ExitStack
from datetime import datetime, timedelta, timezone

import httpx
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    load_state,
    raw_parquet_writer,
    save_state,
    transient_retry,
)

ERDDAP = "https://erddap.ifremer.fr/erddap"
STATE_VERSION = 1
FLUSH_ROWS = 200_000          # row-group flush size for the streaming writer
MAX_WINDOWS = 4000            # safety ceiling per fetch; raises on runaway

# ---- column schemas (name, arrow type). Time vars stay string, cast in SQL. --

AF_COLS = [
    ("platform_number", pa.string()),
    ("cycle_number", pa.int32()),
    ("time", pa.string()),
    ("latitude", pa.float64()),
    ("longitude", pa.float64()),
    ("pres", pa.float64()),
    ("temp", pa.float64()),
    ("psal", pa.float64()),
    ("pres_qc", pa.string()),
    ("temp_qc", pa.string()),
    ("psal_qc", pa.string()),
    ("data_mode", pa.string()),
    ("direction", pa.string()),
]

BGC_COLS = [
    ("platform_number", pa.string()),
    ("cycle_number", pa.int32()),
    ("time", pa.string()),
    ("latitude", pa.float64()),
    ("longitude", pa.float64()),
    ("pres", pa.float64()),
    ("temp", pa.float64()),
    ("psal", pa.float64()),
    ("doxy", pa.float64()),
    ("chla", pa.float64()),
    ("nitrate", pa.float64()),
    ("bbp700", pa.float64()),
    ("ph_in_situ_total", pa.float64()),
]

REF_COLS = [
    ("platform_number", pa.string()),
    ("cycle_number", pa.int32()),
    ("time", pa.string()),
    ("latitude", pa.float64()),
    ("longitude", pa.float64()),
    ("pres", pa.float64()),
    ("temp", pa.float64()),
    ("psal", pa.float64()),
    ("ptmp", pa.float64()),
]

INDEX_COLS = [
    ("file", pa.string()),
    ("date", pa.string()),
    ("latitude", pa.float64()),
    ("longitude", pa.float64()),
    ("ocean", pa.string()),
    ("profiler_type", pa.string()),
    ("institution", pa.string()),
    ("date_update", pa.string()),
]

# node_id -> firehose config for the three time-windowed measurement datasets.
TS_DATASETS = {
    "argo-program-argofloats": {
        "dataset": "ArgoFloats",
        "coldefs": AF_COLS,
        "start": "1997-07-01T00:00:00Z",
        "step_days": 7,
    },
    "argo-program-argofloats-synthetic-bgc": {
        "dataset": "ArgoFloats-synthetic-BGC",
        "coldefs": BGC_COLS,
        "start": "2002-09-01T00:00:00Z",
        "step_days": 14,
    },
    "argo-program-argofloats-reference": {
        "dataset": "ArgoFloats-reference",
        "coldefs": REF_COLS,
        "start": "1998-08-01T00:00:00Z",
        "end": "2022-10-01T00:00:00Z",   # dataset is historical, ends 2022-09
        "step_days": 30,
    },
}

# ----------------------------------------------------------------------------
# HTTP


@transient_retry()
def _http_get(url: str) -> httpx.Response:
    resp = get(url, timeout=(15.0, 600.0))
    resp.raise_for_status()
    return resp


def _fetch_csv(url: str) -> str:
    """GET an ERDDAP .csv. Returns "" when the query matched no rows (ERDDAP
    answers an empty selection with HTTP 404 'no matching results')."""
    try:
        return _http_get(url).text
    except httpx.HTTPStatusError as exc:
        resp = exc.response
        if resp.status_code == 404 and "no matching results" in resp.text.lower():
            return ""
        raise


# ----------------------------------------------------------------------------
# CSV -> streamed parquet


def _coerce(arrow_type: pa.DataType, value: str):
    v = (value or "").strip()
    if v == "" or v.lower() == "nan":
        return None
    if pa.types.is_floating(arrow_type):
        return float(v)
    if pa.types.is_integer(arrow_type):
        return int(float(v))
    return v


def _write_csv_parquet(text: str, coldefs, asset_id: str) -> int:
    """Parse an ERDDAP CSV body (2 header lines: names, then units) into one
    parquet asset, flushing row groups every FLUSH_ROWS to bound memory.
    Writes nothing (no file) when there are zero data rows. Returns row count."""
    schema = pa.schema(coldefs)
    names = [n for n, _ in coldefs]
    types = {n: t for n, t in coldefs}

    reader = csv.reader(io.StringIO(text))
    try:
        header = next(reader)
        next(reader)  # units line
    except StopIteration:
        return 0
    idx = {n: header.index(n) for n in names if n in header}
    missing = [n for n in names if n not in idx]
    if missing:
        raise KeyError(f"{asset_id}: columns absent from ERDDAP response: {missing}")

    buf = {n: [] for n in names}
    nbuf = 0
    total = 0

    with ExitStack() as stack:
        writer = None

        def flush():
            nonlocal writer, nbuf, buf
            if nbuf == 0:
                return
            if writer is None:
                writer = stack.enter_context(raw_parquet_writer(asset_id, schema))
            arrays = [pa.array(buf[n], type=types[n]) for n in names]
            writer.write_table(pa.Table.from_arrays(arrays, schema=schema))
            buf = {n: [] for n in names}
            nbuf = 0

        for row in reader:
            if not row:
                continue
            for n in names:
                j = idx[n]
                buf[n].append(_coerce(types[n], row[j] if j < len(row) else ""))
            nbuf += 1
            total += 1
            if nbuf >= FLUSH_ROWS:
                flush()
        flush()

    return total


# ----------------------------------------------------------------------------
# time helpers


def _parse(iso: str) -> datetime:
    return datetime.fromisoformat(iso.replace("Z", "+00:00"))


def _iso(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


# ----------------------------------------------------------------------------
# fetch fns


def fetch_timeseries(node_id: str) -> None:
    """Time-windowed firehose for a measurement dataset. One parquet per window;
    watermark advances monotonically; resumes across runs."""
    cfg = TS_DATASETS[node_id]
    coldefs = cfg["coldefs"]
    cols = [n for n, _ in coldefs]

    state = load_state(node_id)
    if state.get("schema_version") != STATE_VERSION:
        state = {}
    watermark = state.get("watermark") or cfg["start"]

    now = datetime.now(timezone.utc)
    end_cap = now
    if cfg.get("end"):
        end_cap = min(now, _parse(cfg["end"]))
    step = timedelta(days=cfg["step_days"])

    cur = _parse(watermark)
    windows = 0
    while cur < end_cap:
        windows += 1
        if windows > MAX_WINDOWS:
            raise RuntimeError(
                f"{node_id}: exceeded MAX_WINDOWS={MAX_WINDOWS} at {_iso(cur)} "
                "- source grew past expectations, investigate before raising the cap"
            )
        win_end = min(cur + step, end_cap)
        url = (
            f"{ERDDAP}/tabledap/{cfg['dataset']}.csv?"
            + ",".join(cols)
            + f"&time%3E={_iso(cur)}&time%3C={_iso(win_end)}"
        )
        text = _fetch_csv(url)
        if text:
            asset = f"{node_id}-{cur.strftime('%Y-%m-%d')}"
            _write_csv_parquet(text, coldefs, asset)   # raw FIRST
        cur = win_end
        save_state(node_id, {                          # then advance state
            "schema_version": STATE_VERSION,
            "watermark": _iso(cur),
            "last_success_at": _iso(now),
        })


def fetch_index(node_id: str) -> None:
    """Per-profile global index — small enough to re-pull whole each run."""
    cols = [n for n, _ in INDEX_COLS]
    url = f"{ERDDAP}/tabledap/ArgoFloats-index.csv?" + ",".join(cols)
    text = _fetch_csv(url)
    if not text:
        raise RuntimeError(f"{node_id}: ArgoFloats-index returned no data")
    _write_csv_parquet(text, INDEX_COLS, node_id)


def fetch_grid(node_id: str) -> None:
    """OACP global climatology — a lat x lon grid of mode-water / pycnocline
    properties, pulled in full via griddap. Grid variables discovered live."""
    info = _http_get(f"{ERDDAP}/info/OACP-Argo-Global/index.json").json()["table"]
    c = info["columnNames"]
    rt, vn = c.index("Row Type"), c.index("Variable Name")
    gvars = [r[vn] for r in info["rows"] if r[rt] == "variable"]
    if not gvars:
        raise RuntimeError(f"{node_id}: no grid variables discovered for OACP-Argo-Global")

    # griddap CSV always prefixes the dimension columns (latitude, longitude).
    coldefs = [("latitude", pa.float64()), ("longitude", pa.float64())] + [
        (v, pa.float64()) for v in gvars
    ]
    url = f"{ERDDAP}/griddap/OACP-Argo-Global.csv?" + ",".join(gvars)
    text = _fetch_csv(url)
    if not text:
        raise RuntimeError(f"{node_id}: OACP-Argo-Global griddap returned no data")
    _write_csv_parquet(text, coldefs, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="argo-program-argofloats", fn=fetch_timeseries, kind="download"),
    NodeSpec(id="argo-program-argofloats-synthetic-bgc", fn=fetch_timeseries, kind="download"),
    NodeSpec(id="argo-program-argofloats-reference", fn=fetch_timeseries, kind="download"),
    NodeSpec(id="argo-program-argofloats-index", fn=fetch_index, kind="download"),
    NodeSpec(id="argo-program-oacp-argo-global", fn=fetch_grid, kind="download"),
]

# ----------------------------------------------------------------------------
# transforms — thin parse/type passes, one published Delta table each.

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="argo-program-argofloats-transform",
        deps=["argo-program-argofloats"],
        sql='''
            SELECT
                platform_number,
                cycle_number,
                CAST(time AS TIMESTAMPTZ) AS time,
                latitude,
                longitude,
                pres,
                temp,
                psal,
                pres_qc,
                temp_qc,
                psal_qc,
                data_mode,
                direction
            FROM "argo-program-argofloats"
            WHERE time IS NOT NULL
              AND (temp IS NOT NULL OR psal IS NOT NULL)
        ''',
    ),
    SqlNodeSpec(
        id="argo-program-argofloats-synthetic-bgc-transform",
        deps=["argo-program-argofloats-synthetic-bgc"],
        sql='''
            SELECT
                platform_number,
                cycle_number,
                CAST(time AS TIMESTAMPTZ) AS time,
                latitude,
                longitude,
                pres,
                temp,
                psal,
                doxy,
                chla,
                nitrate,
                bbp700,
                ph_in_situ_total
            FROM "argo-program-argofloats-synthetic-bgc"
            WHERE time IS NOT NULL AND pres IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="argo-program-argofloats-reference-transform",
        deps=["argo-program-argofloats-reference"],
        sql='''
            SELECT
                platform_number,
                cycle_number,
                CAST(time AS TIMESTAMPTZ) AS time,
                latitude,
                longitude,
                pres,
                temp,
                psal,
                ptmp
            FROM "argo-program-argofloats-reference"
            WHERE time IS NOT NULL AND pres IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="argo-program-argofloats-index-transform",
        deps=["argo-program-argofloats-index"],
        sql='''
            SELECT
                file,
                CAST(date AS TIMESTAMPTZ) AS date,
                latitude,
                longitude,
                ocean,
                profiler_type,
                institution,
                CAST(date_update AS TIMESTAMPTZ) AS date_update
            FROM "argo-program-argofloats-index"
            WHERE file IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="argo-program-oacp-argo-global-transform",
        deps=["argo-program-oacp-argo-global"],
        sql='''
            SELECT *
            FROM "argo-program-oacp-argo-global"
            WHERE latitude IS NOT NULL
              AND longitude IS NOT NULL
              AND GLOBAL_PPD IS NOT NULL
        ''',
    ),
]
