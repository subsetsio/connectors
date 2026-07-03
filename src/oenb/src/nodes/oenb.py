"""Oesterreichische Nationalbank (OeNB) connector.

Mechanism: the OeNB Data Web Service ("isadataservice"), a custom XML REST API.
One published subset per OeNB statistical dataset (TOC leaf `hierid`). Each
dataset holds a set of time-series `position` codes; a position can expand into
several dimension-keyed series (e.g. by counterpart sector / instrument), so the
series identity is (pos, dimensions, freq, period).

Fetch shape: stateless full re-pull. The corpus is small (31 datasets, low
thousands of series total) and the API exposes no modified-since filter, so each
run re-fetches every dataset in full over a wide date window and overwrites.
Per dataset we (1) list its positions from /content?hierid, then (2) for each
candidate frequency request /data with the positions batched, unioning every
non-empty observation. Frequencies the dataset doesn't use return empty and are
skipped. Raw is streamed to ndjson.gz because dimension columns vary per record
and a few datasets (balance of payments) fan out to many rows.
"""

import xml.etree.ElementTree as ET

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_parquet_writer,
    transient_retry,
)

# Explicit, uniform schema — dimensions are flattened into the single `dim_key`
# string, so every observation row has the same columns and types. Declaring it
# up front (rather than auto-inferring from ndjson) is what makes the raw read
# back deterministically for datasets with hundreds of thousands of rows.
SCHEMA = pa.schema([
    ("hierid", pa.string()),
    ("pos", pa.string()),
    ("pos_title", pa.string()),
    ("freq", pa.string()),
    ("period", pa.string()),
    ("value", pa.float64()),
    ("unit_text", pa.string()),
    ("unit_mult", pa.string()),
    ("dim_key", pa.string()),
])

# Flush the row buffer to a parquet row group at this size to bound memory.
FLUSH_ROWS = 50_000

BASE = "https://www.oenb.at/isadataservice"

# Candidate frequency codes. The service has no endpoint listing which
# frequencies a dataset uses, so we probe each and union what comes back;
# unused frequencies return an empty <data/> and cost only one tiny request.
FREQS = ["D", "W", "M", "Q", "S", "H", "A"]

# Wide window covering the full history of every series. Full ISO dates are
# accepted for every frequency (daily through annual).
START = "1900-01-01"
END = "2099-12-31"

# Positions per /data request. Codes are ~14-20 chars; 40 keeps the URL well
# under any practical length limit while bounding the response size.
POS_BATCH = 40

# Entity union — the 31 rank-active OeNB TOC leaf datasets (hierids).
from constants import ENTITY_IDS


@transient_retry()
def _get_xml(path: str, params) -> ET.Element:
    resp = get(f"{BASE}/{path}", params=params, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return ET.fromstring(resp.content)


def _list_positions(hierid: str) -> list[str]:
    """Distinct position codes belonging to a dataset (deduped across groups)."""
    root = _get_xml("content", [("lang", "EN"), ("hierid", hierid)])
    seen, out = set(), []
    for pos in root.findall(".//groups/group/position"):
        pid = pos.get("id")
        if pid and pid not in seen:
            seen.add(pid)
            out.append(pid)
    return out


def _chunks(items, n):
    for i in range(0, len(items), n):
        yield items[i:i + n]


def _dim_key(ds: ET.Element) -> str:
    """Stable '|'-joined dimension code signature (attr1, attr2, ...)."""
    codes, i = [], 1
    while ds.get(f"attr{i}") is not None:
        codes.append(ds.get(f"attr{i}"))
        i += 1
    return "|".join(codes)


def fetch_one(node_id: str) -> None:
    asset = node_id
    hierid = node_id[len("oenb-"):]
    positions = _list_positions(hierid)
    if not positions:
        raise RuntimeError(f"{node_id}: dataset {hierid} listed no positions")

    n_rows = 0
    buf: list[dict] = []
    with raw_parquet_writer(asset, SCHEMA) as writer:
        def flush():
            if buf:
                writer.write_table(pa.Table.from_pylist(buf, schema=SCHEMA))
                buf.clear()

        for freq in FREQS:
            for batch in _chunks(positions, POS_BATCH):
                params = [("lang", "EN"), ("hierid", hierid), ("freq", freq),
                          ("starttime", START), ("endtime", END)]
                params += [("pos", p) for p in batch]
                root = _get_xml("data", params)
                for ds in root.findall(".//dataSet"):
                    pos = ds.get("pos")
                    pos_title = ds.get("posTitle")
                    unit_text = ds.get("unitText")
                    unit_mult = ds.get("unitMult")
                    dim_key = _dim_key(ds)
                    for obs in ds.findall(".//obs"):
                        try:
                            value = float(obs.get("value"))
                        except (TypeError, ValueError):
                            continue
                        buf.append({
                            "hierid": hierid,
                            "pos": pos,
                            "pos_title": pos_title,
                            "freq": freq,
                            "period": obs.get("periode"),
                            "value": value,
                            "unit_text": unit_text,
                            "unit_mult": unit_mult,
                            "dim_key": dim_key,
                        })
                        n_rows += 1
                        if len(buf) >= FLUSH_ROWS:
                            flush()
        flush()

    if n_rows == 0:
        raise RuntimeError(f"{node_id}: dataset {hierid} returned no observations")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"oenb-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


# One published Delta table per dataset: long-format observations with a
# best-effort DATE derived from the period string (NULL for weekly/semiannual,
# where the raw `period`/`frequency` remain authoritative).
_SQL = '''
    WITH base AS (
        SELECT *, CAST(period AS VARCHAR) AS p
        FROM "{dep}"
    )
    SELECT
        CASE freq
            WHEN 'A' THEN make_date(TRY_CAST(p AS INTEGER), 1, 1)
            WHEN 'M' THEN make_date(
                TRY_CAST(substr(p, 1, 4) AS INTEGER),
                TRY_CAST(substr(p, 6, 2) AS INTEGER), 1)
            WHEN 'Q' THEN make_date(
                TRY_CAST(substr(p, 1, 4) AS INTEGER),
                (TRY_CAST(substr(p, 7, 1) AS INTEGER) - 1) * 3 + 1, 1)
            WHEN 'H' THEN make_date(  -- half-year periods are 'YYYY-B1' / 'YYYY-B2'
                TRY_CAST(substr(p, 1, 4) AS INTEGER),
                (TRY_CAST(substr(p, 7, 1) AS INTEGER) - 1) * 6 + 1, 1)
            WHEN 'D' THEN TRY_CAST(p AS DATE)
            ELSE NULL
        END                              AS date,
        p                                AS period,
        freq                             AS frequency,
        pos                              AS series_code,
        pos_title                        AS series_name,
        dim_key                          AS dimensions,
        TRY_CAST(value AS DOUBLE)        AS value,
        unit_text                        AS unit,
        TRY_CAST(unit_mult AS INTEGER)   AS unit_mult
    FROM base
    WHERE value IS NOT NULL
'''

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_SQL.format(dep=s.id),
        # Series identity within a dataset is (pos, dimensions, freq, period);
        # one observation per series per period (see module docstring).
        key=("series_code", "dimensions", "frequency", "period"),
        temporal="date",
    )
    for s in DOWNLOAD_SPECS
]
