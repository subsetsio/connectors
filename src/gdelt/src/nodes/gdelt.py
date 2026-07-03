"""GDELT 2.0 Events — daily country x event-root x quad-class activity panel.

GDELT publishes the full firehose of CAMEO-coded world news events as one
tab-delimited CSV.zip "export" file per 15-minute interval (~96/day), listed in
masterfilelist.txt, from 2015-02-18 onward. The full row-level corpus is ~600M
rows / ~390k files — too large to publish at row grain, so we AGGREGATE on the
fly: for each complete past UTC day we fetch that day's export files, roll the
events up to (event_day x action-location country x CAMEO event-root x quad class)
with event counts and mention/article/Goldstein/tone measures, and write ONE
small parquet batch per file-date. The published subset `gdelt-events` is the
glob-union of those batches, re-aggregated in SQL into a clean
conflict/cooperation time series. The aggregate is tiny: ~3.5k groups/day x ~4150
days ≈ 14M rows for the whole 11-year history — a few hundred MB of parquet.

DESIGN — stateless full re-pull (NO connector-scoped watermark). This is
deliberate and load-bearing. In this harness raw is *run-scoped*
(`runs/<run_id>/raw/`) while state is *connector-scoped*, and the SQL transform
rebuilds the table with overwrite() from the glob-union of THIS run's raw only.
A shared watermark that skipped file-dates fetched by a *prior* run — whose
batches live in that prior run's raw dir, invisible to this run's transform —
would silently publish a partial table (exactly the failure mode an earlier
watermarked version hit: the backfill split across two run_ids and the published
table covered only the second run's slice). So every run re-fetches the whole
history into its own raw dir and the transform sees all of it. At ~2.7s/file-date
the full backfill is ~11k s of fetch, inside the cloud DAG_TIME_BUDGET (~5.75h),
so a single run materializes the complete table; revisions are picked up for free
because no high-water mark is ever trusted.

Resume is per-run and idempotent, NOT stateful: on a supervisor interrupt ->
continuation (same run_id, same raw dir) the loop skips file-dates whose batch is
already present in this run's raw, so it picks up where it left off without
re-fetching. There is no self-imposed run budget — the loop runs until caught up
to the live edge (yesterday UTC; today's 15-minute files are still accumulating)
and the supervisor caps wall-clock. The cost is that a *fresh* run_id re-fetches
the corpus from scratch; that is the price of a guaranteed-complete table under
run-scoped raw, and it is what makes the connector robust to run fragmentation.

Why event_day (not file-date) is the grain: a 15-minute export file mostly
contains events dated that day, but carries a few late-detected stragglers dated
earlier. Keying the aggregate on each row's event day (and re-summing across
batches in the transform) attributes activity to when it happened; the per-batch
sums are merged by the transform's GROUP BY, so the same (event_day, country,
root, quad) appearing in several file-date batches is summed correctly. Within
the export stream global_event_id is unique (re-mentions live in the separate
mentions feed), so events are never double-counted.

Note on http: the GDELT bulk host data.gdeltproject.org serves these files over
plain HTTP only (its HTTPS endpoint presents an invalid certificate). The codelist
lookups on www.gdeltproject.org are not used here — labels are applied in SQL.
"""
import io
import os
import zipfile
from collections import defaultdict
from datetime import datetime, timezone

import httpx
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    list_raw_fragments,
    transient_retry,
)

# GDELT 2.0 begins 2015-02-18; v1 (1979-2015) uses an incompatible schema/cadence
# and is intentionally excluded.
SOURCE_MIN_DATE = datetime(2015, 2, 18).date()
_SOURCE_MIN_DAY8 = "20150218"  # same bound as YYYYMMDD for lexical event-day filtering

_MASTER_FILE_LIST_URL = "http://data.gdeltproject.org/gdeltv2/masterfilelist.txt"

# Column indices in the fixed 61-field GDELT 2.0 Event layout (tab-delimited, no
# header). Only the handful we aggregate on are named here.
_I_DAY = 1               # event date, YYYYMMDD
_I_EVENT_ROOT = 28       # CAMEO event root code, "01".."20"
_I_QUAD = 29             # quad class, 1..4
_I_GOLDSTEIN = 30        # Goldstein scale, -10..10
_I_NUM_MENTIONS = 31
_I_NUM_ARTICLES = 33
_I_TONE = 34             # average document tone, -100..100
_I_ACTION_FIPS = 53      # action-location country, FIPS 10-4 two-letter code
_N_COLS = 61

