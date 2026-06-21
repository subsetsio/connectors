"""ADP National Employment Report — U.S. private employment levels.

Raw + seasonally adjusted, monthly + weekly, back to 2010. Static-CDN bulk
download (mechanism `bulk_history_csv`): the persistent root index JSON resolves
to the current history ZIP holding one long-format CSV for the whole corpus.

Fetch shape: stateless full re-pull. The corpus is one small CSV (~26k rows,
<2MB) with no incremental filter, so we re-download the whole thing every run
and overwrite — revisions and benchmark re-weightings are picked up for free.
The dated /artifacts/.../<YYYYMMDD>/ folder rotates each monthly release, so we
always resolve the current ZIP via the persistent root index rather than
hardcoding a date.
"""
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet

from utils import parse_float, read_history_csv

# Persistent root index (the only stable URL; everything under /artifacts is
# point-in-time and must be discovered through this).
NER_INDEX = "https://adpemploymentreport.com/ner_production.json"

NER_SCHEMA = pa.schema([
    ("timestep", pa.string()),
    ("aggregation", pa.string()),
    ("category", pa.string()),
    ("date", pa.string()),
    ("ner", pa.float64()),
    ("ner_sa", pa.float64()),
])


def fetch_ner_employment(node_id: str) -> None:
    rows = read_history_csv(NER_INDEX)
    records = [{
        "timestep": r["timestep"],
        "aggregation": r["agg_RIS"],
        "category": r["category"],
        "date": r["date"],
        "ner": parse_float(r["NER"]),
        "ner_sa": parse_float(r["NER_SA"]),
    } for r in rows]
    table = pa.Table.from_pylist(records, schema=NER_SCHEMA)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="adp-ner-employment", fn=fetch_ner_employment, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="adp-ner-employment-transform",
        deps=["adp-ner-employment"],
        sql='''
            SELECT
                CAST(date AS DATE)        AS date,
                timestep                  AS frequency,
                aggregation,
                category,
                ner                       AS employment,
                ner_sa                    AS employment_sa
            FROM "adp-ner-employment"
            WHERE date IS NOT NULL
        ''',
    ),
]
