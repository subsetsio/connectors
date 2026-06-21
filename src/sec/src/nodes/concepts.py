"""sec-concepts — catalog of the curated XBRL financial concepts we publish,
with the source's own label/description (read off the Frames API, which has no
standalone concept-metadata endpoint)."""
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, configure_http, save_raw_parquet
from utils import CONCEPTS, USER_AGENT, periods_for, try_frame

CONCEPTS_SCHEMA = pa.schema([
    ("taxonomy", pa.string()),
    ("tag", pa.string()),
    ("unit", pa.string()),
    ("concept_type", pa.string()),
    ("label", pa.string()),
    ("description", pa.string()),
])


def _concept_meta(taxonomy: str, tag: str, unit: str, ctype: str):
    """Pull the source's label/description by probing recent populated periods
    (most-recent first); the Frames API has no standalone concept-metadata
    endpoint, so we read it off a real frame."""
    for period in list(reversed(periods_for(ctype)))[:15]:
        data = try_frame(taxonomy, tag, unit, period)
        if data:
            return data
    return None


def fetch_concepts(node_id: str) -> None:
    asset = node_id
    configure_http(headers={"User-Agent": USER_AGENT})
    rows = []
    for taxonomy, tag, unit, ctype in CONCEPTS:
        meta = _concept_meta(taxonomy, tag, unit, ctype)
        rows.append({
            "taxonomy": taxonomy,
            "tag": tag,
            "unit": unit,
            "concept_type": ctype,
            "label": meta.get("label") if meta else None,
            "description": meta.get("description") if meta else None,
        })
    table = pa.Table.from_pylist(rows, schema=CONCEPTS_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="sec-concepts", fn=fetch_concepts, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="sec-concepts-transform",
        deps=["sec-concepts"],
        sql='''
            SELECT
                taxonomy,
                tag,
                unit,
                concept_type,
                label,
                description
            FROM "sec-concepts"
        ''',
    ),
]
