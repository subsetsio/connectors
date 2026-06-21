"""OpenAlex works-by-year — counts of scholarly works by publication year,
from the REST API's `group_by`."""

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import works_group


def fetch(node_id: str) -> None:
    rows = []
    for g in works_group("publication_year"):
        k = str(g.get("key"))
        if not k.isdigit():
            continue
        rows.append({"publication_year": int(k), "works_count": g.get("count")})
    if not rows:
        raise AssertionError("works-by-year: group_by returned no year rows")
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="openalex-works-by-year", fn=fetch, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="openalex-works-by-year-transform",
        deps=["openalex-works-by-year"],
        sql='''
            SELECT CAST(publication_year AS INTEGER) AS publication_year,
                   CAST(works_count AS BIGINT)       AS works_count
            FROM "openalex-works-by-year"
            WHERE publication_year IS NOT NULL
              AND CAST(publication_year AS INTEGER) BETWEEN 1500 AND 2100
            ORDER BY publication_year
        ''',
    ),
]
