"""EUROCONTROL Performance Review Unit — open aviation performance data.

Source: EUROCONTROL Aviation Intelligence Portal (ansperformance.eu), open CSV
performance datasets sourced from the Network Manager repository. Each subset is
one dataset-group published as a single Delta table by unioning the source's
per-calendar-year CSV files.

Fetch shape: stateless full re-pull (shape 1). Each fetch fn discovers the
available years for its group by probing the authoritative download host
(https://www.eurocontrol.int/performance/data/download/csv/<group>_<YYYY>.csv,
or .csv.bz2 for the bzip2-compressed groups) across a generous candidate window
(a fixed lower floor below any real data, up to a *dynamic* ceiling of the
current year): a year is "present" iff its URL returns 200 — 404 means absent.
This is source-driven discovery (the ceiling grows automatically each year), not
a hardcoded data extent. The companion index at ansperformance.eu/csv/ is NOT
used — it is bot-protected and 403s from datacenter IPs.

For each present year the file is downloaded, decompressed if needed, every row
normalized to the group's fixed canonical column set (missing cells -> ""), and
written as one NDJSON batch raw asset `<node_id>-<year>`. The SQL transform globs
`<node_id>-*` and unions all year batches into one table.

No auth, no documented rate limit. Full corpus per refresh; only the current-year
file changes month to month, picked up for free by the full re-pull.
"""
import bz2
import csv
import io
from datetime import datetime, timezone

import httpx
from ratelimit import limits, sleep_and_retry
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_random_exponential,
)

from subsets_utils import NodeSpec, SqlNodeSpec, configure_http, get, is_transient, save_raw_ndjson

DOWNLOAD_BASE = "https://www.eurocontrol.int/performance/data/download/csv"
# Generous floor below any real data (earliest observed file is 2008); the
# ceiling is the current year (+1 slack), so newly-published years are picked up
# automatically. Not a hardcoded data extent — membership is decided by probing.
SOURCE_MIN_YEAR = 2005
# eurocontrol.int's CDN rejects the library's default UA on some paths; present a
# standard browser UA (ASCII-only).
BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

# Entity union (rank-active subsets). Each is a dataset-group = its own table.
ENTITY_IDS = [
    "airport_traffic",
    "all_pre_departure_delays",
    "apt_dly",
    "asma_additional_time",
    "atc_pre_departure_delays",
    "atfm_slot_adherence",
    "co2_emmissions_by_state",
    "ert_dly_ansp",
    "ert_dly_fir",
    "horizontal_flight_efficiency",
    "taxi_in_additional_time",
    "taxi_out_additional_time",
    "vertical_flight_efficiency",
]

# Per-group config. `cols` is the canonical (latest-year, superset) header used
# to normalize every row to a uniform key set so all year batches share one
# schema. `date` selects the date strategy: ("flt"|"entry", <col>) for a daily
# date column, or ("monthly", <month_col>) to synthesize a month-start date.
# `dims` are string dimensions, `text` are free-text columns, `nums` are numeric
# measures (TRY_CAST to DOUBLE in the transform).
_ERT = [
    "FLT_ERT_1", "DLY_ERT_1", "DLY_ERT_A_1", "DLY_ERT_C_1", "DLY_ERT_D_1",
    "DLY_ERT_E_1", "DLY_ERT_G_1", "DLY_ERT_I_1", "DLY_ERT_M_1", "DLY_ERT_N_1",
    "DLY_ERT_O_1", "DLY_ERT_P_1", "DLY_ERT_R_1", "DLY_ERT_S_1", "DLY_ERT_T_1",
    "DLY_ERT_V_1", "DLY_ERT_W_1", "DLY_ERT_NA_1", "FLT_ERT_1_DLY",
    "FLT_ERT_1_DLY_15",
]
_APT_ARR = [
    "FLT_ARR_1", "DLY_APT_ARR_1", "DLY_APT_ARR_A_1", "DLY_APT_ARR_C_1",
    "DLY_APT_ARR_D_1", "DLY_APT_ARR_E_1", "DLY_APT_ARR_G_1", "DLY_APT_ARR_I_1",
    "DLY_APT_ARR_M_1", "DLY_APT_ARR_N_1", "DLY_APT_ARR_O_1", "DLY_APT_ARR_P_1",
    "DLY_APT_ARR_R_1", "DLY_APT_ARR_S_1", "DLY_APT_ARR_T_1", "DLY_APT_ARR_V_1",
    "DLY_APT_ARR_W_1", "DLY_APT_ARR_NA_1", "FLT_ARR_1_DLY", "FLT_ARR_1_DLY_15",
]
_ADD_TIME_NUMS = [
    "TF", "VALID_FL", "NO_REF", "TOTAL_REF_NB_FL", "TOTAL_REF_TIME_MIN",
    "TOTAL_ADD_TIME_MIN",
]
_VERT_NUMS = [
    "NBR_FLIGHTS_DESCENT", "TOT_DIST_LEVEL_NM_DESCENT",
    "TOT_DIST_LVL_NM_DESC_BLW_70", "TOT_TIME_LEVEL_SECONDS_DESCENT",
    "TOT_TIME_LEVEL_SEC_DESC_BLW_70", "MEDIAN_CDO_ALT", "NBR_CDO_FLIGHTS",
    "NBR_CDO_FLIGHTS_BELOW_7000", "TOT_DELTA_CO2_KG_DESCENT",
    "TOT_DELTA_CO2_KG_DESC_BLW_70", "NBR_FLIGHTS_CLIMB",
    "TOT_DIST_LEVEL_NM_CLIMB", "TOT_DIST_LVL_NM_CLIMB_BLW_100",
    "TOT_TIME_LEVEL_SECONDS_CLIMB", "TOT_TIME_LVL_SEC_CLIMB_BLW_100",
    "MEDIAN_CCO_ALT", "NBR_CCO_FLIGHTS", "NBR_CCO_FLIGHTS_BELOW_10000",
    "TOT_DELTA_CO2_KG_CLIMB", "TOT_DELTA_CO2_KG_CLIMB_BLW_100",
]


