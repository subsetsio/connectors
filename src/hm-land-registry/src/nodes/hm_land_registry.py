"""HM Land Registry — download node module.

Three publishable assets, one DOWNLOAD_SPEC each:

- ``hm-land-registry-ppd`` — Price Paid Data microdata (property transactions).
  Fetched from the per-year bulk CSV files (pp-YYYY.csv, headerless, 16 fixed
  columns), one parquet *fragment* per year of the single logical asset, so the
  transform's dep view globs every year automatically. Per-year files keep peak
  memory bounded vs the 5.4GB pp-complete.csv.
- ``hm-land-registry-ukhpi`` — UK House Price Index monthly indicators. The
  latest GOV.UK full-file CSV is discovered from the UKHPI reports collection
  and normalized into the same measure names exposed by the linked-data API,
  then streamed to one ndjson.gz asset.
- ``hm-land-registry-ukhpi-regions`` — the region reference taxonomy (slug, uri,
  english name, admin-geo type) joinable to the UKHPI series via region_slug.

All three are stateless full re-pulls: the source republishes the whole corpus
monthly and exposes no incremental delta filter usable for our snapshot pattern.

Licence: Open Government Licence v3.0 (attribution required).
"""

from __future__ import annotations

import csv
import html
import io
import json
import re
from datetime import datetime, timezone

import httpx
import pyarrow as pa
import pyarrow.csv as pacsv

from subsets_utils import NodeSpec, raw_parquet_writer, raw_writer, save_raw_parquet
from utils import request

# --------------------------------------------------------------------------- #
# Price Paid Data (PPD)
# --------------------------------------------------------------------------- #

# HTTP (not HTTPS) is required: this is an AWS S3 *website* endpoint, which has
# no TLS listener (https times out at the handshake). It is HM Land Registry's
# only published bulk-CSV host. Payload is public open data (OGL v3.0), so the
# lack of transport encryption carries no confidentiality risk.
_PPD_HOST = (
    "http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com"
)
# Per-year file URL template; the host 301-redirects to prod1.* (followed by
# subsets_utils.get).
_PPD_YEAR_URL = _PPD_HOST + "/pp-{year}.csv"
# Documented start of the dataset; the upper bound is discovered from the clock,
# and missing years (e.g. a not-yet-published current year) are skipped, so this
# is not a hardcoded literal range.
_PPD_MIN_YEAR = 1995

# Headerless CSV column order, per gov.uk/guidance/about-the-price-paid-data.
_PPD_COLS = [
    "transaction_id", "price", "date_of_transfer", "postcode", "property_type",
    "old_new", "duration", "paon", "saon", "street", "locality", "town_city",
    "district", "county", "ppd_category_type", "record_status",
]
# Read everything as text; the transform owns typing.
_PPD_SCHEMA = pa.schema([(c, pa.string()) for c in _PPD_COLS])


def fetch_ppd(node_id: str) -> None:
    """Fetch every per-year Price Paid CSV, one parquet fragment per year.

    Each year is written as ``fragment=<year>`` of the single logical asset
    ``node_id`` (``hm-land-registry-ppd``); the transform's dep view unions the
    fragments automatically.
    """
    current_year = datetime.now(tz=timezone.utc).year
    written = 0
    for year in range(_PPD_MIN_YEAR, current_year + 1):
        url = _PPD_YEAR_URL.format(year=year)
        try:
            resp = request(url, timeout=(10.0, 300.0))
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                # Year not (yet) published — a real gap, not an error.
                print(f"[ppd] {year}: 404, skipping")
                continue
            raise

        read_opts = pacsv.ReadOptions(
            column_names=_PPD_COLS,
            autogenerate_column_names=False,
            block_size=64 << 20,
        )
        conv_opts = pacsv.ConvertOptions(
            column_types={c: pa.string() for c in _PPD_COLS}
        )
        buf = io.BytesIO(resp.content)
        del resp  # free the ~150MB response body before parsing
        reader = pacsv.open_csv(buf, read_options=read_opts, convert_options=conv_opts)
        rows = 0
        with raw_parquet_writer(node_id, _PPD_SCHEMA, fragment=str(year)) as w:
            for batch in reader:
                if batch.num_rows:
                    w.write_batch(batch)
                    rows += batch.num_rows
        print(f"[ppd] {year}: {rows} rows -> {node_id}-{year}")
        written += 1

    if not written:
        raise RuntimeError(
            "PPD: no per-year files fetched — the bulk host or URL scheme changed"
        )


# --------------------------------------------------------------------------- #
# UK House Price Index (UKHPI)
# --------------------------------------------------------------------------- #

_UKHPI_COLLECTION_API = (
    "https://www.gov.uk/api/content/government/collections/uk-house-price-index-reports"
)
_UKHPI_FULL_FILE_RE = re.compile(
    r"https://publicdata\.landregistry\.gov\.uk/[^\"' <]+"
    r"UK-HPI-full-file-[^\"' <]+\.csv[^\"' <]*"
)
_ONS_GEOGRAPHY_URI = "https://statistics.data.gov.uk/id/statistical-geography/{code}"

