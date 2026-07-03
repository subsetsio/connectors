"""SILSO — Sunspot Index and Long-term Solar Observations (Royal Observatory of
Belgium, WDC-SILSO). Publishes the International Sunspot Number (V2.0) as a small
fixed set of time series, one CSV per series at a persistent URL.

Fetch shape: stateless full re-pull. Every file IS its complete bulk export at a
stable URL (largest is the daily total at ~76k rows, <2MB); there is no
incremental query, so we simply re-fetch each series in full every run and
overwrite. No auth, no pagination, no rate limit observed.

Endpoint choice: we read the static pre-generated DATA/*.txt files rather than
the INFO/*csv.php endpoints. The .php endpoints generate the CSV server-side and
proved unreliable from cloud runners for the large daily file (TLS handshake
timeouts / connection resets); the static .txt files are served directly and are
robust. They carry the identical V2.0 columns but are whitespace-separated and
encode the definitive/provisional flag as a trailing '*' marker (present =
provisional) instead of a 0/1 column.

Raw format: each series is parsed into a typed parquet with an explicit schema —
the files are headerless and encode missing values as the sentinel -1 / -1.0, so
a typed-parquet pass (rather than handing the raw text to DuckDB) is the safe
contract. The transform SQL then NULLIFs the sentinels and projects a tidy table
per subset.
"""
import httpx
import pyarrow as pa
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet

_BASE = "https://www.sidc.be/SILSO/DATA"

# The numeric columns of each .txt file, in order: name + kind ('i' = int64,
# 'f' = float64). The trailing definitive/provisional marker ('*' = provisional)
# is NOT a column here — _parse derives a `definitive` (1/0) column from it.
# Verified live against the static V2.0 files.
_TOT_DAILY = [
    ("year", "i"), ("month", "i"), ("day", "i"), ("decimal_date", "f"),
    ("sunspot_number", "f"), ("std_dev", "f"), ("n_observations", "i"),
]
_TOT_MONTHLY = [
    ("year", "i"), ("month", "i"), ("decimal_date", "f"),
    ("sunspot_number", "f"), ("std_dev", "f"), ("n_observations", "i"),
]
_TOT_MONTHLY_SMOOTHED = [
    ("year", "i"), ("month", "i"), ("decimal_date", "f"),
    ("smoothed_sunspot_number", "f"), ("std_dev", "f"), ("n_observations", "i"),
]
_TOT_YEARLY = [
    ("year_mid", "f"), ("sunspot_number", "f"), ("std_dev", "f"),
    ("n_observations", "i"),
]
_HEM_DAILY = [
    ("year", "i"), ("month", "i"), ("day", "i"), ("decimal_date", "f"),
    ("sn_total", "f"), ("sn_north", "f"), ("sn_south", "f"),
    ("std_total", "f"), ("std_north", "f"), ("std_south", "f"),
    ("n_obs_total", "i"), ("n_obs_north", "i"), ("n_obs_south", "i"),
]
_HEM_MONTHLY = [
    ("year", "i"), ("month", "i"), ("decimal_date", "f"),
    ("sn_total", "f"), ("sn_north", "f"), ("sn_south", "f"),
    ("std_total", "f"), ("std_north", "f"), ("std_south", "f"),
    ("n_obs_total", "i"), ("n_obs_north", "i"), ("n_obs_south", "i"),
]
_HEM_MONTHLY_SMOOTHED = [
    ("year", "i"), ("month", "i"), ("decimal_date", "f"),
    ("smoothed_sn_total", "f"), ("smoothed_sn_north", "f"), ("smoothed_sn_south", "f"),
    ("std_total", "f"), ("std_north", "f"), ("std_south", "f"),
    ("n_obs_total", "i"), ("n_obs_north", "i"), ("n_obs_south", "i"),
]

# entity id (matches the entity union) -> (url, numeric column spec)
SERIES = {
    "daily-total":                  (f"{_BASE}/SN_d_tot_V2.0.txt",  _TOT_DAILY),
    "monthly-total":                (f"{_BASE}/SN_m_tot_V2.0.txt",  _TOT_MONTHLY),
    "monthly-smoothed-total":       (f"{_BASE}/SN_ms_tot_V2.0.txt", _TOT_MONTHLY_SMOOTHED),
    "yearly-total":                 (f"{_BASE}/SN_y_tot_V2.0.txt",  _TOT_YEARLY),
    "daily-hemispheric":            (f"{_BASE}/SN_d_hem_V2.0.txt",  _HEM_DAILY),
    "monthly-hemispheric":          (f"{_BASE}/SN_m_hem_V2.0.txt",  _HEM_MONTHLY),
    "monthly-smoothed-hemispheric": (f"{_BASE}/SN_ms_hem_V2.0.txt", _HEM_MONTHLY_SMOOTHED),
}


