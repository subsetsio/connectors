"""NASA multi-surface connector — download stage (raw fetches only).

Four no-auth NASA surfaces, one download NodeSpec per rank-accepted entity:

- Exoplanet Archive TAP (11 tables): full-table `select * from <t>` CSV dumps,
  streamed to gzipped CSV raw (tables run up to ~48k rows x 720 cols).
- JPL SSD/CNEOS REST (cad, fireball, sentry, nhats): small JSON snapshots,
  flattened to NDJSON. cad is pulled with a fixed wide 1900..2100 window
  (the endpoint's full advertised horizon, not a hardcoded data range).
- GISTEMP v4 bulk CSVs: monthly hemispheric anomalies stacked long, plus the
  zonal annual means. Missing cells ('***') become nulls.
- EONET v3 events: one row per event geometry.

All corpora re-pull in full every run (each fetch is seconds and megabytes;
no incremental state to drift). Transforms are authored by the transform
stage as transforms/<table>.sql — none live here.
"""

from __future__ import annotations

import httpx

from subsets_utils import NodeSpec, get_client, raw_writer, save_raw_ndjson
from utils import get_json, get_text, retry

# ---------------------------------------------------------------------------
# Exoplanet Archive TAP
# ---------------------------------------------------------------------------

EXOPLANET_TABLES = [
    "ps", "pscomppars", "toi", "k2pandc", "ml", "stellarhosts", "TD",
    "CUMULATIVE", "Q1_Q17_DR25_KOI", "Q1_Q17_DR25_SUP_KOI", "Q1_Q17_DR25_TCE",
]

TAP_SYNC = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"


def _spec_id(entity: str) -> str:
    return "nasa-" + entity.lower().replace("_", "-")


# spec id -> exact TAP table name (spec ids are lower/dashed and lose case)
_EXO_BY_SPEC = {_spec_id(t): t for t in EXOPLANET_TABLES}


@retry
def fetch_exoplanet(node_id: str) -> None:
    asset = node_id
    table = _EXO_BY_SPEC[node_id]
    params = {"query": f"select * from {table}", "format": "csv"}
    client = get_client()
    # Stream straight to disk: tables range up to ~48k rows x 720 cols, too big
    # to hold the whole CSV in memory comfortably. Retry re-opens (overwrites).
    with raw_writer(asset, "csv.gz", mode="wt", compression="gzip") as out:
        with client.stream(
            "GET", TAP_SYNC, params=params,
            timeout=httpx.Timeout(600.0, connect=15.0),
        ) as resp:
            resp.raise_for_status()
            wrote_any = False
            for chunk in resp.iter_text():
                if chunk:
                    out.write(chunk)
                    wrote_any = True
    if not wrote_any:
        raise AssertionError(f"{asset}: TAP returned an empty body for {table}")


# ---------------------------------------------------------------------------
# JPL SSD / CNEOS REST
# ---------------------------------------------------------------------------

# JPL endpoint -> request params (cad needs an explicit wide history window;
# the others return their full snapshot with no params).
JPL_ENDPOINTS = {
    "cad": {"date-min": "1900-01-01", "date-max": "2100-01-01"},
    "fireball": {},
    "sentry": {},
    "nhats": {},
}


def fetch_jpl(node_id: str) -> None:
    asset = node_id
    endpoint = node_id[len("nasa-"):]
    params = JPL_ENDPOINTS[endpoint]
    payload = get_json(f"https://ssd-api.jpl.nasa.gov/{endpoint}.api", params)

    data = payload.get("data") or []
    fields = payload.get("fields")
    if isinstance(fields, list) and data and isinstance(data[0], list):
        # {fields[], data[][]} envelope (cad, fireball). Sanitize dashed names.
        cols = [f.replace("-", "_") for f in fields]
        records = [dict(zip(cols, row)) for row in data]
    else:
        # list of dicts (sentry, nhats)
        records = list(data)

    # Flatten any one-level nested dicts (nhats min_dv / min_dur) so the raw is
    # flat scalars and the transform needs no struct access.
    flat = []
    for rec in records:
        out = {}
        for k, v in rec.items():
            if isinstance(v, dict):
                for kk, vv in v.items():
                    out[f"{k}_{kk}"] = vv
            else:
                out[k] = v
        flat.append(out)

    if not flat:
        raise AssertionError(f"{asset}: JPL {endpoint} returned no rows")
    save_raw_ndjson(flat, asset)


# ---------------------------------------------------------------------------
# GISTEMP v4 bulk CSVs
# ---------------------------------------------------------------------------

