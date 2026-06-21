"""Apartment List — rental-market data products.

Apartment List publishes six monthly rental-market data products as CSVs on the
Contentful CDN. We discover each product's current edition through the Contentful
Content Delivery API (the read-only public token the live apartmentlist.com site
itself uses) and fetch the CSV from assets.ctfassets.net — both hosts are outside
the Cloudflare/JS gate that fronts www.apartmentlist.com, so no headless browser
is needed.

Five of the six products are wide history tables (one row per location[, bed_size];
one column per YYYY_MM). We melt them to a stable long schema at download time
(location dims + month date + value), so a new month adds rows, not columns. The
sixth (Rent Estimates Summary) is a flat current-month snapshot kept as-is.
"""

import csv
import datetime as dt
import io
import re

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

_CDA = "https://cdn.contentful.com/spaces/jeox55pd4d8n/environments/master/assets"
# Read-only Contentful delivery token, published verbatim in apartmentlist.com's
# page source (a CDA token is designed to be public). Discovery-only.
_TOKEN = "hNMmLWgHrS0Jk4eoSMvFwqTmh_ru53x8EvoHWIfT_2I"

_MONTH_COL = re.compile(r"^\d{4}_\d{2}$")

# Spec id -> product config.
#   title:  Contentful fields.title[match] term
#   prefix: canonical fileName prefix (the title match is broad; e.g. the
#           "Rent Estimates" match also returns the "Summary" assets)
#   has_bed_size: only Rent Estimates carries a bed_size dimension
_WIDE = {
    "apartment-list-rent-estimates": {
        "title": "Apartment List Rent Estimates",
        "prefix": "Apartment_List_Rent_Estimates_2",
        "has_bed_size": True,
    },
    "apartment-list-vacancy-index": {
        "title": "Apartment List Vacancy Index",
        "prefix": "Apartment_List_Vacancy_Index_",
        "has_bed_size": False,
    },
    "apartment-list-time-on-market": {
        "title": "Apartment List Time On Market",
        "prefix": "Apartment_List_Time_On_Market_",
        "has_bed_size": False,
    },
    "apartment-list-rent-growth-yoy": {
        "title": "Apartment List Rent Growth YoY",
        "prefix": "Apartment_List_Rent_Growth_YoY_",
        "has_bed_size": False,
    },
    "apartment-list-rent-growth-mom": {
        "title": "Apartment List Rent Growth MoM",
        "prefix": "Apartment_List_Rent_Growth_MoM_",
        "has_bed_size": False,
    },
}

_SUMMARY = {
    "apartment-list-rent-estimates-summary": {
        "title": "Apartment List Rent Estimates Summary",
        "prefix": "Apartment_List_Rent_Estimates_Summary_",
    },
}


@transient_retry()
def _discover_csv_url(title: str, prefix: str) -> str:
    """Return the https CSV url of the most-recent edition for a product.

    Query the CDA for the product's title, newest first, and take the first item
    whose fileName matches the canonical prefix (the title match is broad). The
    asset url is protocol-relative ('//assets.ctfassets.net/...') — prepend https.
    """
    resp = get(
        _CDA,
        params={
            "access_token": _TOKEN,
            "fields.title[match]": title,
            "order": "-sys.createdAt",
            "limit": 1000,
        },
        timeout=120,
    )
    resp.raise_for_status()
    for item in resp.json().get("items", []):
        f = item.get("fields", {}).get("file", {})
        fn = f.get("fileName", "")
        url = f.get("url", "")
        if fn.startswith(prefix) and url:
            return "https:" + url if url.startswith("//") else url
    raise RuntimeError(f"no Contentful asset matched prefix {prefix!r} for {title!r}")


@transient_retry()
def _download_csv(url: str) -> list[dict]:
    resp = get(url, timeout=180)
    resp.raise_for_status()
    text = resp.content.decode("utf-8-sig")
    return list(csv.DictReader(io.StringIO(text)))


def _na(v):
    """Source uses the literal 'NA' (and occasionally blanks) for null."""
    if v is None:
        return None
    v = v.strip()
    return None if v in ("", "NA") else v


def _int(v):
    v = _na(v)
    if v is None:
        return None
    try:
        return int(float(v))
    except ValueError:
        return None


def _float(v):
    v = _na(v)
    if v is None:
        return None
    try:
        return float(v)
    except ValueError:
        return None


def _dims(row: dict, has_bed_size: bool) -> dict:
    d = {
        "location_name": _na(row.get("location_name")),
        "location_type": _na(row.get("location_type")),
        "location_fips_code": _na(row.get("location_fips_code")),
        "population": _int(row.get("population")),
        "state": _na(row.get("state")),
        "county": _na(row.get("county")),
        "metro": _na(row.get("metro")),
    }
    if has_bed_size:
        d["bed_size"] = _na(row.get("bed_size"))
    return d


def _wide_schema(has_bed_size: bool) -> pa.Schema:
    fields = [
        ("location_name", pa.string()),
        ("location_type", pa.string()),
        ("location_fips_code", pa.string()),
        ("population", pa.int64()),
        ("state", pa.string()),
        ("county", pa.string()),
        ("metro", pa.string()),
    ]
    if has_bed_size:
        fields.append(("bed_size", pa.string()))
    fields += [("month", pa.date32()), ("value", pa.float64())]
    return pa.schema(fields)


