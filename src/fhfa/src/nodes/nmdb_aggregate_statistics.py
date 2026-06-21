"""NMDB Aggregate Statistics — combined outstanding-mortgage zip -> one CSV."""

from __future__ import annotations

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet

from utils import _csv_bytes_to_string_table, _get, _unzip_single_csv

NMDB_URL = "https://www.fhfa.gov/document/d/nmdb/nmdb-outstanding-mortgage-statistics-all-quarterly.zip"
NMDB_COLS = [
    "SOURCE", "FREQUENCY", "GEOLEVEL", "GEOID", "GEONAME", "MARKET", "PERIOD",
    "YEAR", "QUARTER", "MONTH", "SUPPRESSED", "SERIESID", "VALUE1", "VALUE2",
]


def fetch_nmdb_aggregate_statistics(node_id: str) -> None:
    resp = _get(NMDB_URL)
    csv_bytes = _unzip_single_csv(resp.content)
    table = _csv_bytes_to_string_table(csv_bytes, NMDB_COLS)
    table = table.rename_columns([c.lower() for c in table.column_names])
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="fhfa-nmdb-aggregate-statistics", fn=fetch_nmdb_aggregate_statistics, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="fhfa-nmdb-aggregate-statistics-transform",
        deps=["fhfa-nmdb-aggregate-statistics"],
        sql='''
            SELECT
                source, frequency, geolevel, geoid, geoname, market, period,
                CAST(NULLIF(year, '') AS INTEGER)     AS year,
                CAST(NULLIF(quarter, '') AS INTEGER)  AS quarter,
                CAST(NULLIF(month, '') AS INTEGER)    AS month,
                suppressed, seriesid,
                CAST(NULLIF(value1, '') AS DOUBLE)    AS value1,
                CAST(NULLIF(value2, '') AS DOUBLE)    AS value2
            FROM "fhfa-nmdb-aggregate-statistics"
        ''',
    ),
]