_VALID_QUADS = {1, 2, 3, 4}

# FIPS 10-4 (NGA GEC) -> ISO 3166-1 alpha-2. GDELT geo country codes are FIPS, not
# ISO; this static concordance maps them. Non-country / obsolete codes are absent
# (their events fall into the null-country bucket).
_FIPS_TO_ISO2 = {
    "AA": "AW", "AC": "AG", "AE": "AE", "AF": "AF", "AG": "DZ", "AJ": "AZ",
    "AL": "AL", "AM": "AM", "AN": "AD", "AO": "AO", "AQ": "AS", "AR": "AR",
    "AS": "AU", "AT": "AT", "AU": "AT", "AV": "AI", "AY": "AQ", "BA": "BH",
    "BB": "BB", "BC": "BW", "BD": "BM", "BE": "BE", "BF": "BS", "BG": "BD",
    "BH": "BZ", "BK": "BA", "BL": "BO", "BM": "MM", "BN": "BJ", "BO": "BY",
    "BP": "SB", "BR": "BR", "BS": "PM", "BT": "BT", "BU": "BG", "BV": "BV",
    "BX": "BN", "BY": "BI", "CA": "CA", "CB": "KH", "CD": "TD", "CE": "LK",
    "CF": "CG", "CG": "CD", "CH": "CN", "CI": "CL", "CJ": "KY", "CK": "CC",
    "CM": "CM", "CN": "KM", "CO": "CO", "CR": "CR", "CS": "CR", "CT": "CF",
    "CU": "CU", "CV": "CV", "CW": "CK", "CY": "CY", "DA": "DK", "DJ": "DJ",
    "DO": "DM", "DR": "DO", "EC": "EC", "EG": "EG", "EI": "IE", "EK": "GQ",
    "EN": "EE", "ER": "ER", "ES": "SV", "ET": "ET", "EU": "RE", "EZ": "CZ",
    "FI": "FI", "FJ": "FJ", "FK": "FK", "FM": "FM", "FO": "FO", "FP": "PF",
    "FR": "FR", "FS": "TF", "GA": "GM", "GB": "GA", "GG": "GE", "GH": "GH",
    "GI": "GI", "GJ": "GD", "GK": "GG", "GL": "GL", "GM": "DE", "GP": "GP",
    "GQ": "GU", "GR": "GR", "GT": "GT", "GV": "GN", "GY": "GY", "HA": "HT",
    "HK": "HK", "HM": "HM", "HO": "HN", "HR": "HR", "HU": "HU", "IC": "IS",
    "ID": "ID", "IM": "IM", "IN": "IN", "IO": "IO", "IP": "CX", "IR": "IR",
    "IS": "IL", "IT": "IT", "IV": "CI", "IZ": "IQ", "JA": "JP", "JE": "JE",
    "JM": "JM", "JO": "JO", "JQ": "UM", "KE": "KE", "KG": "KG",
    "KN": "KP", "KQ": "UM", "KR": "KI", "KS": "KR", "KT": "CX", "KU": "KW",
    "KV": "XK", "KZ": "KZ", "LA": "LA", "LE": "LB", "LG": "LV", "LH": "LT",
    "LI": "LR", "LO": "SK", "LS": "LI", "LT": "LS", "LU": "LU", "LY": "LY",
    "MA": "MG", "MB": "MQ", "MC": "MO", "MD": "MD", "MF": "YT", "MG": "MN",
    "MH": "MS", "MI": "MW", "MJ": "ME", "MK": "MK", "ML": "ML", "MN": "MC",
    "MO": "MA", "MP": "MU", "MR": "MR", "MT": "MT", "MU": "OM", "MV": "MV",
    "MX": "MX", "MY": "MY", "MZ": "MZ", "NC": "NC", "NE": "NU", "NF": "NF",
    "NG": "NE", "NH": "VU", "NI": "NG", "NL": "NL", "NO": "NO", "NP": "NP",
    "NR": "NR", "NS": "SR", "NU": "NI", "NZ": "NZ", "PA": "PY", "PC": "PN",
    "PE": "PE", "PK": "PK", "PL": "PL", "PM": "PA", "PO": "PT", "PP": "PG",
    "PS": "PW", "PU": "GW", "QA": "QA", "RE": "MU", "RI": "RS", "RM": "MH",
    "RN": "MF", "RO": "RO", "RP": "PH", "RQ": "PR", "RS": "RU", "RW": "RW",
    "SA": "SA", "SB": "PM", "SC": "KN", "SE": "SC", "SF": "ZA", "SG": "SN",
    "SH": "SH", "SI": "SI", "SL": "SL", "SM": "SM", "SN": "SG", "SO": "SO",
    "SP": "ES", "ST": "LC", "SU": "SD", "SV": "SJ", "SW": "SE", "SX": "GS",
    "SY": "SY", "SZ": "CH", "TC": "AE", "TD": "TT", "TH": "TH", "TI": "TJ",
    "TK": "TC", "TL": "TK", "TN": "TO", "TO": "TG", "TP": "ST", "TS": "TN",
    "TT": "TL", "TU": "TR", "TV": "TV", "TW": "TW", "TX": "TM", "TZ": "TZ",
    "UC": "CW", "UG": "UG", "UK": "GB", "UM": "UM", "UP": "UA", "US": "US",
    "UV": "BF", "UY": "UY", "UZ": "UZ", "VC": "VC", "VE": "VE", "VI": "VG",
    "VM": "VN", "VQ": "VI", "VT": "VA", "WA": "NA", "WE": "PS", "WF": "WF",
    "WI": "EH", "WS": "WS", "WZ": "SZ", "YM": "YE", "ZA": "ZM", "ZI": "ZW",
}