def fetch_wide_history(node_id: str) -> None:
    """Discover + download a wide-history product CSV and melt it to long rows
    (one row per location[, bed_size] × month), skipping NA cells."""
    cfg = _WIDE[node_id]
    rows = _download_csv(_discover_csv_url(cfg["title"], cfg["prefix"]))
    if not rows:
        raise RuntimeError(f"{node_id}: source CSV had 0 rows")
    month_cols = [c for c in rows[0] if _MONTH_COL.match(c)]
    if not month_cols:
        raise RuntimeError(f"{node_id}: no YYYY_MM value columns found in header")
    has_bed = cfg["has_bed_size"]
    out = []
    for row in rows:
        base = _dims(row, has_bed)
        for col in month_cols:
            val = _float(row.get(col))
            if val is None:
                continue
            y, m = col.split("_")
            rec = dict(base)
            rec["month"] = dt.date(int(y), int(m), 1)
            rec["value"] = val
            out.append(rec)
    if not out:
        raise RuntimeError(f"{node_id}: melt produced 0 valued rows")
    table = pa.Table.from_pylist(out, schema=_wide_schema(has_bed))
    save_raw_parquet(table, node_id)


_SUMMARY_SCHEMA = pa.schema(
    [
        ("location_name", pa.string()),
        ("location_type", pa.string()),
        ("location_fips_code", pa.string()),
        ("population", pa.int64()),
        ("state", pa.string()),
        ("county", pa.string()),
        ("metro", pa.string()),
        ("year", pa.int64()),
        ("month", pa.int64()),
        ("rent_change_mom", pa.float64()),
        ("rent_change_yoy", pa.float64()),
        ("price_overall", pa.float64()),
        ("price_1br", pa.float64()),
        ("price_2br", pa.float64()),
    ]
)


def fetch_summary(node_id: str) -> None:
    """Discover + download the flat current-month Summary snapshot (one row per
    location: latest level + MoM/YoY change)."""
    cfg = _SUMMARY[node_id]
    rows = _download_csv(_discover_csv_url(cfg["title"], cfg["prefix"]))
    if not rows:
        raise RuntimeError(f"{node_id}: source CSV had 0 rows")
    out = []
    for row in rows:
        rec = _dims(row, has_bed_size=False)
        rec.update(
            {
                "year": _int(row.get("year")),
                "month": _int(row.get("month")),
                "rent_change_mom": _float(row.get("rent_change_mom")),
                "rent_change_yoy": _float(row.get("rent_change_yoy")),
                "price_overall": _float(row.get("price_overall")),
                "price_1br": _float(row.get("price_1br")),
                "price_2br": _float(row.get("price_2br")),
            }
        )
        out.append(rec)
    table = pa.Table.from_pylist(out, schema=_SUMMARY_SCHEMA)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="apartment-list-rent-estimates", fn=fetch_wide_history, kind="download"),
    NodeSpec(id="apartment-list-vacancy-index", fn=fetch_wide_history, kind="download"),
    NodeSpec(id="apartment-list-time-on-market", fn=fetch_wide_history, kind="download"),
    NodeSpec(id="apartment-list-rent-growth-yoy", fn=fetch_wide_history, kind="download"),
    NodeSpec(id="apartment-list-rent-growth-mom", fn=fetch_wide_history, kind="download"),
    NodeSpec(id="apartment-list-rent-estimates-summary", fn=fetch_summary, kind="download"),
]


# Common dimension projection shared by the five wide-history transforms. The
# month column is already a DATE; we only rename `value` to a product-specific,
# correctly-typed measure and drop any residual nulls.
_WIDE_DIMS = (
    "location_name, location_type, location_fips_code, population, "
    "state, county, metro"
)


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="apartment-list-rent-estimates-transform",
        deps=["apartment-list-rent-estimates"],
        sql=f'''
            SELECT {_WIDE_DIMS}, bed_size,
                   month AS date,
                   CAST(value AS INTEGER) AS rent_usd
            FROM "apartment-list-rent-estimates"
            WHERE value IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="apartment-list-vacancy-index-transform",
        deps=["apartment-list-vacancy-index"],
        sql=f'''
            SELECT {_WIDE_DIMS},
                   month AS date,
                   value AS vacancy_rate
            FROM "apartment-list-vacancy-index"
            WHERE value IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="apartment-list-time-on-market-transform",
        deps=["apartment-list-time-on-market"],
        sql=f'''
            SELECT {_WIDE_DIMS},
                   month AS date,
                   value AS days_on_market
            FROM "apartment-list-time-on-market"
            WHERE value IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="apartment-list-rent-growth-yoy-transform",
        deps=["apartment-list-rent-growth-yoy"],
        sql=f'''
            SELECT {_WIDE_DIMS},
                   month AS date,
                   value AS rent_growth_yoy
            FROM "apartment-list-rent-growth-yoy"
            WHERE value IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="apartment-list-rent-growth-mom-transform",
        deps=["apartment-list-rent-growth-mom"],
        sql=f'''
            SELECT {_WIDE_DIMS},
                   month AS date,
                   value AS rent_growth_mom
            FROM "apartment-list-rent-growth-mom"
            WHERE value IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="apartment-list-rent-estimates-summary-transform",
        deps=["apartment-list-rent-estimates-summary"],
        sql=f'''
            SELECT {_WIDE_DIMS},
                   make_date(year, month, 1) AS date,
                   rent_change_mom,
                   rent_change_yoy,
                   CAST(price_overall AS INTEGER) AS price_overall,
                   CAST(price_1br AS INTEGER)     AS price_1br,
                   CAST(price_2br AS INTEGER)     AS price_2br
            FROM "apartment-list-rent-estimates-summary"
            WHERE year IS NOT NULL AND month IS NOT NULL
        ''',
    ),
]
