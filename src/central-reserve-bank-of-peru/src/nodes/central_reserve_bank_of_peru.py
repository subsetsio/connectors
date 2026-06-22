"""Central Reserve Bank of Peru (BCRP / BCRPData) — single node module.

The whole source is one REST surface (estadisticas.bcrp.gob.pe) plus its
metadata catalog. Three subsets, modelled per the time-series rule:

  - series  — the per-series reference catalog (code, name, category, group,
              frequency, unit, dates). Derived entirely from the metadata file
              (one semicolon-delimited row per series). Stateless full pull.
  - groups  — the (category, group) taxonomy with series counts, also derived
              from the metadata file. Stateless full pull.
  - values  — long-format observations across every series. The data API has no
              bulk endpoint and no usable column->code mapping when several
              codes are batched (the response order is independent of the
              request order and series carry no code), so each series' full
              history is pulled one code at a time and reshaped to
              (series_code, frequency, date, value). With ~17k series this is a
              code-bucketed firehose: raw is written in code-index batches and
              the resume point is derived from the raw already present in THIS
              run's scope (fresh run -> empty scope -> full re-pull, which is how
              revisions are picked up; continuation -> resume after the last
              batch). The API has no incremental/since filter, so a stateless
              full re-pull is the only option; the firehose batching just makes
              that pull resumable.

The data API intermittently answers a valid request with an empty HTML page
(HTTP 200, non-JSON) instead of the data — observed to be transient (the same
request succeeds on retry), so it is classified retryable alongside the usual
network/5xx/429 errors.
"""
from datetime import datetime, timezone
import csv
import io
import re

import httpx
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    is_transient,
    list_raw_files,
    save_raw_ndjson,
    save_state,
)

SLUG = "central-reserve-bank-of-peru"
STATE_VERSION = 1

API_BASE = "https://estadisticas.bcrp.gob.pe/estadisticas/series/api"
METADATA_URL = "https://estadisticas.bcrp.gob.pe/estadisticas/series/metadata"

# Flush a values batch after this many codes or rows, whichever comes first.
VALUES_BATCH_CODES = 500
VALUES_BATCH_ROWS = 200_000

# metadata column positions (semicolon-delimited, latin-1)
_C_CODE, _C_CATEGORY, _C_GROUP, _C_NAME = 0, 1, 2, 3
_C_UNIT, _C_SCALE, _C_GEO, _C_SOURCE = 6, 7, 8, 9
_C_FREQ, _C_CREATED, _C_PUBGROUP, _C_AREA = 10, 11, 12, 13
_C_UPDATED, _C_START, _C_END = 14, 15, 16

# Spanish month abbreviations used in BCRP period labels (Set = September, PE).
_MONTHS = {
    "Ene": 1, "Feb": 2, "Mar": 3, "Abr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Ago": 8, "Set": 9, "Sep": 9, "Oct": 10, "Nov": 11, "Dic": 12,
}

_YEAR_RE = re.compile(r"(\d{4})")
_BATCH_RE = re.compile(r"-(\d{6})-(\d{6})\.ndjson\.zst$")


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------

class _FlakyEmptyResponse(Exception):
    """A 200 response whose body is the BCRP empty-HTML page, not JSON."""


def _retryable(exc: BaseException) -> bool:
    return is_transient(exc) or isinstance(exc, _FlakyEmptyResponse)


@retry(
    retry=retry_if_exception(_retryable),
    stop=stop_after_attempt(6),
    wait=wait_exponential(min=4, max=120),
    reraise=True,
)
def _get_series_json(url: str) -> dict:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    try:
        return resp.json()
    except ValueError:
        # Transient empty-HTML reject page; reraise as retryable.
        raise _FlakyEmptyResponse(url)


@retry(
    retry=retry_if_exception(is_transient),
    stop=stop_after_attempt(6),
    wait=wait_exponential(min=4, max=120),
    reraise=True,
)
def _get_metadata_text() -> str:
    resp = get(METADATA_URL, timeout=(10.0, 300.0))
    resp.raise_for_status()
    # Served with an Excel content-type but is plain latin-1 delimited text.
    return resp.content.decode("latin-1")


# ---------------------------------------------------------------------------
# Metadata catalog
# ---------------------------------------------------------------------------

