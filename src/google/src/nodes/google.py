"""Google connector — Community Mobility Reports.

Publishes the Google COVID-19 Community Mobility Reports: a global, daily
time series of percent-change-from-baseline mobility across six place
categories (retail/recreation, grocery/pharmacy, parks, transit stations,
workplaces, residential), broken down by country / sub_region_1 (state) /
sub_region_2 (county) / metro_area, from 2020-02-15 to 2022-10-15.

Mechanism (from research): bulk_download, no auth. A single global CSV at a
stable gstatic URL contains every region. The dataset is FROZEN — no longer
updated since 2022-10-15 — so every refresh re-fetches the same immutable URL
(stateless full re-pull; no watermark, no incremental filter exists).

The CSV is ~1.14 GB gzip-served (and decompresses to ~15 GB / ~130M rows), so
the download streams the response straight into a row-group-flushed parquet
writer without buffering the whole file in memory or on disk. Columns are kept
as raw strings in the parquet; the SQL transform does the date/number casting.

Other Google datasets considered but not published here: Google Books Ngrams
(cataloged but each per-(corpus, ngram-size) table is tens of GB to multiple
TB — incompatible with this CI-bound fetch+SQL pipeline) and the Google Trends
API (alpha/gated, no public access). See the source's research/collect assets.
"""

import io

import pyarrow as pa
import pyarrow.csv as pacsv

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get_client,
    raw_parquet_writer,
    transient_retry,
)

MOBILITY_URL = "https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv"

# Verified column order of the Global Mobility Report CSV header. Kept as
# strings in raw — the transform casts dates and the percent-change metrics.
MOBILITY_COLUMNS = [
    "country_region_code",
    "country_region",
    "sub_region_1",
    "sub_region_2",
    "metro_area",
    "iso_3166_2_code",
    "census_fips_code",
    "place_id",
    "date",
    "retail_and_recreation_percent_change_from_baseline",
    "grocery_and_pharmacy_percent_change_from_baseline",
    "parks_percent_change_from_baseline",
    "transit_stations_percent_change_from_baseline",
    "workplaces_percent_change_from_baseline",
    "residential_percent_change_from_baseline",
]

MOBILITY_SCHEMA = pa.schema([(c, pa.string()) for c in MOBILITY_COLUMNS])

_PARSE_BLOCK_SIZE = 32 << 20  # 32 MB read blocks -> bounded-memory batches


class _IterStream(io.RawIOBase):
    """Adapt an iterator of byte chunks into a sequential read-only file object.

    Lets pyarrow's CSV reader pull blocks straight from the streaming HTTP
    response (already content-decoded by httpx) without materializing the whole
    decompressed file.
    """

    def __init__(self, chunks):
        self._chunks = chunks
        self._buf = b""

    def readable(self):
        return True

    def readinto(self, b):
        while not self._buf:
            try:
                self._buf = next(self._chunks)
            except StopIteration:
                return 0
        n = min(len(b), len(self._buf))
        b[:n] = self._buf[:n]
        self._buf = self._buf[n:]
        return n


@transient_retry(attempts=5)
def _stream_csv_to_parquet(asset: str) -> int:
    """Stream the global CSV into a parquet asset; return rows written.

    Idempotent: each attempt opens a fresh parquet writer and overwrites, so a
    transient failure mid-stream is safe to retry from the start.
    """
    client = get_client()
    convert = pacsv.ConvertOptions(column_types={c: pa.string() for c in MOBILITY_COLUMNS})
    read_opts = pacsv.ReadOptions(block_size=_PARSE_BLOCK_SIZE)
    rows = 0
    with client.stream("GET", MOBILITY_URL, timeout=(10.0, 300.0)) as resp:
        resp.raise_for_status()
        reader = io.BufferedReader(_IterStream(resp.iter_bytes()), buffer_size=1 << 20)
        csv_reader = pacsv.open_csv(reader, read_options=read_opts, convert_options=convert)
        with raw_parquet_writer(asset, MOBILITY_SCHEMA) as writer:
            for batch in csv_reader:
                writer.write_batch(batch)
                rows += batch.num_rows
    if rows == 0:
        raise AssertionError(f"{asset}: mobility CSV parsed to 0 rows — format may have changed")
    return rows


def fetch_mobility(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    n = _stream_csv_to_parquet(asset)
    print(f"  {asset}: wrote {n} rows")


DOWNLOAD_SPECS = [
    NodeSpec(id="google-community-mobility-reports", fn=fetch_mobility, kind="download"),
]


_PCT_COLS = {
    "retail_and_recreation_percent_change_from_baseline": "retail_and_recreation_pct_change",
    "grocery_and_pharmacy_percent_change_from_baseline": "grocery_and_pharmacy_pct_change",
    "parks_percent_change_from_baseline": "parks_pct_change",
    "transit_stations_percent_change_from_baseline": "transit_stations_pct_change",
    "workplaces_percent_change_from_baseline": "workplaces_pct_change",
    "residential_percent_change_from_baseline": "residential_pct_change",
}

_PCT_SELECT = ",\n            ".join(
    f"TRY_CAST(NULLIF({src}, '') AS DOUBLE) AS {dst}" for src, dst in _PCT_COLS.items()
)

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="google-community-mobility-reports-transform",
        deps=["google-community-mobility-reports"],
        sql=f"""
            SELECT
                NULLIF(country_region_code, '') AS country_region_code,
                NULLIF(country_region, '')      AS country_region,
                NULLIF(sub_region_1, '')        AS sub_region_1,
                NULLIF(sub_region_2, '')        AS sub_region_2,
                NULLIF(metro_area, '')          AS metro_area,
                NULLIF(iso_3166_2_code, '')     AS iso_3166_2_code,
                NULLIF(census_fips_code, '')    AS census_fips_code,
                NULLIF(place_id, '')            AS place_id,
                CAST(date AS DATE)              AS date,
                {_PCT_SELECT}
            FROM "google-community-mobility-reports"
            WHERE date IS NOT NULL AND date <> ''
        """,
        temporal="date",
    ),
]
