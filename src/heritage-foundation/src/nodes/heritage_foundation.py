"""Heritage Foundation — Index of Economic Freedom.

Single product: an annual, country-level economic-freedom index. There is no
programmatic catalog and no single all-years file — the source publishes one
Excel workbook per edition (year). We fetch every reachable edition and melt
each one into a tidy long table.

The edition layout drifts across two methodologies, so the fetch fn does the
reconciliation (the SQL transform is a thin type/dedup pass):

  * pre-2017 editions (2009-2016) carry the old ~10 "freedoms" (Freedom from
    Corruption, Fiscal Freedom, Gov't Size, ...); 2009 has no Region column,
    and 2013-style files interleave "Change in X" columns we must skip.
  * 2017+ editions carry the modern 12 components (split into Tax Burden /
    Fiscal Health, Judicial Effectiveness, Government Integrity, ...).
  * 2024+ editions live on a different host (static.heritage.org, .xlsx with a
    one-row "COMPONENT SCORES" banner above the header) with drifting sheet
    names and header spellings ("Monitary", "Efect").

Rather than force every edition into one wide schema, we emit long rows keyed
(year, country, component): each component keeps its own canonical slug, so a
methodology change just means different components appear in different years —
no information is lost or mis-attributed. The overall index is component
"overall". Scores are 0-100.

Stateless full re-pull: the whole corpus is ~18 small workbooks (~40k rows),
so we re-fetch and overwrite every run; revisions are picked up for free.
"""

import io
import re
from datetime import datetime, timezone

import pandas as pd
import pyarrow as pa
from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet, transient_retry

# Earliest Index edition reachable via the mirrors (verified — 2008 and older
# 404 on both hosts). The upper bound is discovered dynamically per run; we
# probe each year and skip the ones that aren't published, so this is not a
# fixed range that would silently cap as new editions ship.
FIRST_EDITION = 2009

# Per-edition workbook URLs. 2024+ editions live on static.heritage.org; older
# editions on the legacy azure mirror. We try the current host first and fall
# back, so we never hardcode the boundary year.
STATIC_URL = "https://static.heritage.org/index/data/{y}/{y}_indexofeconomicfreedom_data.xlsx"
AZURE_URL = "https://indexdotnet.azurewebsites.net/index/excel/{y}/index{y}_data.xls"

RAW_SCHEMA = pa.schema([
    ("year", pa.int64()),
    ("country", pa.string()),
    ("region", pa.string()),
    ("component", pa.string()),
    ("score", pa.float64()),
])


def _normalize(value) -> str:
    """Lowercase a header cell down to space-separated alphanumerics."""
    return re.sub(r"[^a-z0-9]+", " ", str(value).lower()).strip()


def _classify_header(header) -> str | None:
    """Map a raw header cell to a canonical column role / component slug.

    Returns the sentinel "__country__"/"__region__" for the key columns, a
    component slug for a score column, or None for columns we drop (rank
    columns, ids, "Change in X" deltas, blank banner cells).
    """
    n = _normalize(header)
    if not n or n == "nan":
        return None
    if "change" in n:  # 2013-style "Change in X" delta columns
        return None
    if n in ("country", "country name"):
        return "__country__"
    if n == "region":
        return "__region__"
    if n in ("countryid", "country id", "webname", "web name",
             "world rank", "region rank", "rank", "year", "id"):
        return None
    # Overall index: "Overall Score", "2016 Score", "2009 Overall Score", "Score".
    if "overall" in n or n.endswith("score") or n.endswith(" score"):
        return "overall"
    if "property" in n:
        return "property_rights"
    if "judic" in n:                       # "Judicial Effectiveness", "Judical", "Judicial Efect"
        return "judicial_effectiveness"
    if "integrity" in n:                   # "Government Integrity"
        return "government_integrity"
    if "corruption" in n:                  # pre-2017 "Freedom from Corruption"
        return "freedom_from_corruption"
    if "tax" in n:                         # modern "Tax Burden"
        return "tax_burden"
    if "fiscal health" in n:               # modern "Fiscal Health"
        return "fiscal_health"
    if "fiscal" in n:                      # pre-2017 "Fiscal Freedom"
        return "fiscal_freedom"
    if "spending" in n:                    # modern "Government Spending"
        return "government_spending"
    if "gov" in n and "size" in n:         # pre-2017 "Gov't Size"
        return "government_size"
    if "business" in n:
        return "business_freedom"
    if "labor" in n or "labour" in n:
        return "labor_freedom"
    if "monetary" in n or "monitary" in n or "monet" in n:   # "Monitary" typo in 2026
        return "monetary_freedom"
    if "trade" in n:
        return "trade_freedom"
    if "invest" in n:
        return "investment_freedom"
    if "financ" in n:
        return "financial_freedom"
    return None


