"""CRU (Climatic Research Unit, UEA) connector.

Publishes one subset: `cru-country-values` — the CRU CY country climate
averages. These are national spatial averages of the CRU TS 0.5deg gridded
fields, distributed as small fixed-width `.per` text files, one per
(variable, country) under
  https://crudata.uea.ac.uk/cru/.../crucy.<run>.v4.09/countries/<var>/

Shape = stateless full re-pull. The whole CY corpus is ~2,900 small text files
(~10 variables x ~292 countries/territories, ~17 KB each) and re-fetches in a
few minutes, so there is no watermark/cursor — we crawl the directory indexes
each run and overwrite. New CRU TS versions (e.g. 4.10) appear at a new
version-stamped path; the version dir is pinned here and bumped deliberately
when CRU releases (re-discovering it dynamically risks silently switching
datasets mid-series).

Each `.per` file: 3 header lines (provenance; country/parameter/units; period +
missing value -999.0), one header row (YEAR JAN..DEC MAM JJA SON DJF ANN), then
one row per year 1901-2024. We explode it to long format: one row per
(country, variable, year, period). Missing values (-999.0) are dropped.

Open Government Licence v3.0 — Climatic Research Unit (University of East Anglia).
"""

import re

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_parquet_writer,
    transient_retry,
)

# CRU TS / CY version dir — pinned deliberately (bump on a new CRU release).
CY_BASE = (
    "https://crudata.uea.ac.uk/cru/data/hrg/cru_ts_4.09/"
    "crucy.2503061057.v4.09/countries"
)

# The 10 CRU TS / CY variable directory codes.
VAR_CODES = ["cld", "dtr", "frs", "pet", "pre", "tmn", "tmp", "tmx", "vap", "wet"]

MISSING = -999.0

SCHEMA = pa.schema([
    ("country", pa.string()),
    ("variable", pa.string()),
    ("parameter", pa.string()),
    ("units", pa.string()),
    ("year", pa.int32()),
    ("period", pa.string()),
    ("value", pa.float64()),
])


@transient_retry(min_wait=2, max_wait=60)
def _fetch_text(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    # .per files are latin-1 fixed-width ASCII; decode defensively.
    return resp.content.decode("latin-1", "replace")


def _list_per_files(var: str) -> list[str]:
    """Filenames of the .per files listed in a variable's directory index."""
    html = _fetch_text(f"{CY_BASE}/{var}/")
    files = re.findall(r'href="(crucy\.[^"]+\.per)"', html)
    if not files:
        raise RuntimeError(f"variable dir {var}: no .per files found in index")
    return files


def _parse_per(text: str, var: str) -> list[dict]:
    """Explode one .per file into long-format rows; drop missing values."""
    lines = text.splitlines()
    country, parameter, units = None, None, None
    for line in lines[:3]:
        low = line.lower()
        # Per-country files say "parameter ="; the global "all" land-average
        # file capitalises it ("Parameter ="), so match case-insensitively.
        if "parameter" in low and "units" in low:
            for part in line.split(":"):
                part = part.strip()
                if part.lower().startswith("country"):
                    country = part.split("=", 1)[1].strip()
                elif part.lower().startswith("parameter"):
                    parameter = part.split("=", 1)[1].strip()
                elif part.lower().startswith("units"):
                    units = part.split("=", 1)[1].strip()
            break
    if not country:
        raise RuntimeError(f"{var}: could not parse country/parameter header")

    hdr_idx = next(i for i, l in enumerate(lines) if l.strip().startswith("YEAR"))
    periods = lines[hdr_idx].split()[1:]  # JAN..DEC MAM JJA SON DJF ANN

    rows = []
    for line in lines[hdr_idx + 1:]:
        fields = line.split()
        if not fields:
            continue
        year = int(fields[0])
        values = fields[1:]
        if len(values) != len(periods):
            raise RuntimeError(
                f"{var}/{country} {year}: {len(values)} values, expected {len(periods)}"
            )
        for period, raw in zip(periods, values):
            val = float(raw)
            if val == MISSING:
                continue
            rows.append({
                "country": country,
                "variable": var,
                "parameter": parameter,
                "units": units,
                "year": year,
                "period": period,
                "value": val,
            })
    return rows


def fetch_country_values(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    with raw_parquet_writer(asset, SCHEMA) as writer:
        for var in VAR_CODES:
            files = _list_per_files(var)
            batch = []
            for fname in files:
                text = _fetch_text(f"{CY_BASE}/{var}/{fname}")
                batch.extend(_parse_per(text, var))
            if not batch:
                raise RuntimeError(f"variable {var}: parsed 0 rows from {len(files)} files")
            writer.write_table(pa.Table.from_pylist(batch, schema=SCHEMA))


DOWNLOAD_SPECS = [
    NodeSpec(id="cru-country-values", fn=fetch_country_values, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="cru-country-values-transform",
        deps=["cru-country-values"],
        sql='''
            SELECT
                country,
                variable,
                parameter,
                units,
                CAST(year AS INTEGER) AS year,
                period,
                CAST(value AS DOUBLE) AS value
            FROM "cru-country-values"
            WHERE value IS NOT NULL
        ''',
        key=("country", "variable", "year", "period"),
        temporal="year",
    ),
]
