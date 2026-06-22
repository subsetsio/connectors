"""Audubon Christmas Bird Count (CBC) connector.

Source: the public `HistoricalResultsByCount` CSV report at
netapp.audubon.org. One stateless GET per count circle
(`?rf=CSV&cid=<id>&sy=<startYear>&ey=<endYear>`) returns that circle's ENTIRE
multi-year history as a single multi-section CSV: circle metadata
(name/abbrev/lat-long), per-year weather, a species x count-year observation
matrix, and observers. No auth, no cookies, no pagination.

Two published tables, each its own download node:

  - observations: long-format bird counts (circle x species x count-year). The
    flagship dataset — the longest-running community-science wildlife record,
    back to the first count in 1900.
  - circles: one row per count circle with geographic coordinates. Reference
    data, joinable to observations on circle_id.

Both nodes crawl the full set of circles (enumerated by scanning the cid band,
see constants.py). The same upstream CSV backs both tables, but the one-download-
per-entity contract makes them independent nodes, so each crawls the corpus once
— the cost of the source publishing every table inside one per-circle file with
no lighter metadata endpoint.

Shape: stateless full re-pull. The corpus is a few-thousand circles re-fetched
in full each run and overwritten; revisions and late editorial corrections are
picked up for free. No watermark/cursor — the source exposes no since-filter
that returns only changed records.
"""
from __future__ import annotations

import csv
import io
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

import pyarrow as pa
import pyarrow.parquet as pq

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_parquet,
    raw_parquet_writer,
)
from constants import CID_MIN, CID_MAX, CID_CEILING_MARGIN, SY, EY

REPORT_URL = (
    "https://netapp.audubon.org/CBCObservation/Reports/HistoricalResultsByCount.aspx"
)

# Concurrent fetchers. The source is an older IIS/ASP.NET app with no documented
# rate limit; keep concurrency modest to stay polite.
WORKERS = 8

# A cid with no circle returns a ~325-byte header-only template (HTTP 200).
# Real circles return much more even when sparse; this threshold separates them.
EMPTY_RESPONSE_MAX_BYTES = 600

# Abort the crawl if more than this fraction of circle fetches fail outright
# (after retries) — a few transient losses are tolerable, a systemic failure is
# corruption we must not publish over.
MAX_FETCH_FAILURE_FRACTION = 0.01

# Buffer this many observation rows before flushing a parquet row group, so we
# don't emit one tiny row group per circle.
OBS_FLUSH_ROWS = 100_000

OBS_SCHEMA = pa.schema(
    [
        ("circle_id", pa.int64()),
        ("common_name", pa.string()),
        ("scientific_name", pa.string()),
        ("count_year", pa.int32()),
        ("season_year", pa.int32()),
        ("count_date", pa.string()),          # MM/DD/YYYY, cast to DATE in transform
        ("how_many", pa.int64()),             # null when count-week-only / unreported
        ("count_week_only", pa.bool_()),      # seen during count week, not count day
        ("number_per_party_hours", pa.float64()),
        ("flags", pa.string()),
    ]
)

CIRCLE_SCHEMA = pa.schema(
    [
        ("circle_id", pa.int64()),
        ("circle_name", pa.string()),
        ("abbrev", pa.string()),
        ("latitude", pa.float64()),
        ("longitude", pa.float64()),
    ]
)

_YEAR_RE = re.compile(r"\s*(\d{4})\s*\[(\d+)\]")
_DATE_RE = re.compile(r"Count Date:\s*([\d/]+)")


@transient_retry()
def _fetch_circle_csv(cid: int) -> str:
    """Fetch one circle's full-history CSV. Retries transient errors; raises on
    permanent ones (treated as a bug/corruption, not a per-circle skip)."""
    resp = get(
        REPORT_URL,
        params={"rf": "CSV", "cid": cid, "sy": SY, "ey": EY},
        timeout=(10.0, 180.0),
    )
    resp.raise_for_status()
    return resp.text


def _is_empty(text: str) -> bool:
    return len(text.encode("utf-8", "ignore")) <= EMPTY_RESPONSE_MAX_BYTES


def _clean(s: str | None) -> str | None:
    if s is None:
        return None
    s = s.strip()
    return s or None


