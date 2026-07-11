"""Port of Los Angeles connector.

Source: City of Los Angeles Socrata portal (data.lacity.org). The Port of LA
publishes its statistical datasets there; each dataset is a stable 4x4 Socrata
resource id fetched via the SODA JSON endpoint
(https://data.lacity.org/resource/<id>.json).

Fetch shape: stateless full re-pull. Every dataset in scope is a small static
historical table (tens to ~100 rows), so each refresh re-pulls the whole table
in one paginated request and overwrites. No watermark/cursor - these tables no
longer update and full re-pull is trivially cheap. SODA returns every field as
a JSON string and some columns are sparsely populated, so raw is saved as NDJSON
and the transform SQL does the typing/casting.
"""

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_ndjson,
)

BASE = "https://data.lacity.org/resource"
PAGE_SIZE = 50000  # all datasets here are far smaller than one page

# The entity union - rank-active Port-of-LA datasets (Socrata 4x4 ids).
# Copied from data/sources/port-of-la/work/entity_union.json.
ENTITY_IDS = [
    "2t3h-my34",  # Emission from Port Operations (2005-2012)
    "38a8-tm7u",  # Historical TEU Statistics
    "5a4i-e2zs",  # Historic Tonnage Data Short Ton (1920-1970)
    "aiix-duyv",  # Emissions Reduction Percentage 2005-2012
    "b3i5-86hy",  # Port Air Quality (2006-2013)
    "du8q-hww5",  # Adopted Budget 2010-2014
    "geed-7eey",  # Film Permit Tracking 2014
    "gvpf-vb3s",  # Workers' Compensation Light Duty Hours
    "i9rh-q5gx",  # Historic Tonnage Data MMRT
    "jdgw-bwcf",  # Finance Annual Financial Report FY12-FY13
    "jmt8-y5rm",  # Cruise Passenger (1990-2014)
    "s2gq-nz3r",  # Workers' Compensation New Claims
    "s5jy-jcce",  # ADP Project
    "tsuv-4rgh",  # TEU Counts Monthly And Calendar YTD
    "v3my-p6u5",  # Workers' Compensation Benefits Expenditures
    "v7gk-cxxi",  # Quarterly Financial Statement 2013-2014
    "xhx7-hr4h",  # Single Audit Report 2013
]


def _fetch_page(resource_id: str, offset: int) -> list:
    url = f"{BASE}/{resource_id}.json"
    resp = get(
        url,
        params={"$limit": PAGE_SIZE, "$offset": offset, "$order": ":id"},
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    return resp.json()


def fetch_one(node_id: str) -> None:
    """Fetch a single Socrata dataset in full and save it as NDJSON.

    The runtime passes the spec id (e.g. 'port-of-la-tsuv-4rgh'); the asset name
    IS that id. Recover the Socrata resource id by stripping the slug prefix.
    """
    asset = node_id
    resource_id = node_id[len("port-of-la-"):]

    rows = []
    offset = 0
    while True:
        page = _fetch_page(resource_id, offset)
        rows.extend(page)
        if len(page) < PAGE_SIZE:
            break
        offset += PAGE_SIZE
        if offset > 5_000_000:  # safety ceiling - these tables are tiny
            raise RuntimeError(
                f"{resource_id}: exceeded {offset} rows; source grew unexpectedly"
            )

    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"port-of-la-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