def _cfg(date, dims, nums, text=(), ext="csv"):
    cols = ["YEAR"]
    if date[0] == "monthly":
        cols.append(date[1])
    else:
        cols += ["MONTH_NUM", "MONTH_MON", date[1]]
    # de-dupe while preserving order, then append dims/text/nums
    seen = set(cols)
    for c in [*dims, *text, *nums]:
        if c not in seen:
            cols.append(c)
            seen.add(c)
    return {"cols": cols, "date": date, "dims": list(dims), "nums": list(nums),
            "text": list(text), "ext": ext}


_APT_DIMS = ["APT_ICAO", "APT_NAME", "STATE_NAME"]
_ENT_DIMS = ["ENTITY_NAME", "ENTITY_TYPE"]

GROUPS = {
    "airport_traffic": _cfg(
        ("flt", "FLT_DATE"), _APT_DIMS,
        ["FLT_DEP_1", "FLT_ARR_1", "FLT_TOT_1", "FLT_DEP_IFR_2", "FLT_ARR_IFR_2", "FLT_TOT_IFR_2"],
    ),
    "all_pre_departure_delays": _cfg(
        ("flt", "FLT_DATE"), _APT_DIMS,
        ["FLT_DEP_1", "FLT_DEP_IFR_2", "DLY_ALL_PRE_2"],
    ),
    "atc_pre_departure_delays": _cfg(
        ("flt", "FLT_DATE"), _APT_DIMS,
        ["FLT_DEP_1", "FLT_DEP_IFR_2", "DLY_ATC_PRE_2", "FLT_DEP_3", "DLY_ATC_PRE_3"],
    ),
    "atfm_slot_adherence": _cfg(
        ("flt", "FLT_DATE"), _APT_DIMS,
        ["FLT_DEP_1", "FLT_DEP_REG_1", "FLT_DEP_OUT_EARLY_1", "FLT_DEP_IN_1", "FLT_DEP_OUT_LATE_1"],
    ),
    "apt_dly": _cfg(
        ("flt", "FLT_DATE"), _APT_DIMS, _APT_ARR, text=["ATFM_VERSION"], ext="csv.bz2",
    ),
    "ert_dly_ansp": _cfg(("flt", "FLT_DATE"), _ENT_DIMS, _ERT, ext="csv.bz2"),
    "ert_dly_fir": _cfg(("flt", "FLT_DATE"), _ENT_DIMS, _ERT, ext="csv.bz2"),
    "horizontal_flight_efficiency": _cfg(
        ("entry", "ENTRY_DATE"), _ENT_DIMS,
        ["DIST_FLOWN_KM", "DIST_DIRECT_KM", "DIST_ACHIEVED_KM"], text=["TYPE_MODEL"],
    ),
    "asma_additional_time": _cfg(("monthly", "MONTH_NUM"), _APT_DIMS, _ADD_TIME_NUMS, text=["MONTH_MON", "COMMENT"]),
    "taxi_in_additional_time": _cfg(("monthly", "MONTH_NUM"), _APT_DIMS, _ADD_TIME_NUMS, text=["MONTH_MON", "COMMENT"]),
    "taxi_out_additional_time": _cfg(("monthly", "MONTH_NUM"), _APT_DIMS, _ADD_TIME_NUMS, text=["MONTH_MON", "COMMENT"]),
    "vertical_flight_efficiency": _cfg(
        ("monthly", "MONTH_NUM"), _APT_DIMS, _VERT_NUMS, text=["MONTH_MON", "AIRPORT_NAME"],
    ),
    "co2_emmissions_by_state": _cfg(
        ("monthly", "MONTH"), ["STATE_NAME", "STATE_CODE"], ["CO2_QTY_TONNES", "TF"], text=["NOTE"],
    ),
}

