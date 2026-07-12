"""Global Lake & River Ice Phenology Database (NSIDC G01377).

The whole source is two stable, public CSV files under
https://noaadata.apps.nsidc.org/NOAA/G01377/ . Both are tiny (~3.2MB total),
so the fetch shape is the default stateless full re-pull: download each CSV in
full every run and overwrite. No incremental filter is exposed and none is
needed.

Raw is saved faithfully as NDJSON (every value a string, exactly as the CSV
delivers it); the missing-value sentinels the source uses (-999 for numerics,
'-' for text) are stripped and the columns typed in the transform SQL.
"""
import csv
import io

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

BASE = "https://noaadata.apps.nsidc.org/NOAA/G01377"

CSV_URLS = {
    "lake-river-ice-phenology-freeze-thaw": f"{BASE}/liag_freeze_thaw_table.csv",
    "lake-river-ice-phenology-physical-characteristics": f"{BASE}/liag_physical_character_table.csv",
}


@transient_retry()
def _fetch_csv_rows(url: str) -> list[dict]:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    text = resp.content.decode("utf-8-sig", errors="replace")
    reader = csv.DictReader(io.StringIO(text))
    return [dict(row) for row in reader]


def fetch_csv(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    url = CSV_URLS[node_id]
    rows = _fetch_csv_rows(url)
    if not rows:
        raise AssertionError(f"{node_id}: fetched 0 rows from {url}")
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="lake-river-ice-phenology-freeze-thaw", fn=fetch_csv, kind="download"),
    NodeSpec(id="lake-river-ice-phenology-physical-characteristics", fn=fetch_csv, kind="download"),
]
