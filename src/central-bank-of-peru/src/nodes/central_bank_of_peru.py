"""Central Reserve Bank of Peru (BCRPData) connector — both published subsets.

Two download nodes, both reading the single semicolon-delimited, ISO-8859-1
metadata catalog at ``/estadisticas/series/metadata``:

* ``central-bank-of-peru-series`` — one row per series (code, category, group,
  name, unit, frequency, span).
* ``central-bank-of-peru-values`` — long-format observations across all series,
  fetched from the per-series JSON API ``/api/{codes}/json/{start}/{end}/ing``.
  Up to 10 codes of the SAME frequency are batched per request (the API caps at
  10 and rejects mixed frequencies). The ~17,100-series corpus is ~1,700
  requests; a stateless full re-pull each run (~15 min) — late revisions are
  picked up for free.

API quirks learned by probing (2026-06-19):
  * Omitting the date range returns only the LAST ~60 observations, NOT full
    history — so the range is always set explicitly from each series' metadata
    span. An over-wide range (e.g. year 1900 or 2030) returns an empty HTML
    body, so the range is the actual min(start)..max(end) of the batch.
  * Period labels are localized per frequency: Mensual "Jan.1992", Anual
    "1970", Trimestral "Q1.20", Diaria "01.Jan.24". Daily/quarterly carry
    2-digit years, disambiguated against the batch's known 4-digit span.
  * Missing observations come back as the string "n.d." (kept as a null).
  * A bad/empty code returns an empty HTML body with HTTP 200; a poisoned batch
    falls back to per-series fetches so one bad code never drops its 9 siblings.
"""

import pyarrow as pa

from subsets_utils import NodeSpec, save_raw_parquet, raw_parquet_writer
from utils import (
    _C_CODE, _C_CAT, _C_GRP, _C_NAME, _C_DESC,
    _C_GEO, _C_SOURCE, _C_FREQ,
    _C_PUBGRP, _C_AREA, _C_UPDATED, _C_START, _C_END,
    _cell,
    _fetch_catalog_rows,
    _http_get,
)

_API_BASE = "https://estadisticas.bcrp.gob.pe/estadisticas/series/api"
_BATCH = 10  # API hard cap: max 10 codes per request, all same frequency

_ES_MONTHS = {
    "ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6,
    "jul": 7, "ago": 8, "sep": 9, "set": 9, "oct": 10, "nov": 11, "dic": 12,
}
_EN_MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}


# --------------------------------------------------------------------------- #
# central-bank-of-peru-series — the metadata catalog
# --------------------------------------------------------------------------- #
_CATALOG_SCHEMA = pa.schema([
    ("codigo_serie", pa.string()),
    ("categoria", pa.string()),
    ("grupo", pa.string()),
    ("nombre", pa.string()),
    ("descripcion", pa.string()),
    ("geografia", pa.string()),
    ("fuente", pa.string()),
    ("frecuencia", pa.string()),
    ("grupo_publicacion", pa.string()),
    ("area_publica", pa.string()),
    ("fecha_actualizacion", pa.string()),
    ("fecha_inicio", pa.string()),
    ("fecha_fin", pa.string()),
])


def fetch_series(node_id: str) -> None:
    """Download and store the full BCRPData series catalog (one row per series)."""
    asset = node_id
    rows = _fetch_catalog_rows()
    cols = {name: [] for name in _CATALOG_SCHEMA.names}
    for r in rows:
        cols["codigo_serie"].append(_cell(r, _C_CODE))
        cols["categoria"].append(_cell(r, _C_CAT))
        cols["grupo"].append(_cell(r, _C_GRP))
        cols["nombre"].append(_cell(r, _C_NAME))
        cols["descripcion"].append(_cell(r, _C_DESC))
        cols["geografia"].append(_cell(r, _C_GEO))
        cols["fuente"].append(_cell(r, _C_SOURCE))
        cols["frecuencia"].append(_cell(r, _C_FREQ))
        cols["grupo_publicacion"].append(_cell(r, _C_PUBGRP))
        cols["area_publica"].append(_cell(r, _C_AREA))
        cols["fecha_actualizacion"].append(_cell(r, _C_UPDATED))
        cols["fecha_inicio"].append(_cell(r, _C_START))
        cols["fecha_fin"].append(_cell(r, _C_END))
    table = pa.table(cols, schema=_CATALOG_SCHEMA)
    save_raw_parquet(table, asset)


