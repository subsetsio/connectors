"""EPO patent applications & grants (countries.json) — long-format counts."""

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import fetch_json


def fetch_patent_applications_grants(node_id: str) -> None:
    """countries.json: dict keyed '<country>_<metric>_tng', each value a list of
    rows keyed by field_id with year columns. Unpivot into long format:
    (country_code, metric, field_id, year, value)."""
    data = fetch_json("countries.json")
    rows = []
    for key, series in data.items():
        stem = key[:-4] if key.endswith("_tng") else key  # drop trailing _tng
        country, _, metric = stem.rpartition("_")
        cc = country.upper()  # e.g. 'US'; aggregate -> 'ALL_COUNTRIES'
        for rec in series:
            field_id = rec.get("field_id")
            for col, val in rec.items():
                if col.isdigit():  # year columns only
                    rows.append(
                        {
                            "country_code": cc,
                            "metric": metric,
                            "field_id": field_id,
                            "year": col,
                            "value": val,
                        }
                    )
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="epo-patent-applications-grants",
        fn=fetch_patent_applications_grants,
        kind="download",
    ),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="epo-patent-applications-grants-transform",
        deps=["epo-patent-applications-grants"],
        sql='''
            SELECT
                country_code,
                metric,
                CAST(field_id AS INTEGER) AS field_id,
                CAST(year AS INTEGER)     AS year,
                CAST(value AS BIGINT)     AS value
            FROM "epo-patent-applications-grants"
            WHERE value IS NOT NULL AND value <> ''
        ''',
    ),
]