# The 51 canonical UKHPI measures (union across regions). Every row is filled
# with all of them (null when a region lacks one) so the raw schema is stable.
_UKHPI_MEASURES = [
    "averagePrice", "averagePriceCash", "averagePriceDetached",
    "averagePriceExistingProperty", "averagePriceFirstTimeBuyer",
    "averagePriceFlatMaisonette", "averagePriceFormerOwnerOccupier",
    "averagePriceMortgage", "averagePriceNewBuild", "averagePriceSA",
    "averagePriceSemiDetached", "averagePriceTerraced",
    "housePriceIndex", "housePriceIndexCash", "housePriceIndexDetached",
    "housePriceIndexExistingProperty", "housePriceIndexFirstTimeBuyer",
    "housePriceIndexFlatMaisonette", "housePriceIndexFormerOwnerOccupier",
    "housePriceIndexMortgage", "housePriceIndexNewBuild", "housePriceIndexSA",
    "housePriceIndexSemiDetached", "housePriceIndexTerraced",
    "percentageAnnualChange", "percentageAnnualChangeCash",
    "percentageAnnualChangeDetached", "percentageAnnualChangeExistingProperty",
    "percentageAnnualChangeFirstTimeBuyer", "percentageAnnualChangeFlatMaisonette",
    "percentageAnnualChangeFormerOwnerOccupier", "percentageAnnualChangeMortgage",
    "percentageAnnualChangeNewBuild", "percentageAnnualChangeSemiDetached",
    "percentageAnnualChangeTerraced",
    "percentageChange", "percentageChangeCash", "percentageChangeDetached",
    "percentageChangeExistingProperty", "percentageChangeFirstTimeBuyer",
    "percentageChangeFlatMaisonette", "percentageChangeFormerOwnerOccupier",
    "percentageChangeMortgage", "percentageChangeNewBuild",
    "percentageChangeSemiDetached", "percentageChangeTerraced",
    "salesVolume", "salesVolumeCash", "salesVolumeExistingProperty",
    "salesVolumeMortgage", "salesVolumeNewBuild",
]


_UKHPI_CSV_MAP = {
    "AveragePrice": "averagePrice",
    "AveragePriceSA": "averagePriceSA",
    "DetachedPrice": "averagePriceDetached",
    "SemiDetachedPrice": "averagePriceSemiDetached",
    "TerracedPrice": "averagePriceTerraced",
    "FlatPrice": "averagePriceFlatMaisonette",
    "CashPrice": "averagePriceCash",
    "MortgagePrice": "averagePriceMortgage",
    "FTBPrice": "averagePriceFirstTimeBuyer",
    "FOOPrice": "averagePriceFormerOwnerOccupier",
    "NewPrice": "averagePriceNewBuild",
    "OldPrice": "averagePriceExistingProperty",
    "Index": "housePriceIndex",
    "IndexSA": "housePriceIndexSA",
    "DetachedIndex": "housePriceIndexDetached",
    "SemiDetachedIndex": "housePriceIndexSemiDetached",
    "TerracedIndex": "housePriceIndexTerraced",
    "FlatIndex": "housePriceIndexFlatMaisonette",
    "CashIndex": "housePriceIndexCash",
    "MortgageIndex": "housePriceIndexMortgage",
    "FTBIndex": "housePriceIndexFirstTimeBuyer",
    "FOOIndex": "housePriceIndexFormerOwnerOccupier",
    "NewIndex": "housePriceIndexNewBuild",
    "OldIndex": "housePriceIndexExistingProperty",
    "1m%Change": "percentageChange",
    "Detached1m%Change": "percentageChangeDetached",
    "SemiDetached1m%Change": "percentageChangeSemiDetached",
    "Terraced1m%Change": "percentageChangeTerraced",
    "Flat1m%Change": "percentageChangeFlatMaisonette",
    "Cash1m%Change": "percentageChangeCash",
    "Mortgage1m%Change": "percentageChangeMortgage",
    "FTB1m%Change": "percentageChangeFirstTimeBuyer",
    "FOO1m%Change": "percentageChangeFormerOwnerOccupier",
    "New1m%Change": "percentageChangeNewBuild",
    "Old1m%Change": "percentageChangeExistingProperty",
    "12m%Change": "percentageAnnualChange",
    "Detached12m%Change": "percentageAnnualChangeDetached",
    "SemiDetached12m%Change": "percentageAnnualChangeSemiDetached",
    "Terraced12m%Change": "percentageAnnualChangeTerraced",
    "Flat12m%Change": "percentageAnnualChangeFlatMaisonette",
    "Cash12m%Change": "percentageAnnualChangeCash",
    "Mortgage12m%Change": "percentageAnnualChangeMortgage",
    "FTB12m%Change": "percentageAnnualChangeFirstTimeBuyer",
    "FOO12m%Change": "percentageAnnualChangeFormerOwnerOccupier",
    "New12m%Change": "percentageAnnualChangeNewBuild",
    "Old12m%Change": "percentageAnnualChangeExistingProperty",
    "SalesVolume": "salesVolume",
    "CashSalesVolume": "salesVolumeCash",
    "MortgageSalesVolume": "salesVolumeMortgage",
    "NewSalesVolume": "salesVolumeNewBuild",
    "OldSalesVolume": "salesVolumeExistingProperty",
}


