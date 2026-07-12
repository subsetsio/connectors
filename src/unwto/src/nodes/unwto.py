"""UN Tourism (UNWTO) — international tourism arrivals and expenditure by country.

Source: UN Statistics Division's Statistical Yearbook (SYB) mirror of the UNWTO
World Tourism Organization tourism database, table 176. A single bulk CSV holds
the full country x year corpus for two series: tourist/visitor arrivals
(thousands) and inbound tourism expenditure (millions of US dollars).

Strategy: stateless full re-pull (shape 1). The CSV is a complete snapshot of the
current SYB edition (~420KB, ~2150 rows), re-fetched in full each refresh; there
is no incremental query and the file is cheap to pull whole. The download parses
the CSV into a clean long-format parquet (one row per country x year x series);
the SQL transform pivots the two series into one wide published table.

URL caveat: the filename embeds the SYB edition number (SYB67) and a YYYYMM
release stamp that change with each annual release (~Q4). Bump TOURISM_URL when a
new edition lands — the data.un.org SYB directory is the stable anchor.
"""

import csv
import io

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_parquet,
)

# Current SYB edition (SYB68 = 2025 edition, released 2025-11). Bump yearly.
TOURISM_URL = (
    "https://data.un.org/_Docs/SYB/CSV/"
    "SYB68_176_202511_Tourist-Visitors%20Arrival%20and%20Expenditure.csv"
)

# Long-format raw schema — one row per country x year x series.
SCHEMA = pa.schema([
    ("country_code", pa.int32()),
    ("country", pa.string()),
    ("year", pa.int32()),
    ("series", pa.string()),          # 'arrivals' | 'expenditure'
    ("arrivals_type", pa.string()),   # TF/VF/THS/TCE; null for expenditure
    ("value", pa.float64()),
])


def _fetch_csv(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


def _parse_value(raw: str) -> float | None:
    raw = (raw or "").strip()
    if not raw:
        return None
    return float(raw.replace(",", ""))


def fetch_tourism(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    text = _fetch_csv(TOURISM_URL)

    # The first physical line is a human title banner ("T31,Tourist/visitor
    # arrivals..."); the real CSV header is line 2. The country-name column has
    # an EMPTY header (second column). Strip the banner, then DictReader.
    lines = text.split("\n")
    reader = csv.DictReader(io.StringIO("\n".join(lines[1:])))

    country_codes: list[int] = []
    countries: list[str] = []
    years: list[int] = []
    series_norm: list[str] = []
    arr_types: list[str | None] = []
    values: list[float | None] = []

    for row in reader:
        code = (row.get("Region/Country/Area") or "").strip()
        name = (row.get("") or "").strip()
        year = (row.get("Year") or "").strip()
        series = (row.get("Series") or "").strip()
        if not code or not year:
            continue

        s = series.lower()
        if "arrivals" in s:
            norm = "arrivals"
            arr_type = (row.get("Tourism arrivals series type") or "").strip() or None
        elif "expenditure" in s:
            norm = "expenditure"
            arr_type = None
        else:
            # Unknown series value — surface it as a bug rather than silently drop.
            raise ValueError(f"unexpected Series value: {series!r}")

        country_codes.append(int(code))
        countries.append(name)
        years.append(int(year))
        series_norm.append(norm)
        arr_types.append(arr_type)
        values.append(_parse_value(row.get("Value", "")))

    table = pa.table(
        {
            "country_code": country_codes,
            "country": countries,
            "year": years,
            "series": series_norm,
            "arrivals_type": arr_types,
            "value": values,
        },
        schema=SCHEMA,
    )
    save_raw_parquet(table, asset)
    print(f"{asset}: parsed {len(table):,} long-format rows")


DOWNLOAD_SPECS = [
    NodeSpec(
        id="unwto-tourism-arrivals-expenditure",
        fn=fetch_tourism,
        kind="download",
    ),
]