GISTEMP_BASE = "https://data.giss.nasa.gov/gistemp/tabledata_v4/"
# region label -> filename groups for the monthly long table.
GISTEMP_MONTHLY = {
    "Global": "GLB.Ts+dSST.csv",
    "NH": "NH.Ts+dSST.csv",
    "SH": "SH.Ts+dSST.csv",
}
GISTEMP_ZONAL_FILE = "ZonAnn.Ts+dSST.csv"


def _parse_anomaly(token: str):
    """GISTEMP cells: '***' = missing; decimals printed as '-.19' / '.04'."""
    t = token.strip()
    if not t or t == "***":
        return None
    try:
        return float(t)
    except ValueError:
        return None


def _gistemp_rows(text: str):
    """Yield (header, data_cells) — skipping an optional title line and the
    repeated header / footer-note lines GISTEMP interleaves."""
    lines = [ln for ln in text.splitlines() if ln.strip()]
    # First data-bearing header is the line beginning with 'Year'.
    header = None
    for ln in lines:
        if ln.startswith("Year"):
            header = ln.split(",")
            break
    if header is None:
        raise AssertionError("GISTEMP: no 'Year' header line found")
    for ln in lines:
        cells = ln.split(",")
        year = cells[0].strip()
        if len(year) == 4 and year.isdigit():
            yield header, cells


def fetch_gistemp(node_id: str) -> None:
    asset = node_id
    rows = []
    if node_id == "nasa-gistemp-monthly-anomalies":
        for region, fname in GISTEMP_MONTHLY.items():
            text = get_text(GISTEMP_BASE + fname)
            for header, cells in _gistemp_rows(text):
                year = int(cells[0])
                for j in range(1, len(header)):
                    val = _parse_anomaly(cells[j]) if j < len(cells) else None
                    rows.append({
                        "region": region,
                        "year": year,
                        "period": header[j].strip(),
                        "anomaly_c": val,
                    })
    elif node_id == "nasa-gistemp-zonal-annual":
        text = get_text(GISTEMP_BASE + GISTEMP_ZONAL_FILE)
        for header, cells in _gistemp_rows(text):
            year = int(cells[0])
            for j in range(1, len(header)):
                val = _parse_anomaly(cells[j]) if j < len(cells) else None
                rows.append({
                    "year": year,
                    "zone": header[j].strip(),
                    "anomaly_c": val,
                })
    else:
        raise AssertionError(f"unexpected gistemp node {node_id}")

    if not rows:
        raise AssertionError(f"{asset}: parsed zero GISTEMP rows")
    save_raw_ndjson(rows, asset)


# ---------------------------------------------------------------------------
# EONET v3 events
# ---------------------------------------------------------------------------

EONET_EVENTS = "https://eonet.gsfc.nasa.gov/api/v3/events"


def fetch_eonet(node_id: str) -> None:
    asset = node_id
    payload = get_json(EONET_EVENTS, {"status": "all"})
    events = payload.get("events") or []
    rows = []
    for ev in events:
        cats = ev.get("categories") or [{}]
        srcs = ev.get("sources") or [{}]
        cat = cats[0] if cats else {}
        src = srcs[0] if srcs else {}
        for geom in ev.get("geometry") or []:
            coords = geom.get("coordinates")
            lon = lat = None
            if geom.get("type") == "Point" and isinstance(coords, list) and len(coords) >= 2:
                try:
                    lon, lat = float(coords[0]), float(coords[1])
                except (TypeError, ValueError):
                    lon = lat = None
            rows.append({
                "event_id": ev.get("id"),
                "title": ev.get("title"),
                "category_id": cat.get("id"),
                "category_title": cat.get("title"),
                "source_id": src.get("id"),
                "closed": ev.get("closed"),
                "date": geom.get("date"),
                "geom_type": geom.get("type"),
                "longitude": lon,
                "latitude": lat,
                "magnitude_value": geom.get("magnitudeValue"),
                "magnitude_unit": geom.get("magnitudeUnit"),
            })
    if not rows:
        raise AssertionError(f"{asset}: EONET returned no event geometries")
    save_raw_ndjson(rows, asset)


# ---------------------------------------------------------------------------
# Specs — one per rank-accepted collect entity
# ---------------------------------------------------------------------------

DOWNLOAD_SPECS = (
    [NodeSpec(id=_spec_id(t), fn=fetch_exoplanet, kind="download")
     for t in EXOPLANET_TABLES]
    + [NodeSpec(id=f"nasa-{e}", fn=fetch_jpl, kind="download")
       for e in JPL_ENDPOINTS]
    + [
        NodeSpec(id="nasa-gistemp-monthly-anomalies", fn=fetch_gistemp, kind="download"),
        NodeSpec(id="nasa-gistemp-zonal-annual", fn=fetch_gistemp, kind="download"),
        NodeSpec(id="nasa-events", fn=fetch_eonet, kind="download"),
    ]
)
