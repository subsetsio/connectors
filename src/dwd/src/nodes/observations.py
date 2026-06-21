"""DWD per-station observation products — uniform wide ingest.

Per-station observation archives (kl, more_precip, soil_temperature, solar,
water_equiv, weather_phenomena, more_weather_phenomena, climate_indices). Each
(resolution, variable) "product" shares one wide column layout across all its
stations; the station id and the historical/recent period are column values, not
schema splits. One parametric fetcher (`fetch_obs`) drives every product from the
`_OBS_PRODUCTS` table.

Stateless full re-pull every refresh: the server overwrites files in place and
exposes no since/cursor delta, so a stored watermark would only risk skipping the
in-place revisions DWD makes to historical records.
"""

import csv
import io
import zipfile

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, raw_parquet_writer
from utils import OBS, _get_bytes, _list_hrefs

# spec_id -> (resolution, variable). Each product's stations share one wide
# layout; the variable's own column codes (TMK, RSK, ...) become the table's
# measurement columns. date_col is derived from the resolution below.
_OBS_PRODUCTS: list[tuple[str, str]] = [
    ("daily", "kl"),
    ("daily", "more_precip"),
    ("daily", "soil_temperature"),
    ("daily", "solar"),
    ("daily", "water_equiv"),
    ("daily", "weather_phenomena"),
    ("daily", "more_weather_phenomena"),
    ("monthly", "kl"),
    ("monthly", "more_precip"),
    ("monthly", "weather_phenomena"),
    ("monthly", "climate_indices"),
    ("annual", "kl"),
    ("annual", "more_precip"),
    ("annual", "weather_phenomena"),
    ("annual", "climate_indices"),
]


def _obs_spec_id(res: str, var: str) -> str:
    return f"dwd-obs-{res}-{var.replace('_', '-')}"


_OBS_BY_ID = {_obs_spec_id(r, v): (r, v) for r, v in _OBS_PRODUCTS}

# daily archives key on MESS_DATUM; monthly/annual (incl. climate_indices) on
# MESS_DATUM_BEGINN. Both are YYYYMMDD.
_DATE_COL = {"daily": "MESS_DATUM", "monthly": "MESS_DATUM_BEGINN", "annual": "MESS_DATUM_BEGINN"}
# columns excluded from the generic measurement-cast (keys + end-of-record marker)
_KEY_COLS = ("STATIONS_ID", "MESS_DATUM", "MESS_DATUM_BEGINN", "MESS_DATUM_ENDE", "eor")


def _read_produkt(zip_bytes: bytes) -> tuple[list[str], list[list[str]]]:
    """Return (header, rows) of the single produkt_*.txt inside a station ZIP.
    Cells and column names are whitespace-stripped (DWD pads with spaces)."""
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        names = [n for n in zf.namelist() if n.lower().startswith("produkt") and n.lower().endswith(".txt")]
        if not names:
            raise RuntimeError(f"no produkt_*.txt in ZIP (members: {zf.namelist()[:5]})")
        text = zf.read(names[0]).decode("latin-1")
    reader = csv.reader(io.StringIO(text), delimiter=";")
    rows = [[c.strip() for c in r] for r in reader if r]
    if not rows:
        return [], []
    return rows[0], rows[1:]


def _obs_listing_dirs(res: str, var: str) -> list[str]:
    """Directory URLs holding this product's per-station ZIPs."""
    base = f"{OBS}/{res}/{var}"
    if var == "solar":  # flat: tageswerte_ST_<id>_row.zip directly in the product dir
        return [base]
    if var == "climate_indices":  # nested kl/ + precip/ each with historical/recent
        return [f"{base}/{sub}/{per}" for sub in ("kl", "precip") for per in ("historical", "recent")]
    return [f"{base}/{per}" for per in ("historical", "recent")]