def _parse_circle_csv(cid: int, text: str) -> tuple[dict | None, list[dict]]:
    """Return (circle_metadata, observation_rows) parsed from one circle CSV.

    The file is a multi-section CSV (blank-line-delimited blocks, each with its
    own header). We walk csv-parsed rows and switch on the header rows. The
    observation section's `COM_NAME` and `CountYear` cells are multi-line quoted
    blobs (common+scientific name; year [count_year] + count date + effort
    metadata) — parsed field-by-field below.
    """
    rows = csv.reader(io.StringIO(text))
    section = None
    circle: dict | None = None
    obs: list[dict] = []

    for r in rows:
        if not r:
            continue
        head = r[0].lstrip("﻿").strip()  # strip BOM on the first cell
        if not head:
            continue
        if head == "CircleName":
            section = "circle"
            continue
        if head == "COM_NAME":
            section = "obs"
            continue
        if head.startswith("CountYear"):  # weather / effort sub-tables — not published
            section = "skip"
            continue
        if head.startswith("#"):
            continue

        if section == "circle" and circle is None:
            lat = lon = None
            latlong = r[2] if len(r) > 2 else ""
            if "/" in latlong:
                a, b = latlong.split("/", 1)
                try:
                    lat, lon = float(a), float(b)
                except ValueError:
                    lat = lon = None
            circle = {
                "circle_id": cid,
                "circle_name": _clean(r[0]),
                "abbrev": _clean(r[1]) if len(r) > 1 else None,
                "latitude": lat,
                "longitude": lon,
            }
            section = None
        elif section == "obs" and len(r) >= 5:
            how = r[2].strip()
            if not how:
                continue  # species not reported this count year — sparse row, skip
            com_lines = r[0].split("\n")
            common = _clean(com_lines[0])
            scientific = None
            for ln in com_lines[1:]:
                ln = ln.strip()
                if ln.startswith("[") and ln.endswith("]"):
                    scientific = _clean(ln[1:-1])
            cy_lines = r[1].split("\n")
            m = _YEAR_RE.match(cy_lines[0])
            season_year = int(m.group(1)) if m else None
            count_year = int(m.group(2)) if m else None
            count_date = None
            for ln in cy_lines:
                dm = _DATE_RE.search(ln)
                if dm:
                    count_date = dm.group(1)
                    break
            cw = how.lower() == "cw"
            how_many = int(how) if how.isdigit() else None
            npph_raw = r[3].strip()
            try:
                npph = float(npph_raw) if npph_raw else None
            except ValueError:
                npph = None
            obs.append(
                {
                    "circle_id": cid,
                    "common_name": common,
                    "scientific_name": scientific,
                    "count_year": count_year,
                    "season_year": season_year,
                    "count_date": count_date,
                    "how_many": how_many,
                    "count_week_only": cw,
                    "number_per_party_hours": npph,
                    "flags": _clean(r[4]),
                }
            )

    return circle, obs


def _crawl(cids, handle):
    """Fetch every cid concurrently; call handle(cid, text) for non-empty
    responses in the main thread. Tracks the highest valid cid (band-ceiling
    guard) and aborts if too many fetches fail."""
    cids = list(cids)
    failures = 0
    max_valid_cid = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(_fetch_circle_csv, c): c for c in cids}
        for fut in as_completed(futs):
            cid = futs[fut]
            try:
                text = fut.result()
            except Exception as exc:  # noqa: BLE001 - logged with context, then thresholded
                failures += 1
                print(f"  cid={cid}: fetch failed ({type(exc).__name__}: {exc})")
                continue
            if _is_empty(text):
                continue
            max_valid_cid = max(max_valid_cid, cid)
            handle(cid, text)

    if max_valid_cid >= CID_MAX - CID_CEILING_MARGIN:
        raise RuntimeError(
            f"valid circle found at cid={max_valid_cid}, within {CID_CEILING_MARGIN} "
            f"of CID_MAX={CID_MAX}: the id band has grown — widen CID_MAX in constants.py"
        )
    if failures > max(1, int(len(cids) * MAX_FETCH_FAILURE_FRACTION)):
        raise RuntimeError(
            f"{failures}/{len(cids)} circle fetches failed (> "
            f"{MAX_FETCH_FAILURE_FRACTION:.0%}) — refusing to publish a truncated corpus"
        )


def fetch_observations(node_id: str) -> None:
    asset = node_id
    buf: list[dict] = []

    with raw_parquet_writer(asset, OBS_SCHEMA) as writer:

        def flush():
            if buf:
                writer.write_table(pa.Table.from_pylist(buf, schema=OBS_SCHEMA))
                buf.clear()

        def handle(cid: int, text: str) -> None:
            _, obs = _parse_circle_csv(cid, text)
            buf.extend(obs)
            if len(buf) >= OBS_FLUSH_ROWS:
                flush()

        _crawl(range(CID_MIN, CID_MAX + 1), handle)
        flush()


def fetch_circles(node_id: str) -> None:
    asset = node_id
    circles: list[dict] = []

    def handle(cid: int, text: str) -> None:
        circle, _ = _parse_circle_csv(cid, text)
        if circle is not None:
            circles.append(circle)

    _crawl(range(CID_MIN, CID_MAX + 1), handle)
    save_raw_parquet(pa.Table.from_pylist(circles, schema=CIRCLE_SCHEMA), asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="christmas-bird-count-observations", fn=fetch_observations, kind="download"),
    NodeSpec(id="christmas-bird-count-circles", fn=fetch_circles, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="christmas-bird-count-observations-transform",
        deps=["christmas-bird-count-observations"],
        sql='''
            SELECT
                circle_id,
                common_name,
                scientific_name,
                count_year,
                season_year,
                TRY_STRPTIME(count_date, '%m/%d/%Y')::DATE AS count_date,
                how_many,
                count_week_only,
                number_per_party_hours,
                flags
            FROM "christmas-bird-count-observations"
            WHERE common_name IS NOT NULL
              AND count_year IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="christmas-bird-count-circles-transform",
        deps=["christmas-bird-count-circles"],
        sql='''
            SELECT
                circle_id,
                circle_name,
                abbrev,
                latitude,
                longitude
            FROM "christmas-bird-count-circles"
            WHERE circle_id IS NOT NULL
        ''',
    ),
]
