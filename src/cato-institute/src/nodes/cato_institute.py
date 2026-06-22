"""Cato Institute — Human Freedom Index (HFI).

Single statistical dataset: a country-year panel co-published with the Fraser
Institute. The latest annual edition is a static CSV that contains the WHOLE
back-revised panel (2000-2023, ~165 jurisdictions, 155 columns: headline
hf_score/hf_rank/hf_quartile plus the personal-freedom (pf_*) and
economic-freedom (ef_*) sub-indicator hierarchies).

Fetch shape: stateless full re-pull. The file is a single static artefact with
no incremental/`since` filter and re-downloading it costs one ~3.7MB GET, so we
overwrite the whole panel each run — late methodology revisions are picked up
for free. URL stability is point-in-time (the filename embeds the edition year
and the naming convention has changed between editions), so the current
edition's URL is pinned here and updated when a new edition ships.
"""

import io

import pyarrow.csv as pacsv

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet, transient_retry

# Latest verified edition (2025 HFI, covering data through 2023). Pinned because
# the per-edition filename convention is not stable across editions.
HFI_CSV_URL = (
    "https://www.cato.org/sites/cato.org/files/"
    "human-freedom-index-files/2025-human-freedom-index-data.csv"
)


@transient_retry()
def _download_csv(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.content


def fetch_human_freedom_index(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    raw = _download_csv(HFI_CSV_URL)
    # Single full snapshot → safe to let pyarrow infer types in one pass
    # (year/ranks → int64, scores → double, iso/country/region → string).
    table = pacsv.read_csv(io.BytesIO(raw))
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="cato-institute-human-freedom-index",
        fn=fetch_human_freedom_index,
        kind="download",
    ),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="cato-institute-human-freedom-index-transform",
        deps=["cato-institute-human-freedom-index"],
        sql='''
            SELECT *
            FROM "cato-institute-human-freedom-index"
            WHERE iso IS NOT NULL
              AND year IS NOT NULL
        ''',
    ),
]