def _latest_ukhpi_full_file_url() -> str:
    collection = request(
        _UKHPI_COLLECTION_API,
        headers={"Accept": "application/json"},
        timeout=(10.0, 60.0),
    ).json()
    documents = collection.get("links", {}).get("documents", [])
    data_docs = [
        d for d in documents
        if "data downloads" in d.get("title", "").lower() and d.get("api_url")
    ]
    if not data_docs:
        raise RuntimeError("UKHPI: GOV.UK reports collection has no data-download document")
    data_docs.sort(key=lambda d: d.get("public_updated_at", ""), reverse=True)

    report = request(
        data_docs[0]["api_url"],
        headers={"Accept": "application/json"},
        timeout=(10.0, 60.0),
    ).json()
    body = html.unescape(report.get("details", {}).get("body", ""))
    match = _UKHPI_FULL_FILE_RE.search(body)
    if not match:
        raise RuntimeError(
            f"UKHPI: latest data-download page {data_docs[0]['api_url']} "
            "has no full-file CSV link"
        )
    return match.group(0).split("?", 1)[0]


def _csv_number(value: str | None) -> int | float | None:
    if value is None:
        return None
    value = value.strip().replace(",", "")
    if not value:
        return None
    number = float(value)
    return int(number) if number.is_integer() else number


def _ukhpi_rows_from_csv(text: str):
    for item in csv.DictReader(io.StringIO(text)):
        date = datetime.strptime(item["Date"], "%d/%m/%Y").date()
        ref_month = date.strftime("%Y-%m")
        row = {
            "region_slug": item["AreaCode"],
            "region_name": item["RegionName"],
            "ref_month": ref_month,
            # Full-ISO month-start date: a stable temporal column the raw
            # freshness test can compare against `today - Nd` without the
            # length-mismatch that lexicographic "YYYY-MM" comparison hits.
            "ref_date": date.isoformat(),
        }
        for measure in _UKHPI_MEASURES:
            row[measure] = None
        for source_col, measure in _UKHPI_CSV_MAP.items():
            row[measure] = _csv_number(item.get(source_col))
        yield row


def fetch_ukhpi(node_id: str) -> None:
    """Fetch the GOV.UK full-file CSV and stream monthly rows to ndjson.gz."""
    url = _latest_ukhpi_full_file_url()
    resp = request(url, timeout=(10.0, 180.0))
    total_rows = 0
    regions: set[str] = set()
    with raw_writer(node_id, "ndjson.gz", mode="wt", compression="gzip") as f:
        for row in _ukhpi_rows_from_csv(resp.text):
            regions.add(row["region_slug"])
            f.write(json.dumps(row) + "\n")
            total_rows += 1
    print(f"[ukhpi] {len(regions)} regions, {total_rows} rows from {url} -> {node_id}")
    if total_rows == 0:
        raise RuntimeError("UKHPI: wrote 0 rows — GOV.UK full-file CSV shape changed")


# --------------------------------------------------------------------------- #
# UKHPI region reference taxonomy
# --------------------------------------------------------------------------- #

_REGIONS_SCHEMA = pa.schema([
    ("region_slug", pa.string()),
    ("region_uri", pa.string()),
    ("region_name", pa.string()),
    ("region_type", pa.string()),  # "|"-joined admin-geo types; "" if none
])


def fetch_ukhpi_regions(node_id: str) -> None:
    """Build the UKHPI region reference from the same full-file CSV."""
    url = _latest_ukhpi_full_file_url()
    resp = request(url, timeout=(10.0, 180.0))
    regions: dict[str, str] = {}
    for item in csv.DictReader(io.StringIO(resp.text)):
        regions[item["AreaCode"]] = item["RegionName"]

    if len(regions) < 300:
        raise RuntimeError(
            f"UKHPI regions: full-file CSV returned only {len(regions)} regions "
            "(expected >=300) — region enumeration broke"
        )

    rows = []
    for code, name in sorted(regions.items()):
        rows.append({
            "region_slug": code,
            "region_uri": _ONS_GEOGRAPHY_URI.format(code=code),
            "region_name": name,
            "region_type": "",
        })
    table = pa.Table.from_pylist(rows, schema=_REGIONS_SCHEMA)
    save_raw_parquet(table, node_id)
    print(f"[ukhpi-regions] {len(rows)} regions -> {node_id}")


# --------------------------------------------------------------------------- #
# Specs
# --------------------------------------------------------------------------- #

DOWNLOAD_SPECS = [
    NodeSpec(id="hm-land-registry-ppd", fn=fetch_ppd, kind="download"),
    NodeSpec(id="hm-land-registry-ukhpi", fn=fetch_ukhpi, kind="download"),
    NodeSpec(id="hm-land-registry-ukhpi-regions", fn=fetch_ukhpi_regions, kind="download"),
]