# --------------------------------------------------------------------------- #
# central-bank-of-peru-values — observations
# period-label / metadata-span parsing
# --------------------------------------------------------------------------- #
def _meta_span(start: str, end: str, freq: str):
    """Parse a series' metadata start/end into (start_param, end_param, ymin, ymax).

    Returns None if either bound is unparseable for the given frequency.
    *_param strings are formatted for the API URL; ymin/ymax are 4-digit ints
    used to disambiguate 2-digit period labels in the response.
    """
    try:
        if freq == "Mensual":
            sy, sm = _es_month_year(start)
            ey, em = _es_month_year(end)
            return f"{sy}-{sm}", f"{ey}-{em}", sy, ey
        if freq == "Anual":
            sy, ey = int(start), int(end)
            return f"{sy}", f"{ey}", sy, ey
        if freq == "Trimestral":
            sy, sq = _quarter_year(start)
            ey, eq = _quarter_year(end)
            return f"{sy}-{sq}", f"{ey}-{eq}", sy, ey
        if freq == "Diaria":
            # Already ISO "YYYY-MM-DD".
            sy, ey = int(start[:4]), int(end[:4])
            return start, end, sy, ey
    except (ValueError, KeyError, IndexError):
        return None
    return None


def _es_month_year(s: str) -> tuple[int, int]:
    # "Ene-1992" -> (1992, 1)
    mon, yr = s.split("-")
    return int(yr), _ES_MONTHS[mon.strip().lower()[:3]]


def _quarter_year(s: str) -> tuple[int, int]:
    # "T1-2012" -> (2012, 1)
    q, yr = s.split("-")
    return int(yr), int(q.strip().upper().lstrip("T"))


def _yy_to_year(yy: int, ymin: int, ymax: int) -> int:
    """Disambiguate a 2-digit year against the batch's known 4-digit span."""
    for cand in (1900 + yy, 2000 + yy):
        if ymin - 1 <= cand <= ymax + 1:
            return cand
    # Fallback pivot when the span doesn't decide it.
    return 2000 + yy if yy <= 30 else 1900 + yy


def _label_to_iso(label: str, freq: str, ymin: int, ymax: int) -> str | None:
    """Convert a localized period label to an ISO 'YYYY-MM-DD' date, or None."""
    try:
        if freq == "Mensual":
            mon, yr = label.split(".")
            return f"{int(yr):04d}-{_EN_MONTHS[mon.lower()[:3]]:02d}-01"
        if freq == "Anual":
            return f"{int(label):04d}-01-01"
        if freq == "Trimestral":
            q, yy = label.lstrip("Qq").split(".")
            year = _yy_to_year(int(yy), ymin, ymax)
            month = (int(q) - 1) * 3 + 1
            return f"{year:04d}-{month:02d}-01"
        if freq == "Diaria":
            dd, mon, yy = label.split(".")
            year = _yy_to_year(int(yy), ymin, ymax)
            return f"{year:04d}-{_EN_MONTHS[mon.lower()[:3]]:02d}-{int(dd):02d}"
    except (ValueError, KeyError, IndexError):
        return None
    return None


