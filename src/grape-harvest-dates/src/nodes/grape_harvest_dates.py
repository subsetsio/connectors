"""European grape-harvest dates connector.

Source: NOAA/WDS Paleoclimatology "Western Europe 650 Year Grape Harvest Date
Database" (Daux et al. 2012, doi:10.25921/2xg2-mt70). A single ~262 KB
fixed-width text file holds 27 regional composite grape-harvest-date (GHD)
series, expressed as days after 31 August, for Year 1354-2007.

Two published subsets, both parsed from the same file:
  - harvest-dates : long-format observations (region, region_code, year, harvest_date)
  - regions       : the 27-region reference table with lat/lon (joinable on region_code)

The dataset is static (last updated 8/2012), so each fetch is a full re-pull of
the one file (stateless) — cheap and revision-safe.
"""

import re

import pyarrow as pa
from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet, transient_retry

GHD_TXT_URL = "https://www.ncei.noaa.gov/pub/data/paleo/historical/europe/europe2012ghd.txt"

# A short code is a letter-led token like "Als", "Cha1", "NLo" — the per-block
# column anchors. The location table also gives the canonical region names + lat/lon.
_CODE_RE = re.compile(r"^[A-Za-z][A-Za-z0-9()]{1,5}$")
_NUM_RE = re.compile(r"-?\d+\.\d+|-?\d+")
_BLOCK_RE = re.compile(r"part \d of 3")
_LOC_RE = re.compile(r"^(.*?)\s+(-?\d+\.?\d*)\s+(-?\d+\.?\d*)\s*$")

HARVEST_SCHEMA = pa.schema([
    ("region", pa.string()),
    ("region_code", pa.string()),
    ("year", pa.int32()),
    ("harvest_date", pa.float64()),
])

REGIONS_SCHEMA = pa.schema([
    ("region", pa.string()),
    ("region_code", pa.string()),
    ("latitude", pa.float64()),
    ("longitude", pa.float64()),
])


@transient_retry()
def _download_text() -> str:
    resp = get(GHD_TXT_URL, timeout=(10.0, 120.0))
    resp.raise_for_status()
    # Latin-1: the header carries accented region names (Rhône, Vendée).
    return resp.content.decode("latin-1")


def _parse_locations(lines):
    """Ordered list of (region_name, latitude, longitude) from the header table.

    This order is canonical and matches the per-block column order, so the
    9 regions of block N are locations[N*9 : N*9+9]."""
    start = next(i for i, l in enumerate(lines) if "Latitude" in l and "Longitude" in l)
    locs = []
    for l in lines[start + 1:]:
        if not l.strip():
            continue
        if l.strip().startswith("DATA"):
            break
        m = _LOC_RE.match(l)
        if not m:
            raise AssertionError(f"unparseable region location row: {l!r}")
        locs.append((m.group(1).strip(), float(m.group(2)), float(m.group(3))))
    if len(locs) != 27:
        raise AssertionError(f"expected 27 region locations, parsed {len(locs)}")
    return locs


def _token_centers(line):
    """Character-center of every whitespace-delimited token on a line."""
    return [(m.start() + m.end()) / 2 for m in re.finditer(r"\S+", line)]


def _find_code_row(lines, block_idx):
    """Index of the short-code header row for a block: the row whose tokens after
    the first are exactly 9 short codes. (Block 1's leading token is 'Year';
    blocks 2-3 lead with '1354' — a quirk of the file, both handled here.)"""
    for i in range(block_idx + 1, block_idx + 6):
        toks = lines[i].split()
        if len(toks) == 10 and all(_CODE_RE.match(t) for t in toks[1:]):
            return i
    raise AssertionError(f"no code row found after block header at line {block_idx}")


def _parse_ghd(text):
    """Parse the file into (regions, observations).

    regions: list of dicts region/region_code/latitude/longitude (27 rows).
    observations: list of dicts region/region_code/year/harvest_date (one per
    non-blank cell)."""
    lines = text.splitlines()
    locs = _parse_locations(lines)
    block_hdrs = [i for i, l in enumerate(lines) if _BLOCK_RE.search(l)]
    if len(block_hdrs) != 3:
        raise AssertionError(f"expected 3 data blocks, found {len(block_hdrs)}")

    regions = []
    observations = []
    for bn, bi in enumerate(block_hdrs):
        code_row = _find_code_row(lines, bi)
        codes = lines[code_row].split()[1:]            # 9 short codes
        centers = _token_centers(lines[code_row])[1:]  # 9 column centers (drop leading token)
        region_slice = locs[bn * 9: bn * 9 + 9]
        if len(region_slice) != 9:
            raise AssertionError(f"block {bn + 1}: expected 9 regions, got {len(region_slice)}")

        for ci, code in enumerate(codes):
            name, lat, lon = region_slice[ci]
            regions.append({
                "region": name,
                "region_code": code,
                "latitude": lat,
                "longitude": lon,
            })

        end = block_hdrs[bn + 1] if bn + 1 < len(block_hdrs) else len(lines)
        for l in lines[code_row + 1:end]:
            if not l.strip():
                continue
            toks = [(m.group(), (m.start() + m.end()) / 2) for m in _NUM_RE.finditer(l)]
            if not toks:
                continue
            year = int(float(toks[0][0]))
            if year < 1300 or year > 2100:   # guard against stray trailing summary rows
                continue
            for val, pos in toks[1:]:
                ci = min(range(9), key=lambda k: abs(centers[k] - pos))
                name, _, _ = region_slice[ci]
                observations.append({
                    "region": name,
                    "region_code": codes[ci],
                    "year": year,
                    "harvest_date": float(val),
                })

    if len(regions) != 27:
        raise AssertionError(f"expected 27 regions, built {len(regions)}")
    return regions, observations


def fetch_harvest_dates(node_id: str) -> None:
    asset = node_id
    _, observations = _parse_ghd(_download_text())
    if not observations:
        raise AssertionError("parsed zero harvest-date observations")
    table = pa.Table.from_pylist(observations, schema=HARVEST_SCHEMA)
    save_raw_parquet(table, asset)


def fetch_regions(node_id: str) -> None:
    asset = node_id
    regions, _ = _parse_ghd(_download_text())
    table = pa.Table.from_pylist(regions, schema=REGIONS_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="grape-harvest-dates-harvest-dates", fn=fetch_harvest_dates, kind="download"),
    NodeSpec(id="grape-harvest-dates-regions", fn=fetch_regions, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="grape-harvest-dates-harvest-dates-transform",
        deps=["grape-harvest-dates-harvest-dates"],
        sql='''
            SELECT
                region,
                region_code,
                CAST(year AS INTEGER)        AS year,
                CAST(harvest_date AS DOUBLE) AS harvest_date
            FROM "grape-harvest-dates-harvest-dates"
            WHERE harvest_date IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="grape-harvest-dates-regions-transform",
        deps=["grape-harvest-dates-regions"],
        sql='''
            SELECT
                region,
                region_code,
                CAST(latitude AS DOUBLE)  AS latitude,
                CAST(longitude AS DOUBLE) AS longitude
            FROM "grape-harvest-dates-regions"
        ''',
    ),
]
