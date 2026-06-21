"""House Price Index — single long-format master CSV."""

from __future__ import annotations

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet

from utils import _csv_bytes_to_string_table, _get

HPI_URL = "https://www.fhfa.gov/hpi/download/monthly/hpi_master.csv"
HPI_COLS = [
    "hpi_type", "hpi_flavor", "frequency", "level", "place_name", "place_id",
    "yr", "period", "index_nsa", "index_sa", "rstderr", "note",
]


def fetch_hpi(node_id: str) -> None:
    resp = _get(HPI_URL)
    table = _csv_bytes_to_string_table(resp.content, HPI_COLS)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="fhfa-hpi", fn=fetch_hpi, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="fhfa-hpi-transform",
        deps=["fhfa-hpi"],
        sql='''
            SELECT
                hpi_type, hpi_flavor, frequency, level, place_name, place_id,
                CAST(NULLIF(yr, '') AS INTEGER)        AS year,
                CAST(NULLIF(period, '') AS INTEGER)    AS period,
                CAST(NULLIF(index_nsa, '') AS DOUBLE)  AS index_nsa,
                CAST(NULLIF(index_sa, '') AS DOUBLE)   AS index_sa,
                CAST(NULLIF(rstderr, '') AS DOUBLE)    AS rstderr,
                NULLIF(note, '')                       AS note
            FROM "fhfa-hpi"
            WHERE NULLIF(index_nsa, '') IS NOT NULL OR NULLIF(index_sa, '') IS NOT NULL
        ''',
    ),
]