def _is_transient(exc: BaseException) -> bool:
    # httpx.TransportError is the base for ConnectError/ReadError/WriteError and
    # all the timeout/protocol variants; OSError covers raw "connection reset by
    # peer" (errno 104) surfaced from the socket layer. This host is flaky for
    # large transfers, so treat the whole transport/connection family as transient.
    if isinstance(exc, (httpx.TransportError, ConnectionError, OSError)):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        code = exc.response.status_code
        return code == 429 or 500 <= code < 600
    return False


_CHUNK = 256 * 1024  # bytes per Range request

# sidc.be sits behind a WAF that resets connections lacking browser-like
# headers (every request from cloud-runner IPs got RST with the default
# client UA, while a browser UA is served normally). Send a realistic browser
# header set. ASCII-only (httpx rejects non-ASCII header values).
_BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/plain,text/html,application/xhtml+xml,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.sidc.be/SILSO/datafiles",
}


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(8),
    wait=wait_exponential(min=4, max=120),
    reraise=True,
)
def _http_get(url: str, extra_headers: dict) -> httpx.Response:
    # Generous connect timeout: sidc.be can be slow to complete a TLS handshake
    # from cloud runners. Each call is one small Range chunk, retried on any
    # transport error (this host resets long transfers from cloud IPs).
    resp = get(url, headers={**_BROWSER_HEADERS, **extra_headers}, timeout=(30.0, 180.0))
    resp.raise_for_status()
    return resp


def _fetch_text(url: str) -> str:
    # Chunked, Range-based download. sidc.be resets a single long-lived transfer
    # of the large files from cloud runners, but happily serves small byte
    # ranges (Accept-Ranges: bytes, verified) — so we pull the file in small
    # chunks, each independently retried. Accept-Encoding: identity is required
    # for the server to honour Range (it ignores Range when it gzips).
    first = _http_get(url, {"Accept-Encoding": "identity", "Range": f"bytes=0-{_CHUNK - 1}"})
    if first.status_code == 200:
        # Server ignored Range and sent the whole body in one shot.
        return first.content.decode("utf-8")
    # 206 Partial Content: total size is the tail of "bytes <lo>-<hi>/<total>".
    total = int(first.headers["Content-Range"].split("/")[-1])
    buf = bytearray(first.content)
    while len(buf) < total:
        lo = len(buf)
        hi = min(lo + _CHUNK, total) - 1
        chunk = _http_get(url, {"Accept-Encoding": "identity", "Range": f"bytes={lo}-{hi}"})
        buf += chunk.content
    if len(buf) != total:
        raise ValueError(f"size mismatch for {url}: got {len(buf)}, expected {total}")
    return buf.decode("utf-8")


def _parse(text: str, columns: list[tuple[str, str]]) -> pa.Table:
    n = len(columns)
    cols: dict[str, list] = {name: [] for name, _ in columns}
    definitive: list[int] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()  # whitespace-separated, variable spacing
        # A trailing '*' marks a provisional value; its absence = definitive.
        if len(parts) == n:
            is_def = 1
        elif len(parts) == n + 1 and parts[-1] == "*":
            is_def = 0
            parts = parts[:n]
        else:
            raise ValueError(f"expected {n} (+ optional '*') fields, got {len(parts)}: {line!r}")
        for (name, kind), raw in zip(columns, parts):
            cols[name].append(int(raw) if kind == "i" else float(raw))
        definitive.append(is_def)
    fields = [pa.field(name, pa.int64() if kind == "i" else pa.float64()) for name, kind in columns]
    fields.append(pa.field("definitive", pa.int64()))
    data = {name: cols[name] for name, _ in columns}
    data["definitive"] = definitive
    return pa.table(data, schema=pa.schema(fields))


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity = node_id[len("silso-"):]
    url, columns = SERIES[entity]
    table = _parse(_fetch_text(url), columns)
    if table.num_rows == 0:
        raise ValueError(f"{node_id}: parsed 0 rows from {url}")
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"silso-{eid}", fn=fetch_one, kind="download")
    for eid in SERIES
]

