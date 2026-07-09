"""Reserve Bank of Australia — statistical tables connector.

Mechanism: per-table CSV bulk download (research mechanism `bulk_csv`). Each
RBA statistical table is published as one or more CSV files at the stable URL
    https://www.rba.gov.au/statistics/tables/csv/<slug>.csv

Access note: the RBA site is behind Akamai. The default subsets_utils
User-Agent (`DataIntegrations/1.0`) is blocklisted and returns HTTP 403; a
plain descriptive User-Agent passes (verified). We override it once per fetch
via `configure_http`. The tables *index* HTML is bot-blocked regardless, so the
catalog of CSV files was enumerated at the collect stage and is carried in the
entity union — there is no live index scrape here.

Each CSV is a wide statistical-table spreadsheet: a one-line table title, a
metadata block (rows labelled Title / Description / Frequency / Type / Units /
Source / Publication date / Series ID, one column per series), then data rows
(column 0 = observation date, remaining columns = series values). We parse each
CSV into a uniform LONG format (one row per series x observation) so a single
generic SQL transform publishes every subset.

Six subsets are multi-file (collapsed at collect): the five "...by Country"
tables (one CSV per geographic region) and `j1-forecasts` (one CSV per forecast
variable). For those, fetch_one fetches every member CSV and tags each long row
with a `partition_key` (the region / forecast-variable suffix).

Fetch shape: stateless full re-pull (shape 1). The whole corpus is ~tens of MB
across ~210 small CSVs; every CSV is overwritten in place by the source, so we
re-fetch in full each run and overwrite — no watermark, no incremental filter
(the source exposes none).
"""
from __future__ import annotations

import csv
import io
import re
from datetime import datetime, timedelta

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    get,
    configure_http,
    save_raw_parquet,
    transient_retry,
)

SLUG = "reserve-bank-of-australia"
_CSV_BASE = "https://www.rba.gov.au/statistics/tables/csv"

# Plain descriptive UA — the default DataIntegrations/1.0 is Akamai-blocklisted
# (403); this one passes. ASCII-only (httpx headers must be ASCII).
_USER_AGENT = "subsets.io RBA statistics connector (+https://subsets.io)"

# The entity union (rank-active subsets). One DOWNLOAD_SPEC per id.
from constants import ENTITY_IDS

# Entities that collapse several source CSVs into one subset, mapping each
# member CSV slug to its partition_key label. Labels are explicit (not derived
# by prefix-stripping) because the member-slug naming is not uniform: the
# by-country members are "<entity>-<region>" but the J1 members are
# "j1-<variable>" under entity "j1-forecasts".
_REGIONS = {
    "africa-and-middle-east": "africa-and-middle-east",
    "asia-and-pacific": "asia-and-pacific",
    "developed-countries": "developed-countries",
    "developing-europe": "developing-europe",
    "latin-america-and-caribbean": "latin-america-and-caribbean",
    "offshore-centres": "offshore-centres",
}
MULTI_FILE = {
    "b12.1.1": {f"b12.1.1-{r}": lbl for r, lbl in _REGIONS.items()},
    "b12.2.1": {f"b12.2.1-{r}": lbl for r, lbl in _REGIONS.items()},
    "b13.1.1": {f"b13.1.1-{r}": lbl for r, lbl in _REGIONS.items()},
    "b13.1.2": {f"b13.1.2-{r}": lbl for r, lbl in _REGIONS.items()},
    "b13.2.1": {f"b13.2.1-{r}": lbl for r, lbl in _REGIONS.items()},
    "j1-forecasts": {
        "j1-cash-rate": "cash-rate", "j1-dfd-growth": "dfd-growth",
        "j1-exchange-rate": "exchange-rate", "j1-gdp-growth": "gdp-growth",
        "j1-headline-inflation": "headline-inflation",
        "j1-net-exports": "net-exports", "j1-terms-of-trade": "terms-of-trade",
        "j1-underlying-inflation": "underlying-inflation",
        "j1-unemployment-rate": "unemployment-rate", "j1-wpi-growth": "wpi-growth",
    },
}

_RAW_SCHEMA = pa.schema([
    ("series_id", pa.string()),
    ("series_title", pa.string()),
    ("description", pa.string()),
    ("frequency", pa.string()),
    ("series_type", pa.string()),
    ("units", pa.string()),
    ("source", pa.string()),
    ("publication_date", pa.string()),
    ("obs_date", pa.string()),          # ISO yyyy-mm-dd primary date (col 0)
    ("dimension_date", pa.string()),    # secondary date dimension (e.g. J1 forecast target quarter); else null
    ("value_text", pa.string()),        # raw cell; transform TRY_CASTs to double
    ("source_csv", pa.string()),        # the CSV slug this row came from
    ("partition_key", pa.string()),     # region / forecast var for multi-file; else null
    ("record_type", pa.string()),       # observation | series_break
    ("break_type", pa.string()),        # series-break reference rows only
    ("details", pa.string()),           # series-break reference rows only
])

