"""OpenAlex funders — reference entity table from the S3 snapshot."""

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import iter_entity_rows, join, short, stats


def _flat(r):
    ids = r.get("ids") or {}
    return {
        "id": short(r.get("id")),
        "display_name": r.get("display_name"),
        "alternate_titles": join(r.get("alternate_titles")),
        "country_code": r.get("country_code"),
        "description": r.get("description"),
        "homepage_url": r.get("homepage_url"),
        "works_count": r.get("works_count"),
        "cited_by_count": r.get("cited_by_count"),
        "awards_count": r.get("awards_count"),
        "h_index": stats(r, "h_index"),
        "i10_index": stats(r, "i10_index"),
        "mean_citedness": stats(r, "2yr_mean_citedness"),
        "ror": ids.get("ror"),
        "doi": ids.get("doi"),
        "wikidata": ids.get("wikidata"),
        "created_date": r.get("created_date"),
        "updated_date": r.get("updated_date"),
    }


def fetch(node_id: str) -> None:
    save_raw_ndjson(iter_entity_rows("funders", _flat), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="openalex-funders", fn=fetch, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="openalex-funders-transform",
        deps=["openalex-funders"],
        sql='''
            SELECT id, display_name, alternate_titles, country_code, description,
                   homepage_url,
                   CAST(works_count AS BIGINT)      AS works_count,
                   CAST(cited_by_count AS BIGINT)   AS cited_by_count,
                   CAST(awards_count AS BIGINT)     AS awards_count,
                   CAST(h_index AS INTEGER)         AS h_index,
                   CAST(i10_index AS INTEGER)       AS i10_index,
                   CAST(mean_citedness AS DOUBLE)   AS mean_citedness,
                   ror, doi, wikidata,
                   TRY_CAST(created_date AS DATE)        AS created_date,
                   TRY_CAST(updated_date AS TIMESTAMP)   AS updated_at
            FROM "openalex-funders" WHERE id IS NOT NULL
        ''',
    ),
]
