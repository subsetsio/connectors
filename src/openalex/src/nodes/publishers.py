"""OpenAlex publishers — reference entity table from the S3 snapshot."""

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import iter_entity_rows, join, short, stats


def _flat(r):
    ids = r.get("ids") or {}
    return {
        "id": short(r.get("id")),
        "display_name": r.get("display_name"),
        "alternate_titles": join(r.get("alternate_titles")),
        "country_codes": join(r.get("country_codes")),
        "hierarchy_level": r.get("hierarchy_level"),
        "parent_publisher": short((r.get("parent_publisher") or {}).get("id")
                                  if isinstance(r.get("parent_publisher"), dict)
                                  else r.get("parent_publisher")),
        "works_count": r.get("works_count"),
        "cited_by_count": r.get("cited_by_count"),
        "h_index": stats(r, "h_index"),
        "i10_index": stats(r, "i10_index"),
        "mean_citedness": stats(r, "2yr_mean_citedness"),
        "ror": ids.get("ror"),
        "wikidata": ids.get("wikidata"),
        "created_date": r.get("created_date"),
        "updated_date": r.get("updated_date"),
    }


def fetch(node_id: str) -> None:
    save_raw_ndjson(iter_entity_rows("publishers", _flat), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="openalex-publishers", fn=fetch, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="openalex-publishers-transform",
        deps=["openalex-publishers"],
        sql='''
            SELECT id, display_name, alternate_titles, country_codes,
                   CAST(hierarchy_level AS INTEGER) AS hierarchy_level,
                   parent_publisher,
                   CAST(works_count AS BIGINT)      AS works_count,
                   CAST(cited_by_count AS BIGINT)   AS cited_by_count,
                   CAST(h_index AS INTEGER)         AS h_index,
                   CAST(i10_index AS INTEGER)       AS i10_index,
                   CAST(mean_citedness AS DOUBLE)   AS mean_citedness,
                   ror, wikidata,
                   TRY_CAST(created_date AS DATE)        AS created_date,
                   TRY_CAST(updated_date AS TIMESTAMP)   AS updated_at
            FROM "openalex-publishers" WHERE id IS NOT NULL
        ''',
    ),
]