# Metadata-block row labels (column 0). Anything else before the first data row
# is ignored (e.g. the one-line table title).
_META_LABELS = {
    "title": "series_title",
    "description": "description",
    "frequency": "frequency",
    "type": "series_type",
    "units": "units",
    "source": "source",
    "publication date": "publication_date",
    "series id": "series_id",
    "mnemonic": "series_id",   # legacy tables (a5, d10, ...) label the id row "Mnemonic"
}

# RBA mixes 4- and 2-digit years and slash/dash separators across tables.
_DATE_FORMATS = ("%d/%m/%Y", "%d-%b-%Y", "%d-%b-%y", "%Y-%m-%d", "%d/%m/%y")
_EXCEL_EPOCH = datetime(1899, 12, 30).date()


# --- transport ---------------------------------------------------------------


@transient_retry()
def _fetch_csv_text(slug: str) -> str:
    url = f"{_CSV_BASE}/{slug}.csv"
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    # CSVs carry a UTF-8 BOM; utf-8-sig strips it. Text fields may hold
    # en-dashes / smart quotes — that's fine in the body, only headers are ASCII.
    return resp.content.decode("utf-8-sig", errors="replace")


# --- parsing -----------------------------------------------------------------

def _parse_iso_date(raw: str) -> str | None:
    raw = (raw or "").strip()
    if not raw:
        return None
    if raw.isdigit():
        serial = int(raw)
        if 20000 <= serial <= 60000:
            return (_EXCEL_EPOCH + timedelta(days=serial)).isoformat()
    for fmt in _DATE_FORMATS:
        try:
            return datetime.strptime(raw, fmt).date().isoformat()
        except ValueError:
            continue
    return None


def _slug_year(slug: str) -> str | None:
    match = re.search(r"(19|20)\d{2}", slug)
    if not match:
        return None
    return f"{match.group(0)}-12-31"


def _series_id_from_title(slug: str, title: str, col: int) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    if not cleaned:
        cleaned = f"column-{col}"
    return f"{slug}-{cleaned}"


def _parse_rba_csv(text: str, slug: str, partition_key: str | None) -> list[dict]:
    """Parse one RBA statistical-table CSV into long-format rows."""
    rows = list(csv.reader(io.StringIO(text)))
    # Per-column metadata, keyed by column index (1..N; column 0 is the date).
    meta: dict[int, dict] = {}
    data_start = None
    for i, row in enumerate(rows):
        if not row:
            continue
        label = (row[0] or "").strip().lower()
        if label in _META_LABELS:
            field = _META_LABELS[label]
            for col in range(1, len(row)):
                meta.setdefault(col, {})[field] = (row[col] or "").strip() or None
            continue
        # First row whose column 0 parses as a date marks the data block.
        if _parse_iso_date(row[0]) is not None:
            data_start = i
            break

    if data_start is None and meta:
        return _parse_matrix_csv(rows, slug, partition_key, meta)
    if data_start is None or not meta:
        return []

    # Only columns that carry a non-empty Series ID are real series.
    series_cols = [c for c, m in sorted(meta.items()) if m.get("series_id")]
    # Columns whose Units is exactly 'Date' are a within-row date dimension, not
    # a measured series (e.g. J1 forecasts' "Target quarter"): a single survey
    # date carries one forecast per target quarter, so (series, obs_date) is not
    # unique without it. Pull them out — unless that would leave no value columns.
    date_dim_cols = [c for c in series_cols if (meta[c].get("units") or "") == "Date"]
    value_cols = [c for c in series_cols if c not in date_dim_cols]
    if not value_cols:                 # degenerate: keep everything as series
        value_cols, date_dim_cols = series_cols, []

    out: list[dict] = []
    for row in rows[data_start:]:
        if not row:
            continue
        iso = _parse_iso_date(row[0])
        if iso is None:
            continue
        dim_date = None
        for c in date_dim_cols:
            if c < len(row):
                dim_date = _parse_iso_date(row[c]) or (row[c].strip() or None)
                if dim_date:
                    break
        for col in value_cols:
            if col >= len(row):
                continue
            cell = (row[col] or "").strip()
            if cell == "":
                continue
            m = meta[col]
            out.append({
                "series_id": m.get("series_id"),
                "series_title": m.get("series_title"),
                "description": m.get("description"),
                "frequency": m.get("frequency"),
                "series_type": m.get("series_type"),
                "units": m.get("units"),
                "source": m.get("source"),
                "publication_date": m.get("publication_date"),
                "obs_date": iso,
                "dimension_date": dim_date,
                "value_text": cell,
                "source_csv": slug,
                "partition_key": partition_key,
                "record_type": "observation",
                "break_type": None,
                "details": None,
            })
    return out