# One published Delta table per subset. Sentinel -1/-1.0 -> NULL; rows are kept
# only where the primary value is a real observation. `definitive` is the V2.0
# data-quality flag (1 = definitive value, 0 = provisional/recent).
_TRANSFORM_SQL = {
    "silso-daily-total": '''
        SELECT
            make_date(year, month, day)        AS date,
            NULLIF(sunspot_number, -1)         AS sunspot_number,
            NULLIF(std_dev, -1)                AS std_dev,
            NULLIF(n_observations, -1)         AS n_observations,
            definitive = 1                     AS definitive
        FROM "silso-daily-total"
        WHERE NULLIF(sunspot_number, -1) IS NOT NULL
    ''',
    "silso-monthly-total": '''
        SELECT
            make_date(year, month, 1)          AS date,
            NULLIF(sunspot_number, -1)         AS sunspot_number,
            NULLIF(std_dev, -1)                AS std_dev,
            NULLIF(n_observations, -1)         AS n_observations,
            definitive = 1                     AS definitive
        FROM "silso-monthly-total"
        WHERE NULLIF(sunspot_number, -1) IS NOT NULL
    ''',
    "silso-monthly-smoothed-total": '''
        SELECT
            make_date(year, month, 1)              AS date,
            NULLIF(smoothed_sunspot_number, -1)    AS smoothed_sunspot_number,
            NULLIF(std_dev, -1)                    AS std_dev,
            NULLIF(n_observations, -1)             AS n_observations,
            definitive = 1                         AS definitive
        FROM "silso-monthly-smoothed-total"
        WHERE NULLIF(smoothed_sunspot_number, -1) IS NOT NULL
    ''',
    "silso-yearly-total": '''
        SELECT
            CAST(year_mid AS INTEGER)          AS year,
            year_mid,
            NULLIF(sunspot_number, -1)         AS sunspot_number,
            NULLIF(std_dev, -1)                AS std_dev,
            NULLIF(n_observations, -1)         AS n_observations,
            definitive = 1                     AS definitive
        FROM "silso-yearly-total"
        WHERE NULLIF(sunspot_number, -1) IS NOT NULL
    ''',
    "silso-daily-hemispheric": '''
        SELECT
            make_date(year, month, day)        AS date,
            NULLIF(sn_total, -1)               AS sn_total,
            NULLIF(sn_north, -1)               AS sn_north,
            NULLIF(sn_south, -1)               AS sn_south,
            NULLIF(std_total, -1)              AS std_total,
            NULLIF(std_north, -1)              AS std_north,
            NULLIF(std_south, -1)              AS std_south,
            NULLIF(n_obs_total, -1)            AS n_obs_total,
            NULLIF(n_obs_north, -1)            AS n_obs_north,
            NULLIF(n_obs_south, -1)            AS n_obs_south,
            definitive = 1                     AS definitive
        FROM "silso-daily-hemispheric"
        WHERE NULLIF(sn_total, -1) IS NOT NULL
    ''',
    "silso-monthly-hemispheric": '''
        SELECT
            make_date(year, month, 1)          AS date,
            NULLIF(sn_total, -1)               AS sn_total,
            NULLIF(sn_north, -1)               AS sn_north,
            NULLIF(sn_south, -1)               AS sn_south,
            NULLIF(std_total, -1)              AS std_total,
            NULLIF(std_north, -1)              AS std_north,
            NULLIF(std_south, -1)              AS std_south,
            NULLIF(n_obs_total, -1)            AS n_obs_total,
            NULLIF(n_obs_north, -1)            AS n_obs_north,
            NULLIF(n_obs_south, -1)            AS n_obs_south,
            definitive = 1                     AS definitive
        FROM "silso-monthly-hemispheric"
        WHERE NULLIF(sn_total, -1) IS NOT NULL
    ''',
    "silso-monthly-smoothed-hemispheric": '''
        SELECT
            make_date(year, month, 1)              AS date,
            NULLIF(smoothed_sn_total, -1)          AS smoothed_sn_total,
            NULLIF(smoothed_sn_north, -1)          AS smoothed_sn_north,
            NULLIF(smoothed_sn_south, -1)          AS smoothed_sn_south,
            NULLIF(std_total, -1)                  AS std_total,
            NULLIF(std_north, -1)                  AS std_north,
            NULLIF(std_south, -1)                  AS std_south,
            NULLIF(n_obs_total, -1)                AS n_obs_total,
            NULLIF(n_obs_north, -1)                AS n_obs_north,
            NULLIF(n_obs_south, -1)                AS n_obs_south,
            definitive = 1                         AS definitive
        FROM "silso-monthly-smoothed-hemispheric"
        WHERE NULLIF(smoothed_sn_total, -1) IS NOT NULL
    ''',
}

# Each subset is one observation per period: the date-indexed series are keyed by
# `date` (unique per row), the yearly series by `year`. All are temporal on that
# same period column.
_GRAIN = {
    "silso-daily-total": (("date",), "date"),
    "silso-monthly-total": (("date",), "date"),
    "silso-monthly-smoothed-total": (("date",), "date"),
    "silso-yearly-total": (("year",), "year"),
    "silso-daily-hemispheric": (("date",), "date"),
    "silso-monthly-hemispheric": (("date",), "date"),
    "silso-monthly-smoothed-hemispheric": (("date",), "date"),
}

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        key=_GRAIN[s.id][0],
        temporal=_GRAIN[s.id][1],
        sql=_TRANSFORM_SQL[s.id],
    )
    for s in DOWNLOAD_SPECS
]
