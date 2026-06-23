"""GFED (Global Fire Emissions Database) — regional emission summary tables.

Two published subsets, one per GFED release:
  - emissions_gfed5: current GFED5.1 (1997-2024)
  - emissions_gfed4: legacy GFED4.1s with small fires (1997-2023, 2017+ beta)

Each release publishes ~40 per-species text files under an open HTTP directory
(no auth, no pagination). Every file is fixed-width whitespace text: a '#'
comment header (carrying the per-species unit), then 7 stacked fire-type
sub-tables, each a block of region rows x year columns ending in a '| Mean'
column. We parse every species file, reshape the wide year columns into long
records, and write one parquet per release with columns
(species, fire_type, region, year, value, unit).

Fetch shape: stateless full re-pull. The whole corpus is ~1MB of text per
release and re-fetched every run; revisions are picked up for free. No
watermark/cursor — there is no incremental filter and none is needed.
"""

import re

import pyarrow as pa
from subsets_utils import NodeSpec, SqlNodeSpec, get, transient_retry, save_raw_parquet

# Per-release directory of one .txt summary table per chemical species.
SOURCES = {
    "gfed-emissions-gfed5": {
        "index_url": "https://www.globalfiredata.org/tables/",
        "prefix": "GFED5.1",
    },
    "gfed-emissions-gfed4": {
        "index_url": "https://www.geo.vu.nl/~gwerf/GFED/GFED4/tables/",
        "prefix": "GFED4.1s",
    },
}

SCHEMA = pa.schema([
    ("species", pa.string()),
    ("fire_type", pa.string()),
    ("region", pa.string()),
    ("year", pa.int32()),
    ("value", pa.float64()),
    ("unit", pa.string()),
])

# A species file must yield at least this many region rows across its 7 fire-type
# sections; a smaller count means the fixed-width layout changed and parsing
# silently dropped rows. Each section carries ~15 regions x 7 sections ~= 100.
_MIN_ROWS_PER_SPECIES = 40

_UNIT_RE = re.compile(r"emissions estimates in (.+?) for the (?:globe|world)", re.I)


@transient_retry()
def _get_text(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


def _list_species(index_url: str, prefix: str) -> list:
    """Enumerate species codes from the directory index (one .txt per species)."""
    html = _get_text(index_url)
    pat = re.compile(
        r'href="(?:[^"]*/)?' + re.escape(prefix) + r'_([^"/]+?)\.txt"', re.I
    )
    species = sorted({m.group(1) for m in pat.finditer(html)})
    if len(species) < 20:
        raise ValueError(
            f"{index_url}: enumerated only {len(species)} species (<20); "
            "directory listing format likely changed"
        )
    return species


def _parse_species_file(text: str, species: str) -> list:
    """Parse one fixed-width species summary file into long records.

    Returns list of (species, fire_type, region, year, value, unit) tuples.
    """
    unit = None
    years = None          # parsed once from the single 'Region <years> | Mean' header
    fire_type = None
    rows = []

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            m = _UNIT_RE.search(stripped)
            if m:
                unit = m.group(1).strip()
            continue
        if stripped.startswith("Region"):
            # The column header: tokens between 'Region' and '|' are the years.
            left = line.split("|", 1)[0]
            toks = left.split()
            years = [int(t) for t in toks[1:]]
            continue
        if stripped.endswith(":"):
            fire_type = stripped[:-1].strip()
            continue
        if "|" not in line:
            # Centered 'Year' caption / stray lines — not data.
            continue
        if years is None or fire_type is None:
            continue
        left = line.split("|", 1)[0]
        toks = left.split()
        region = toks[0]
        vals = toks[1:]
        if len(vals) != len(years):
            raise ValueError(
                f"{species}/{fire_type}/{region}: {len(vals)} values vs "
                f"{len(years)} year columns — fixed-width layout drift"
            )
        for yr, raw in zip(years, vals):
            try:
                value = float(raw)
            except ValueError:
                value = None
            rows.append((species, fire_type, region, yr, value, unit))

    if years is None:
        raise ValueError(f"{species}: no 'Region ... | Mean' header row found")
    return rows


def _fetch_release(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    cfg = SOURCES[node_id]
    species_list = _list_species(cfg["index_url"], cfg["prefix"])

    species_col, fire_col, region_col, year_col, value_col, unit_col = (
        [], [], [], [], [], [],
    )
    for species in species_list:
        url = f"{cfg['index_url']}{cfg['prefix']}_{species}.txt"
        text = _get_text(url)
        recs = _parse_species_file(text, species)
        if len(recs) < _MIN_ROWS_PER_SPECIES:
            raise ValueError(
                f"{url}: parsed only {len(recs)} rows (<{_MIN_ROWS_PER_SPECIES}); "
                "file layout likely changed"
            )
        for sp, ft, rg, yr, val, un in recs:
            species_col.append(sp)
            fire_col.append(ft)
            region_col.append(rg)
            year_col.append(yr)
            value_col.append(val)
            unit_col.append(un)

    table = pa.table(
        {
            "species": pa.array(species_col, pa.string()),
            "fire_type": pa.array(fire_col, pa.string()),
            "region": pa.array(region_col, pa.string()),
            "year": pa.array(year_col, pa.int32()),
            "value": pa.array(value_col, pa.float64()),
            "unit": pa.array(unit_col, pa.string()),
        },
        schema=SCHEMA,
    )
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="gfed-emissions-gfed5", fn=_fetch_release, kind="download"),
    NodeSpec(id="gfed-emissions-gfed4", fn=_fetch_release, kind="download"),
]

# Thin parse-and-type pass: raw is already long and clean. Drop the rare
# unparseable value, and dedup defensively on the natural key.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                species,
                fire_type,
                region,
                CAST(year AS INTEGER)  AS year,
                CAST(value AS DOUBLE)  AS value,
                unit
            FROM "{s.id}"
            WHERE value IS NOT NULL
            QUALIFY row_number() OVER (
                PARTITION BY species, fire_type, region, year
                ORDER BY value
            ) = 1
        ''',
    )
    for s in DOWNLOAD_SPECS
]