def _parse_matrix_csv(
    rows: list[list[str]],
    slug: str,
    partition_key: str | None,
    meta: dict[int, dict],
) -> list[dict]:
    """Parse cross-sectional RBA survey matrices with no date/Series ID row."""
    obs_date = _slug_year(slug)
    if obs_date is None:
        return []

    value_cols = [
        c for c, m in sorted(meta.items())
        if m.get("series_title") or m.get("description")
    ]
    if not value_cols:
        return []

    start_idx = None
    seen_publication_date = False
    for i, row in enumerate(rows):
        label = (row[0] or "").strip().lower() if row else ""
        if label == "publication date":
            seen_publication_date = True
            continue
        if seen_publication_date and row and (row[0] or "").strip():
            # Skip blank spacer rows after the metadata block; the first
            # populated label starts the survey matrix.
            start_idx = i
            break
    if start_idx is None:
        return []

    out: list[dict] = []
    section = None
    for row in rows[start_idx:]:
        if not row:
            continue
        label = (row[0] or "").strip()
        if not label:
            continue

        values = {
            col: ((row[col] or "").strip() if col < len(row) else "")
            for col in value_cols
        }
        non_empty_values = [v for v in values.values() if v]
        if not non_empty_values:
            section = label
            continue

        for col, cell in values.items():
            if not cell:
                continue
            m = meta[col]
            title = m.get("series_title") or m.get("description") or f"column {col}"
            out.append({
                "series_id": _series_id_from_title(slug, title, col),
                "series_title": title,
                "description": m.get("description"),
                "frequency": m.get("frequency"),
                "series_type": m.get("series_type"),
                "units": m.get("units"),
                "source": m.get("source"),
                "publication_date": m.get("publication_date"),
                "obs_date": obs_date,
                "dimension_date": None,
                "value_text": cell,
                "source_csv": slug,
                "partition_key": partition_key,
                "record_type": "observation",
                "break_type": section,
                "details": label,
            })
    return out


def _is_event_csv(text: str) -> bool:
    """True for RBA event/reference CSVs: a Date-headed table of annotations
    with no per-column metadata block (series breaks, F1 expert judgement)."""
    return not any(
        row and (row[0] or "").strip().lower() in _META_LABELS
        for row in csv.reader(io.StringIO(text))
    )


def _parse_event_csv(text: str, slug: str, record_type: str) -> list[dict]:
    """Parse an RBA event/reference CSV: Date, event type, series title, details."""
    rows = list(csv.reader(io.StringIO(text)))
    header_idx = None
    for i, row in enumerate(rows):
        if len(row) >= 3 and row[0].strip().lower() == "date":
            header_idx = i
            break
    if header_idx is None:
        return []

    out: list[dict] = []
    for row in rows[header_idx + 1:]:
        if len(row) < 3:
            continue
        iso = _parse_iso_date(row[0])
        if iso is None:
            continue
        details = " ".join(cell.strip() for cell in row[3:] if cell.strip()) or None
        out.append({
            "series_id": None,
            "series_title": row[2].strip() or None,
            "description": details,
            "frequency": None,
            "series_type": None,
            "units": None,
            "source": "RBA",
            "publication_date": None,
            "obs_date": iso,
            "dimension_date": None,
            "value_text": details,
            "source_csv": slug,
            "partition_key": None,
            "record_type": record_type,
            "break_type": row[1].strip() or None,
            "details": details,
        })
    return out


# --- fetch -------------------------------------------------------------------

def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    configure_http(headers={"User-Agent": _USER_AGENT})

    entity_id = node_id[len(SLUG) + 1:]  # strip "reserve-bank-of-australia-"
    # member CSV slug -> partition_key label. Single-file subsets map the one
    # CSV (named after the entity) to a null partition.
    members = MULTI_FILE.get(entity_id, {entity_id: None})

    all_rows: list[dict] = []
    for slug, partition_key in members.items():
        text = _fetch_csv_text(slug)
        if slug.endswith("series-breaks"):
            rows = _parse_event_csv(text, slug, "series_break")
        elif _is_event_csv(text):
            rows = _parse_event_csv(text, slug, "annotation")
        else:
            rows = _parse_rba_csv(text, slug, partition_key)
        if not rows:
            raise ValueError(f"{asset}: parsed 0 long rows from {slug}.csv")
        all_rows.extend(rows)

    table = pa.Table.from_pylist(all_rows, schema=_RAW_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