def _to_score(value):
    """Parse a score cell to float, mapping the various missing markers to None."""
    if value is None:
        return None
    s = str(value).strip().replace(",", "")
    if s in ("", "-", "nan", "NaN", "N/A", "NA", "n/a", "None"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _parse_edition(year: int, content: bytes, engine: str) -> list[dict]:
    """Melt one edition's workbook into long (year, country, region, component, score) rows."""
    raw = pd.read_excel(io.BytesIO(content), sheet_name=0, header=None, engine=engine)

    header_row = None
    for i in range(min(6, len(raw))):
        if _normalize(raw.iloc[i, 0]).startswith("country"):
            header_row = i
            break
    if header_row is None:
        raise RuntimeError(f"edition {year}: could not locate the header row")

    headers = raw.iloc[header_row].tolist()
    component_cols: dict[str, int] = {}
    country_col = None
    region_col = None
    for j, h in enumerate(headers):
        role = _classify_header(h)
        if role == "__country__":
            # Prefer an explicit "Country Name" over a bare "Country" id column.
            if country_col is None or _normalize(h) == "country name":
                country_col = j
        elif role == "__region__":
            region_col = j
        elif role:
            component_cols.setdefault(role, j)  # first matching column wins
    if country_col is None or not component_cols:
        raise RuntimeError(f"edition {year}: header had no country/component columns")

    rows: list[dict] = []
    for r in range(header_row + 1, len(raw)):
        country = raw.iloc[r, country_col]
        if pd.isna(country) or not str(country).strip():
            continue
        country = str(country).strip()
        # Skip non-country artifact rows: some editions (e.g. 2012) carry a
        # numeric column-index legend row right under the header, and footers
        # may carry notes. A real country name always has a letter.
        if not re.search(r"[A-Za-z]", country):
            continue
        region = None
        if region_col is not None:
            rv = raw.iloc[r, region_col]
            region = None if pd.isna(rv) else (str(rv).strip() or None)
        for component, j in component_cols.items():
            rows.append({
                "year": year,
                "country": country,
                "region": region,
                "component": component,
                "score": _to_score(raw.iloc[r, j]),
            })
    return rows


@transient_retry()
def _download(url: str) -> bytes | None:
    """GET a workbook. Returns None when the edition is not published at this
    host (404, or the static host's HTML SPA fallback), so the caller can fall
    back / skip. Transient 5xx/429/network errors are retried by the decorator."""
    resp = get(url, timeout=(10.0, 120.0))
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    if "html" in resp.headers.get("content-type", "").lower():
        return None
    return resp.content


def _fetch_edition(year: int):
    """Return (content, engine) for an edition, or None if not published anywhere."""
    content = _download(STATIC_URL.format(y=year))
    if content is not None:
        return content, "openpyxl"
    content = _download(AZURE_URL.format(y=year))
    if content is not None:
        return content, "xlrd"
    return None


def fetch_index(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    # Upper bound is dynamic — allow an edition named for next year (the source
    # publishes the next edition late in the prior calendar year).
    last_candidate = datetime.now(tz=timezone.utc).year + 1

    rows: list[dict] = []
    editions: list[int] = []
    for year in range(FIRST_EDITION, last_candidate + 1):
        got = _fetch_edition(year)
        if got is None:
            continue
        content, engine = got
        edition_rows = _parse_edition(year, content, engine)
        if not edition_rows:
            raise RuntimeError(f"edition {year}: downloaded a workbook but parsed 0 rows")
        rows.extend(edition_rows)
        editions.append(year)

    if not editions:
        raise RuntimeError(
            "no Index of Economic Freedom editions could be fetched from either host"
        )

    table = pa.Table.from_pylist(rows, schema=RAW_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="heritage-foundation-index-of-economic-freedom",
        fn=fetch_index,
        kind="download",
    ),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="heritage-foundation-index-of-economic-freedom-transform",
        deps=["heritage-foundation-index-of-economic-freedom"],
        sql='''
            SELECT
                CAST(year AS INTEGER) AS year,
                country,
                region,
                component,
                CAST(score AS DOUBLE) AS score
            FROM "heritage-foundation-index-of-economic-freedom"
            WHERE score IS NOT NULL
              AND country IS NOT NULL
              AND component IS NOT NULL
            QUALIFY row_number() OVER (
                PARTITION BY year, country, component ORDER BY score DESC
            ) = 1
        ''',
    ),
]
