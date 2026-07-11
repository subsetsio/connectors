"""OpenAlex works-by-dimension-year — counts of scholarly works by a categorical
dimension (work type, open-access status, research domain/field, UN SDG) over
publication year, from the REST API's `group_by`."""

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import short, works_group

# (dimension name, group_by field, filter field)
_DIMENSIONS = [
    ("type", "type", "type"),
    ("oa_status", "open_access.oa_status", "open_access.oa_status"),
    ("domain", "primary_topic.domain.id", "primary_topic.domain.id"),
    ("field", "primary_topic.field.id", "primary_topic.field.id"),
    ("sdg", "sustainable_development_goals.id", "sustainable_development_goals.id"),
]


def fetch(node_id: str) -> None:
    rows = []
    for dim, gb, filt in _DIMENSIONS:
        values = works_group(gb)  # enumerate the dimension's values (<200)
        if not values:
            raise AssertionError(f"{dim}: enumerate group_by returned nothing")
        for v in values:
            key = v.get("key")
            label = v.get("key_display_name")
            for yg in works_group("publication_year", filt=f"{filt}:{key}"):
                yk = str(yg.get("key"))
                if not yk.isdigit():
                    continue
                rows.append({
                    "dimension": dim,
                    "dimension_key": short(key),
                    "dimension_label": label,
                    "publication_year": int(yk),
                    "works_count": yg.get("count"),
                })
    if not rows:
        raise AssertionError("works-by-dimension-year: produced no rows")
    save_raw_ndjson(rows, node_id)


_DOWNLOAD_SPECS = [
    NodeSpec(id="openalex-works-by-dimension-year", fn=fetch, kind="download"),
]

_TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="openalex-works-by-dimension-year-transform",
        deps=["openalex-works-by-dimension-year"],
        sql='''
            SELECT dimension,
                   dimension_key,
                   dimension_label,
                   CAST(publication_year AS INTEGER) AS publication_year,
                   CAST(works_count AS BIGINT)       AS works_count
            FROM "openalex-works-by-dimension-year"
            WHERE publication_year IS NOT NULL
              AND CAST(publication_year AS INTEGER) BETWEEN 1500 AND 2100
        ''',
    ),
]