def _to_float(v) -> float | None:
    if v is None:
        return None
    s = str(v).strip()
    if not s or s.lower() in ("n.d.", "nd", "na", "n/a", "-"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


_VALUES_SCHEMA = pa.schema([
    ("codigo_serie", pa.string()),
    ("frecuencia", pa.string()),
    ("date", pa.string()),     # ISO 'YYYY-MM-DD'; cast to DATE in transform
    ("value", pa.float64()),
])


def _fetch_chunk(codes: list[str], start_p: str, end_p: str) -> dict | None:
    """Fetch one batch of same-frequency codes. Returns parsed JSON or None on
    an empty/non-JSON body (a poisoned/empty batch)."""
    url = f"{_API_BASE}/{'-'.join(codes)}/json/{start_p}/{end_p}/ing"
    resp = _http_get(url)
    # The API serves JSON under a text/html content-type, and returns an empty
    # HTML body (HTTP 200) for an unknown code or out-of-range request. Detect
    # by body shape, not content-type.
    body = resp.content.lstrip()
    if not body or not body.startswith(b"{"):
        return None
    try:
        return resp.json()
    except ValueError:
        return None


def _rows_from_payload(payload: dict, codes: list[str], freq: str,
                       ymin: int, ymax: int):
    """Yield (code, freq, iso_date, value) tuples from one API JSON payload.

    Values align positionally to ``codes`` (config.series preserves request
    order). Returns None to signal an alignment mismatch (caller should retry
    per-series)."""
    series = payload.get("config", {}).get("series") or []
    if len(series) != len(codes):
        return None
    out = []
    for period in payload.get("periods", []):
        iso = _label_to_iso(str(period.get("name", "")), freq, ymin, ymax)
        if iso is None:
            continue
        vals = period.get("values") or []
        for i, code in enumerate(codes):
            v = _to_float(vals[i]) if i < len(vals) else None
            if v is not None:
                out.append((code, freq, iso, v))
    return out


def fetch_values(node_id: str) -> None:
    """Crawl observations for every series, batched ≤10 by frequency."""
    asset = node_id
    rows = _fetch_catalog_rows()

    # group code -> (start, end) by frequency
    by_freq: dict[str, list[tuple[str, str, str, int, int]]] = {}
    skipped = 0
    for r in rows:
        code = _cell(r, _C_CODE)
        freq = _cell(r, _C_FREQ)
        span = _meta_span(_cell(r, _C_START), _cell(r, _C_END), freq)
        if span is None:
            skipped += 1
            continue
        start_p, end_p, ymin, ymax = span
        by_freq.setdefault(freq, []).append((code, start_p, end_p, ymin, ymax))

    if skipped:
        print(f"[values] skipped {skipped} series with unparseable metadata span")

    total_rows = 0
    with raw_parquet_writer(asset, _VALUES_SCHEMA) as writer:
        for freq, series in by_freq.items():
            # Sort by start so chunks share similar spans (fewer n.d. fills).
            series.sort(key=lambda s: (s[1], s[2]))
            for i in range(0, len(series), _BATCH):
                chunk = series[i:i + _BATCH]
                codes = [c[0] for c in chunk]
                start_p = min(c[1] for c in chunk)
                end_p = max(c[2] for c in chunk)
                ymin = min(c[3] for c in chunk)
                ymax = max(c[4] for c in chunk)

                batch_rows = None
                payload = _fetch_chunk(codes, start_p, end_p)
                if payload is not None:
                    batch_rows = _rows_from_payload(
                        payload, codes, freq, ymin, ymax)

                if batch_rows is None:
                    # Poisoned batch or alignment mismatch — fall back to
                    # per-series fetches so one bad code can't drop the rest.
                    batch_rows = []
                    for c in chunk:
                        p = _fetch_chunk([c[0]], c[1], c[2])
                        if p is None:
                            print(f"[values] no data for {c[0]} "
                                  f"({c[1]}..{c[2]})")
                            continue
                        one = _rows_from_payload(
                            p, [c[0]], freq, c[3], c[4]) or []
                        batch_rows.extend(one)

                if batch_rows:
                    table = pa.table(
                        {
                            "codigo_serie": [b[0] for b in batch_rows],
                            "frecuencia": [b[1] for b in batch_rows],
                            "date": [b[2] for b in batch_rows],
                            "value": [b[3] for b in batch_rows],
                        },
                        schema=_VALUES_SCHEMA,
                    )
                    writer.write_table(table)
                    total_rows += len(batch_rows)

    print(f"[values] wrote {total_rows} observation rows")


DOWNLOAD_SPECS = [
    NodeSpec(id="central-bank-of-peru-series", fn=fetch_series, kind="download"),
    NodeSpec(id="central-bank-of-peru-values", fn=fetch_values, kind="download"),
]