# Politeness: eurocontrol.int 429s under sustained load, so cap to ~2 req/s per
# process. The DAG runs specs sequentially by default; this keeps the aggregate
# request rate against the shared host well under its (undocumented) limit.
@sleep_and_retry
@limits(calls=2, period=1)
def _rate_limited_get(url: str) -> httpx.Response:
    return get(url, timeout=(10.0, 180.0))


@retry(
    retry=retry_if_exception(is_transient),
    stop=stop_after_attempt(8),
    wait=wait_random_exponential(multiplier=2, max=180),
    reraise=True,
)
def _fetch(url: str) -> httpx.Response:
    resp = _rate_limited_get(url)
    resp.raise_for_status()
    return resp


def _group_of(node_id: str) -> str:
    return node_id[len("eurocontrol-"):].replace("-", "_")


def _try_fetch(url: str) -> httpx.Response | None:
    """Fetch a candidate file URL; return the response, or None on a 404
    (file for that year doesn't exist). Transient errors (incl. 429) are retried
    in _fetch with backoff; other 4xx propagate."""
    try:
        return _fetch(url)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return None
        raise


def fetch_one(node_id: str) -> None:
    configure_http(headers={"User-Agent": BROWSER_UA})
    group = _group_of(node_id)
    cfg = GROUPS[group]
    cols, ext = cfg["cols"], cfg["ext"]
    is_bz2 = ext.endswith(".bz2")
    # Probe DOWNWARD from a dynamic ceiling (current year +1 for early-January
    # releases) to the floor. The annual series is contiguous, so: 404s at the
    # top are future years not yet published (keep going); the first 404 AFTER
    # finding data marks the start of the series (stop). This discovers the exact
    # available range with almost no wasted requests and grows automatically.
    ceiling = datetime.now(timezone.utc).year + 1
    found = 0
    for year in range(ceiling, SOURCE_MIN_YEAR - 1, -1):
        resp = _try_fetch(f"{DOWNLOAD_BASE}/{group}_{year}.{ext}")
        if resp is None:
            if found:
                break  # passed the earliest published year
            continue   # future year, not published yet
        text = bz2.decompress(resp.content) if is_bz2 else resp.content
        # utf-8-sig strips a BOM if present
        reader = csv.DictReader(io.StringIO(text.decode("utf-8-sig", "replace")))
        rows = []
        for r in reader:
            # normalize to the canonical key set; missing -> "" so every batch
            # file shares one (all-string) schema for clean NDJSON union.
            rows.append({c: (r.get(c) or "").strip() for c in cols})
        save_raw_ndjson(rows, f"{node_id}-{year}")
        found += 1
    if found == 0:
        raise AssertionError(
            f"{group}: no yearly files found under {DOWNLOAD_BASE} "
            f"({SOURCE_MIN_YEAR}..{ceiling}, ext={ext}) — URL pattern may have changed"
        )


DOWNLOAD_SPECS = [
    NodeSpec(id=f"eurocontrol-{eid.replace('_', '-')}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]


def _build_sql(dep: str, cfg: dict) -> str:
    date = cfg["date"]
    proj = ['TRY_CAST("YEAR" AS INTEGER) AS year']
    if date[0] == "monthly":
        mc = date[1]
        proj.append(f'TRY_CAST("{mc}" AS INTEGER) AS month')
        proj.append(
            f'make_date(TRY_CAST("YEAR" AS INTEGER), TRY_CAST("{mc}" AS INTEGER), 1) AS date'
        )
    else:
        proj.append('TRY_CAST("MONTH_NUM" AS INTEGER) AS month')
        # CAST to VARCHAR first: DuckDB may infer the raw column as DATE/TIMESTAMP
        # (plain "2024-01-01") or VARCHAR ("2024-01-01T00:00:00Z"); take the first
        # 10 chars of the text form either way.
        proj.append(f'TRY_CAST(left(CAST("{date[1]}" AS VARCHAR), 10) AS DATE) AS date')
    for d in cfg["dims"]:
        proj.append(f'NULLIF("{d}", \'\') AS {d.lower()}')
    for t in cfg["text"]:
        proj.append(f'NULLIF("{t}", \'\') AS {t.lower()}')
    for n in cfg["nums"]:
        proj.append(f'TRY_CAST("{n}" AS DOUBLE) AS {n.lower()}')
    inner = f'SELECT {", ".join(proj)} FROM "{dep}"'
    # outer filter drops footer/blank rows whose date won't parse
    return f"SELECT * FROM ({inner}) WHERE date IS NOT NULL"


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_build_sql(s.id, GROUPS[_group_of(s.id)]),
    )
    for s in DOWNLOAD_SPECS
]
