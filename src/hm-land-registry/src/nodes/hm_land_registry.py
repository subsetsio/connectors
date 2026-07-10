"""HM Land Registry — download node module.

Three publishable assets, one DOWNLOAD_SPEC each:

- ``hm-land-registry-ppd`` — Price Paid Data microdata (property transactions).
  Fetched from the per-year bulk CSV files (pp-YYYY.csv, headerless, 16 fixed
  columns), one parquet *fragment* per year of the single logical asset, so the
  transform's dep view globs every year automatically. Per-year files keep peak
  memory bounded vs the 5.4GB pp-complete.csv.
- ``hm-land-registry-ukhpi`` — UK House Price Index monthly indicators. Regions
  are enumerated from SPARQL, each region's full monthly series is paged from
  the linked-data API and flattened (51 canonical measures), streamed to one
  ndjson.gz asset.
- ``hm-land-registry-ukhpi-regions`` — the region reference taxonomy (slug, uri,
  english name, admin-geo type) joinable to the UKHPI series via region_slug.

All three are stateless full re-pulls: the source republishes the whole corpus
monthly and exposes no incremental delta filter usable for our snapshot pattern.

Licence: Open Government Licence v3.0 (attribution required).
"""

from __future__ import annotations

import io
import json
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

_UKHPI_REGION_URL = "https://landregistry.data.gov.uk/data/ukhpi/region/{slug}.json"
_SPARQL_URL = "https://landregistry.data.gov.uk/landregistry/query"
_UKHPI_PAGE_SIZE = 500
_UKHPI_MAX_PAGES = 200  # safety ceiling per region (~700 records today)
_ADMINGEO = "http://data.ordnancesurvey.co.uk/ontology/admingeo/"

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


def _sparql(query: str) -> list[dict]:
    resp = request(
        _SPARQL_URL,
        params={"query": query},
        headers={"Accept": "application/sparql-results+json"},
        timeout=(10.0, 240.0),
    )
    return resp.json()["results"]["bindings"]


def _region_slugs() -> list[str]:
    bindings = _sparql(
        "PREFIX ukhpi: <http://landregistry.data.gov.uk/def/ukhpi/> "
        "SELECT DISTINCT ?r WHERE { ?o ukhpi:refRegion ?r } ORDER BY ?r"
    )
    slugs = [b["r"]["value"].rsplit("/", 1)[-1] for b in bindings]
    if len(slugs) < 300:
        raise RuntimeError(
            f"UKHPI: SPARQL returned only {len(slugs)} region slugs (expected >=300)"
            " — region enumeration broke"
        )
    return slugs


def _region_name(item: dict) -> str | None:
    rr = item.get("refRegion") or {}
    label = rr.get("label")
    if isinstance(label, list) and label:
        return label[0].get("_value")
    if isinstance(label, str):
        return label
    return None


def _region_rows(slug: str):
    """Yield flattened monthly rows for one region across all pages."""
    url = _UKHPI_REGION_URL.format(slug=slug)
    seen = 0
    for page in range(_UKHPI_MAX_PAGES):
        resp = request(
            url,
            params={"_view": "all", "_pageSize": _UKHPI_PAGE_SIZE, "_page": page},
            headers={"Accept": "application/json"},
            timeout=(10.0, 180.0),
        )
        result = resp.json()["result"]
        items = result.get("items", [])
        if not items:
            break
        total = result.get("totalResults")
        for it in items:
            ref_month = it.get("refMonth")
            row = {
                "region_slug": slug,
                "region_name": _region_name(it),
                "ref_month": ref_month,
                # Full-ISO month-start date: a stable temporal column the raw
                # freshness test can compare against `today - Nd` without the
                # length-mismatch that lexicographic "YYYY-MM" comparison hits.
                "ref_date": f"{ref_month}-01" if ref_month else None,
            }
            for m in _UKHPI_MEASURES:
                row[m] = it.get(m)
            yield row
        seen += len(items)
        if total is not None and seen >= total:
            break
    else:
        raise RuntimeError(
            f"UKHPI: region {slug!r} hit the {_UKHPI_MAX_PAGES}-page safety cap"
        )


def fetch_ukhpi(node_id: str) -> None:
    """Enumerate regions, page each region's monthly series, and stream all
    rows to one ndjson.gz asset (`hm-land-registry-ukhpi`)."""
    slugs = _region_slugs()
    asset = node_id  # "hm-land-registry-ukhpi"
    total_rows = 0
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as f:
        for slug in slugs:
            for row in _region_rows(slug):
                f.write(json.dumps(row) + "\n")
                total_rows += 1
    print(f"[ukhpi] {len(slugs)} regions, {total_rows} rows -> {asset}")
    if total_rows == 0:
        raise RuntimeError("UKHPI: wrote 0 rows — region API shape changed")


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
    """Fetch the UKHPI region reference: one row per region with its english
    label and admin-geo type(s). Enumerated from SPARQL over the same refRegion
    universe the UKHPI series uses, so region_slug reconciles 1:1."""
    bindings = _sparql(
        "PREFIX ukhpi: <http://landregistry.data.gov.uk/def/ukhpi/> "
        "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> "
        "SELECT ?r ?label ?type WHERE { "
        "  { SELECT DISTINCT ?r WHERE { ?o ukhpi:refRegion ?r } } "
        "  OPTIONAL { ?r rdfs:label ?label FILTER(lang(?label) = \"en\") } "
        f"  OPTIONAL {{ ?r a ?type FILTER(STRSTARTS(STR(?type), \"{_ADMINGEO}\")) }} "
        "}"
    )
    regions: dict[str, dict] = {}
    for b in bindings:
        uri = b["r"]["value"]
        slug = uri.rsplit("/", 1)[-1]
        d = regions.setdefault(slug, {"uri": uri, "labels": set(), "types": set()})
        if "label" in b:
            d["labels"].add(b["label"]["value"])
        if "type" in b:
            local = b["type"]["value"].rsplit("/", 1)[-1]
            if local:
                d["types"].add(local)

    if len(regions) < 300:
        raise RuntimeError(
            f"UKHPI regions: SPARQL returned only {len(regions)} regions "
            "(expected >=300) — region enumeration broke"
        )

    rows = []
    for slug in sorted(regions):
        d = regions[slug]
        rows.append({
            "region_slug": slug,
            "region_uri": d["uri"],
            "region_name": next(iter(sorted(d["labels"])), None),
            "region_type": "|".join(sorted(d["types"])),
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