_BATCH_SCHEMA = pa.schema([
    ("date", pa.string()),                        # event day, YYYY-MM-DD
    ("action_geo_country_iso2", pa.string()),     # ISO 3166-1 alpha-2, nullable
    ("event_root_code", pa.string()),             # CAMEO root, "01".."20"
    ("quad_class", pa.int8()),                    # 1..4
    ("num_events", pa.int64()),
    ("sum_mentions", pa.int64()),
    ("sum_articles", pa.int64()),
    ("sum_goldstein", pa.float64()),
    ("sum_tone", pa.float64()),
])


@transient_retry()
def _fetch_master_list() -> str:
    resp = get(_MASTER_FILE_LIST_URL, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.text


@transient_retry()
def _fetch_zip(url: str) -> bytes | None:
    """Return the raw zip bytes for one 15-minute export file, or None on 404.

    Individual files are intermittently absent upstream (e.g. the 2025-06-15..
    2025-07-01 source outage); a 404 is skip-and-continue, not fatal."""
    resp = get(url, timeout=(10.0, 180.0))
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.content


def _index_export_urls_by_date(master_text: str) -> dict[str, list[str]]:
    """Parse masterfilelist.txt into {YYYYMMDD: [export_url, ...]}.

    Each line is `<size> <md5> <url>`; we keep only the `.export.` files and key
    them by the YYYYMMDD prefix of the filename. Only posted files appear here,
    so this is the authoritative set (lastupdate.txt can advertise a not-yet-
    posted interval)."""
    by_date: dict[str, list[str]] = defaultdict(list)
    for line in master_text.splitlines():
        parts = line.split()
        if len(parts) < 3:
            continue
        url = parts[2]
        if ".export." not in url:
            continue
        fname = url.rsplit("/", 1)[-1]
        if len(fname) < 8 or not fname[:8].isdigit():
            continue
        by_date[fname[:8]].append(url)
    return by_date


def _aggregate_day(urls: list[str], date8: str) -> dict:
    """Fetch every export file for one file-date and roll its events up to
    (event_day, action-country ISO2, event_root, quad). `date8` is the file-date
    (YYYYMMDD); events whose extracted event day falls outside
    [2015-02-18, date8] are dropped — GDELT dates an event by the action date its
    article reports, so a file routinely carries a few rows dated to historical
    references (pre-2015, even pre-2000) or, from parse noise, the future. Those
    are not contemporaneous detections and would smear the time series, so we keep
    only event days within GDELT 2.0's coverage and no later than the file itself.
    Returns a dict keyed by
    that tuple -> [num_events, sum_mentions, sum_articles, sum_goldstein, sum_tone]."""
    agg: dict[tuple, list] = defaultdict(lambda: [0, 0, 0, 0.0, 0.0])
    for url in urls:
        # A single export file must never abort a multi-day backfill. _fetch_zip
        # already returns None on 404 and retries transient HTTP; here we also
        # skip-and-continue past every OTHER permanent failure mode of one file:
        # a non-404 4xx that survives retries, a connection error that exhausts
        # them, or a truncated/corrupt archive (zipfile.BadZipFile). Across the
        # ~390k-file 2015→now corpus (which includes documented multi-day source
        # outages serving errors, not clean 404s) such a file is expected; losing
        # it costs one 15-minute slice, whereas raising would crash the whole run
        # (exit 1, no continuation) and lose hours of progress. The download
        # health tests still catch wholesale corruption (empty/malformed batches).
        try:
            content = _fetch_zip(url)
            if content is None:
                continue
            with zipfile.ZipFile(io.BytesIO(content)) as zf:
                names = zf.namelist()
                if not names:
                    continue
                text = zf.read(names[0]).decode("utf-8", errors="replace")
        except (httpx.HTTPError, zipfile.BadZipFile, OSError) as exc:
            print(f"    skipping {url.rsplit('/', 1)[-1]}: {type(exc).__name__}: {exc}")
            continue
        for line in text.splitlines():
            if not line:
                continue
            f = line.split("\t")
            if len(f) < _N_COLS:
                continue
            day = f[_I_DAY]
            if len(day) != 8 or not day.isdigit():
                continue
            # Drop event days outside GDELT 2.0 coverage or later than this file
            # (historical article references / future-dated parse noise). YYYYMMDD
            # strings compare lexically == chronologically.
            if day < _SOURCE_MIN_DAY8 or day > date8:
                continue
            try:
                quad = int(f[_I_QUAD])
            except ValueError:
                continue
            if quad not in _VALID_QUADS:
                continue
            root = f[_I_EVENT_ROOT]
            if not root:
                continue
            iso2 = _FIPS_TO_ISO2.get(f[_I_ACTION_FIPS]) if f[_I_ACTION_FIPS] else None
            try:
                mentions = int(f[_I_NUM_MENTIONS] or 0)
            except ValueError:
                mentions = 0
            try:
                articles = int(f[_I_NUM_ARTICLES] or 0)
            except ValueError:
                articles = 0
            try:
                goldstein = float(f[_I_GOLDSTEIN] or 0.0)
            except ValueError:
                goldstein = 0.0
            try:
                tone = float(f[_I_TONE] or 0.0)
            except ValueError:
                tone = 0.0
            date_iso = f"{day[:4]}-{day[4:6]}-{day[6:8]}"
            cell = agg[(date_iso, iso2, root, quad)]
            cell[0] += 1
            cell[1] += mentions
            cell[2] += articles
            cell[3] += goldstein
            cell[4] += tone
    return agg


def _build_batch(agg: dict) -> "pa.Table":
    """Materialize one file-date's aggregate dict into a _BATCH_SCHEMA table
    (0 rows if the dict is empty — a valid, skippable batch)."""
    rows = {
        "date": [], "action_geo_country_iso2": [], "event_root_code": [],
        "quad_class": [], "num_events": [], "sum_mentions": [],
        "sum_articles": [], "sum_goldstein": [], "sum_tone": [],
    }
    for (d, iso2, root, quad), (n, m, a, g, t) in agg.items():
        rows["date"].append(d)
        rows["action_geo_country_iso2"].append(iso2)
        rows["event_root_code"].append(root)
        rows["quad_class"].append(quad)
        rows["num_events"].append(n)
        rows["sum_mentions"].append(m)
        rows["sum_articles"].append(a)
        rows["sum_goldstein"].append(g)
        rows["sum_tone"].append(t)
    return pa.table(rows, schema=_BATCH_SCHEMA)


def fetch_events(node_id: str) -> None:
    """Stateless full re-pull (see module docstring). Re-materialize every
    complete GDELT file-date from 2015-02-18 to yesterday UTC as one parquet
    fragment each, skipping fragments this run already COMMITTED to the raw
    manifest so a continuation resumes cheaply. No watermark, no run budget."""
    today_utc = datetime.now(tz=timezone.utc).date()

    # File-dates already committed in THIS run: each completed leg commits its
    # fragments (stamped with our RUN_ID), so the set is empty on a fresh
    # run_id and grows as the backfill progresses. The commit log — never a
    # directory listing: a failed leg's uncommitted batches must re-fetch or
    # the manifest-first transform would silently miss those dates.
    run_id = os.environ.get("RUN_ID", "unknown")
    done = {frag for frag, meta in list_raw_fragments(node_id, "parquet").items()
            if meta.get("run_id") == run_id}

    print("  fetching master file list...")
    by_date = _index_export_urls_by_date(_fetch_master_list())

    # Only COMPLETE past days (never today), in order, minus what's already done.
    pending = sorted(
        d for d in by_date
        if SOURCE_MIN_DATE <= datetime.strptime(d, "%Y%m%d").date() < today_utc
        and f"{d[:4]}-{d[4:6]}-{d[6:8]}" not in done
    )
    if not pending:
        print(f"  nothing to fetch ({len(done)} batches already present, caught up to {today_utc})")
        return
    print(f"  {len(pending)} file-dates to fetch: {pending[0]} .. {pending[-1]} ({len(done)} already done)")

    for date8 in pending:
        # No self-imposed cap: loop until caught up. The supervisor interrupts the
        # node if the run nears its CI budget; the per-date raw write below (an
        # interrupt loses at most the in-flight date) makes resume safe — the
        # `done` set rebuilt next continuation skips every batch already written.
        agg = _aggregate_day(by_date[date8], date8)
        date_iso = f"{date8[:4]}-{date8[4:6]}-{date8[6:8]}"
        table = _build_batch(agg)
        # Always write a batch — a 0-row batch (all files missing/404 for the day)
        # still marks the date done so a continuation doesn't re-fetch the gap, and
        # is harmless to the transform's union/GROUP BY. The file-date is the
        # fragment key of the one raw asset (object name: <node_id>-<date>.parquet).
        save_raw_parquet(table, node_id, fragment=date_iso)
        if table.num_rows:
            print(f"  {date_iso}: {sum(agg[k][0] for k in agg):,} events -> {table.num_rows:,} groups")
        else:
            print(f"  {date_iso}: no events (all files missing) — empty batch")


DOWNLOAD_SPECS = [
    NodeSpec(
        id="gdelt-events",
        fn=fetch_events,
        kind="download",
    ),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="gdelt-events-transform",
        deps=["gdelt-events"],
        sql='''
            WITH rolled AS (
                SELECT
                    CAST(date AS DATE)                  AS date,
                    action_geo_country_iso2,
                    event_root_code,
                    CAST(quad_class AS TINYINT)         AS quad_class,
                    SUM(CAST(num_events AS BIGINT))     AS num_events,
                    SUM(CAST(sum_mentions AS BIGINT))   AS sum_mentions,
                    SUM(CAST(sum_articles AS BIGINT))   AS sum_articles,
                    SUM(CAST(sum_goldstein AS DOUBLE))  AS tot_goldstein,
                    SUM(CAST(sum_tone AS DOUBLE))       AS tot_tone
                FROM "gdelt-events"
                GROUP BY 1, 2, 3, 4
            )
            SELECT
                date,
                action_geo_country_iso2,
                event_root_code,
                CASE event_root_code
                    WHEN '01' THEN 'Make Public Statement'
                    WHEN '02' THEN 'Appeal'
                    WHEN '03' THEN 'Express Intent to Cooperate'
                    WHEN '04' THEN 'Consult'
                    WHEN '05' THEN 'Engage in Diplomatic Cooperation'
                    WHEN '06' THEN 'Engage in Material Cooperation'
                    WHEN '07' THEN 'Provide Aid'
                    WHEN '08' THEN 'Yield'
                    WHEN '09' THEN 'Investigate'
                    WHEN '10' THEN 'Demand'
                    WHEN '11' THEN 'Disapprove'
                    WHEN '12' THEN 'Reject'
                    WHEN '13' THEN 'Threaten'
                    WHEN '14' THEN 'Protest'
                    WHEN '15' THEN 'Exhibit Force Posture'
                    WHEN '16' THEN 'Reduce Relations'
                    WHEN '17' THEN 'Coerce'
                    WHEN '18' THEN 'Assault'
                    WHEN '19' THEN 'Fight'
                    WHEN '20' THEN 'Engage in Unconventional Mass Violence'
                    ELSE NULL
                END                                     AS event_root_label,
                quad_class,
                CASE quad_class
                    WHEN 1 THEN 'Verbal Cooperation'
                    WHEN 2 THEN 'Material Cooperation'
                    WHEN 3 THEN 'Verbal Conflict'
                    WHEN 4 THEN 'Material Conflict'
                END                                     AS quad_class_label,
                num_events,
                sum_mentions,
                sum_articles,
                tot_goldstein / num_events              AS avg_goldstein,
                tot_tone / num_events                   AS avg_tone
            FROM rolled
            WHERE num_events > 0
        ''',
        key=("date", "action_geo_country_iso2", "event_root_code", "quad_class"),
        temporal="date",
    ),
]