def _metadata_rows() -> list[list[str]]:
    text = _get_metadata_text()
    reader = csv.reader(io.StringIO(text), delimiter=";")
    next(reader)  # header
    return [r for r in reader if r and len(r) > _C_END and r[_C_CODE].strip()]


def _cell(row: list[str], idx: int) -> str:
    return row[idx].strip() if len(row) > idx else ""


# ---------------------------------------------------------------------------
# series — per-series reference catalog
# ---------------------------------------------------------------------------

def fetch_series(node_id: str) -> None:
    rows = []
    for r in _metadata_rows():
        rows.append({
            "series_code": _cell(r, _C_CODE),
            "name": _cell(r, _C_NAME),
            "category": _cell(r, _C_CATEGORY),
            "group": _cell(r, _C_GROUP),
            "frequency": _cell(r, _C_FREQ),
            "unit": _cell(r, _C_UNIT),
            "scale": _cell(r, _C_SCALE),
            "geography": _cell(r, _C_GEO),
            "source": _cell(r, _C_SOURCE),
            "publication_group": _cell(r, _C_PUBGROUP),
            "publishing_area": _cell(r, _C_AREA),
            "created": _cell(r, _C_CREATED),
            "updated": _cell(r, _C_UPDATED),
            "start_period": _cell(r, _C_START),
            "end_period": _cell(r, _C_END),
        })
    save_raw_ndjson(rows, node_id)


# ---------------------------------------------------------------------------
# groups — (category, group) taxonomy
# ---------------------------------------------------------------------------

def fetch_groups(node_id: str) -> None:
    agg: dict[tuple[str, str], dict] = {}
    for r in _metadata_rows():
        cat = _cell(r, _C_CATEGORY)
        grp = _cell(r, _C_GROUP)
        if not cat and not grp:
            continue
        key = (cat, grp)
        bucket = agg.setdefault(key, {"category": cat, "group": grp, "series_count": 0, "_freqs": set()})
        bucket["series_count"] += 1
        f = _cell(r, _C_FREQ)
        if f:
            bucket["_freqs"].add(f)
    rows = []
    for b in agg.values():
        rows.append({
            "category": b["category"],
            "group": b["group"],
            "series_count": b["series_count"],
            "frequencies": ", ".join(sorted(b["_freqs"])),
        })
    save_raw_ndjson(rows, node_id)


# ---------------------------------------------------------------------------
# values — long-format observations (code-bucketed firehose)
# ---------------------------------------------------------------------------

def _two_digit_year(yy: int) -> int:
    """Resolve a 2-digit year against a pivot at the current 2-digit year."""
    pivot = datetime.now(tz=timezone.utc).year % 100
    return 2000 + yy if yy <= pivot else 1900 + yy


def _period_to_iso(label: str, freq: str) -> str | None:
    """Normalise a BCRP period label to an ISO date (period start). None if
    unparseable."""
    try:
        if freq == "Diaria":  # "10.Feb.26"
            d, mon, yy = label.split(".")
            return f"{_two_digit_year(int(yy)):04d}-{_MONTHS[mon]:02d}-{int(d):02d}"
        if freq == "Mensual":  # "Ene.2024"
            mon, yyyy = label.split(".")
            return f"{int(yyyy):04d}-{_MONTHS[mon]:02d}-01"
        if freq == "Trimestral":  # "T1.00"
            q = int(label[1])
            yy = int(label.split(".")[1])
            return f"{_two_digit_year(yy):04d}-{(q - 1) * 3 + 1:02d}-01"
        if freq == "Anual":  # "2024"
            return f"{int(label):04d}-01-01"
    except (ValueError, KeyError, IndexError):
        return None
    return None


