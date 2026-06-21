"""HM Land Registry — UK House Price Index (UKHPI).

Monthly aggregate indicators per region. Region slugs are enumerated from the
SPARQL endpoint, then each region's full monthly series is paged from the
linked-data API and flattened (refRegion/label -> region_slug/region_name,
refMonth + the 51 canonical measures). Streamed to one ndjson.gz asset. A
stateless full re-pull (the source republishes the whole corpus monthly and
there is no usable incremental delta filter).

Licence: Open Government Licence v3.0 (attribution required).
"""

from __future__ import annotations

import json
import re

from subsets_utils import NodeSpec, SqlNodeSpec, raw_writer
from utils import request

# --------------------------------------------------------------------------- #
# Constants
# --------------------------------------------------------------------------- #

_UKHPI_REGION_URL = "https://landregistry.data.gov.uk/data/ukhpi/region/{slug}.json"
_SPARQL_URL = "https://landregistry.data.gov.uk/landregistry/query"
_UKHPI_PAGE_SIZE = 500
_UKHPI_MAX_PAGES = 200  # safety ceiling per region (~700 records today)

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


# --------------------------------------------------------------------------- #
# Fetch
# --------------------------------------------------------------------------- #

def _region_slugs() -> list[str]:
    query = (
        "PREFIX ukhpi: <http://landregistry.data.gov.uk/def/ukhpi/> "
        "SELECT DISTINCT ?r WHERE { ?o ukhpi:refRegion ?r } ORDER BY ?r"
    )
    resp = request(
        _SPARQL_URL,
        params={"query": query},
        headers={"Accept": "application/sparql-results+json"},
        timeout=(10.0, 180.0),
    )
    bindings = resp.json()["results"]["bindings"]
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
            row = {
                "region_slug": slug,
                "region_name": _region_name(it),
                "ref_month": it.get("refMonth"),
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
# Specs
# --------------------------------------------------------------------------- #

DOWNLOAD_SPECS = [
    NodeSpec(id="hm-land-registry-ukhpi", fn=fetch_ukhpi, kind="download"),
]


def _snake(camel: str) -> str:
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", camel).lower()


_UKHPI_MEASURE_SQL = ",\n        ".join(
    f'CAST("{m}" AS DOUBLE) AS {_snake(m)}' for m in _UKHPI_MEASURES
)

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="hm-land-registry-ukhpi-transform",
        deps=["hm-land-registry-ukhpi"],
        sql=f'''
        SELECT
            region_slug,
            region_name,
            strptime(ref_month, '%Y-%m')::DATE AS date,
            {_UKHPI_MEASURE_SQL}
        FROM "hm-land-registry-ukhpi"
        WHERE ref_month IS NOT NULL
        ''',
    ),
]