def fetch_obs(node_id: str) -> None:
    res, var = _OBS_BY_ID[node_id]  # KeyError-by-design if the spec set drifts

    # 1. enumerate every station ZIP, grouped by listing dir (first ZIP of each
    #    group seeds the header union — climate_indices' kl/precip layouts differ).
    zip_urls: list[str] = []
    group_firsts: list[str] = []
    for d in _obs_listing_dirs(res, var):
        zips = sorted(h for h in _list_hrefs(d + "/") if h.endswith(".zip"))
        if not zips:
            continue
        for h in zips:
            zip_urls.append(f"{d}/{h}")
        group_firsts.append(f"{d}/{zips[0]}")
    if not zip_urls:
        raise RuntimeError(f"{node_id}: no station ZIPs found under {OBS}/{res}/{var}")

    # 2. build the superset (ordered union) header from each group's first ZIP,
    #    caching those parsed payloads so they aren't downloaded twice.
    header: list[str] = []
    seen = set()
    cache: dict[str, tuple[list[str], list[list[str]]]] = {}
    for url in group_firsts:
        h, rows = _read_produkt(_get_bytes(url))
        cache[url] = (h, rows)
        for c in h:
            if c not in seen:
                seen.add(c)
                header.append(c)
    if "STATIONS_ID" not in header or _DATE_COL[res] not in header:
        raise RuntimeError(f"{node_id}: produkt header missing keys; got {header[:6]}")

    schema = pa.schema([(c, pa.string()) for c in header])

    # 3. stream every ZIP into the raw parquet, one batch per station file.
    n_stations = 0
    n_rows = 0
    with raw_parquet_writer(node_id, schema) as w:
        for url in zip_urls:
            h, rows = cache.pop(url) if url in cache else _read_produkt(_get_bytes(url))
            if not h or not rows:
                continue
            idx = {name: i for i, name in enumerate(h)}
            cols = {c: [] for c in header}
            for r in rows:
                for c in header:
                    j = idx.get(c)
                    cols[c].append(r[j] if (j is not None and j < len(r)) else None)
            w.write_table(pa.table({c: pa.array(cols[c], type=pa.string()) for c in header}, schema=schema))
            n_stations += 1
            n_rows += len(rows)
    if n_rows == 0:
        raise RuntimeError(f"{node_id}: parsed 0 rows across {n_stations} station files")


def _obs_transform_sql(node_id: str) -> str:
    res, _ = _OBS_BY_ID[node_id]
    date_col = _DATE_COL[res]
    excl = ", ".join(f"'{c}'" for c in _KEY_COLS)
    # Generic typed projection: station id + parsed date + every measurement
    # column cast to DOUBLE with the -999 sentinel nulled. QN_* quality flags and
    # the key/eor columns are dropped. Historical/recent overlap is de-duplicated.
    return f'''
        SELECT
            CAST(STATIONS_ID AS INTEGER) AS station_id,
            strptime(trim(CAST({date_col} AS VARCHAR)), '%Y%m%d')::DATE AS date,
            nullif(
                TRY_CAST(
                    COLUMNS(c -> c NOT IN ({excl}) AND NOT starts_with(c, 'QN')) AS DOUBLE
                ),
                -999
            )
        FROM "{node_id}"
        WHERE TRY_CAST(STATIONS_ID AS INTEGER) IS NOT NULL
          AND strptime(trim(CAST({date_col} AS VARCHAR)), '%Y%m%d') IS NOT NULL
        QUALIFY row_number() OVER (
            PARTITION BY CAST(STATIONS_ID AS INTEGER),
                         strptime(trim(CAST({date_col} AS VARCHAR)), '%Y%m%d')::DATE
            ORDER BY {date_col}
        ) = 1
    '''


DOWNLOAD_SPECS = [NodeSpec(id=sid, fn=fetch_obs, kind="download") for sid in _OBS_BY_ID]

TRANSFORM_SPECS = [
    SqlNodeSpec(id=f"{sid}-transform", deps=[sid], sql=_obs_transform_sql(sid)) for sid in _OBS_BY_ID
]