def _parse_value(raw) -> float | None:
    if raw is None:
        return None
    s = str(raw).strip()
    if not s or s.lower() in ("n.d.", "nd", "n.a.", "na"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _series_window(freq: str, start_field: str) -> tuple[str, str]:
    """Build (start, end) period params for the API from the series' own start
    year (keeps windows tight; an over-wide window is more likely to hit the
    flaky empty-page response)."""
    now_year = datetime.now(tz=timezone.utc).year
    end_year = now_year + 1
    m = _YEAR_RE.search(start_field or "")
    start_year = int(m.group(1)) if m else 1900
    if freq == "Diaria":
        return f"{start_year}-1-1", f"{end_year}-12-31"
    if freq == "Mensual":
        return f"{start_year}-1", f"{end_year}-12"
    if freq == "Trimestral":
        return f"{start_year}-1", f"{end_year}-4"
    # Anual
    return f"{start_year}", f"{end_year}"


def _fetch_series_observations(code: str, freq: str, start_field: str) -> list[dict]:
    start, end = _series_window(freq, start_field)
    # Spanish (default) period labels — "Ene.2024" / "10.Feb.26" / "T1.00" —
    # are what _period_to_iso parses; the English (ing) labels use "Jan"/"Q1".
    url = f"{API_BASE}/{code}/json/{start}/{end}"
    try:
        payload = _get_series_json(url)
    except (httpx.HTTPError, _FlakyEmptyResponse) as exc:
        print(f"skip {code}: {type(exc).__name__} {exc}")
        return []
    out = []
    for period in payload.get("periods", []):
        label = period.get("name", "")
        vals = period.get("values") or []
        value = _parse_value(vals[0]) if vals else None
        iso = _period_to_iso(label, freq)
        out.append({
            "series_code": code,
            "frequency": freq,
            "period": label,
            "date": iso,
            "value": value,
        })
    return out


def fetch_values(node_id: str) -> None:
    # Resume index = highest code-index already covered by raw in THIS run scope.
    done = 0
    for rel in list_raw_files(f"{node_id}-*.ndjson.zst"):
        m = _BATCH_RE.search(rel)
        if m:
            done = max(done, int(m.group(2)))

    series = [
        (_cell(r, _C_CODE), _cell(r, _C_FREQ), _cell(r, _C_START))
        for r in _metadata_rows()
    ]
    series.sort(key=lambda s: s[0])
    todo = series[done:]

    def _checkpoint(n: int) -> None:
        save_state(node_id, {
            "schema_version": STATE_VERSION,
            "completed": n,
            "total": len(series),
            "last_success_at": datetime.now(tz=timezone.utc).isoformat(),
        })

    batch: list[dict] = []
    batch_start = done
    processed = 0
    for code, freq, start_field in todo:
        batch.extend(_fetch_series_observations(code, freq, start_field))
        processed += 1
        if processed % VALUES_BATCH_CODES == 0 or len(batch) >= VALUES_BATCH_ROWS:
            if batch:
                save_raw_ndjson(batch, f"{node_id}-{batch_start:06d}-{done + processed:06d}")
                batch = []
                batch_start = done + processed
            _checkpoint(done + processed)
    if batch:
        save_raw_ndjson(batch, f"{node_id}-{batch_start:06d}-{done + processed:06d}")
    _checkpoint(done + processed)


# ---------------------------------------------------------------------------
# Specs
# ---------------------------------------------------------------------------

DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-series", fn=fetch_series, kind="download"),
    NodeSpec(id=f"{SLUG}-groups", fn=fetch_groups, kind="download"),
    NodeSpec(id=f"{SLUG}-values", fn=fetch_values, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{SLUG}-series-transform",
        deps=[f"{SLUG}-series"],
        sql=f'''
            SELECT
                series_code,
                name,
                category,
                "group",
                frequency,
                unit,
                scale,
                geography,
                source,
                publication_group,
                publishing_area,
                start_period,
                end_period
            FROM "{SLUG}-series"
            WHERE series_code IS NOT NULL AND series_code <> ''
        ''',
    ),
    SqlNodeSpec(
        id=f"{SLUG}-groups-transform",
        deps=[f"{SLUG}-groups"],
        sql=f'''
            SELECT
                category,
                "group",
                CAST(series_count AS BIGINT) AS series_count,
                frequencies
            FROM "{SLUG}-groups"
            WHERE "group" IS NOT NULL AND "group" <> ''
        ''',
    ),
    SqlNodeSpec(
        id=f"{SLUG}-values-transform",
        deps=[f"{SLUG}-values"],
        sql=f'''
            SELECT DISTINCT
                series_code,
                frequency,
                CAST(date AS DATE) AS date,
                CAST(value AS DOUBLE) AS value
            FROM "{SLUG}-values"
            WHERE date IS NOT NULL AND value IS NOT NULL
        ''',
    ),
]
