"""gapminder-concepts: the indicator-metadata catalog merged from both repos."""
import csv
import io

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import REPOS, get_text

# Concept columns kept for the catalog subset (union across both repos; any column
# absent from a repo's concepts.csv is filled with None so every row is uniform).
CONCEPT_KEYS = [
    "concept", "concept_type", "name", "name_short", "name_catalog",
    "description", "unit", "tags", "scales", "domain", "source_url", "format",
]


def fetch_concepts(node_id: str) -> None:
    asset = node_id
    rows = []
    for repo, base in REPOS.items():
        text = get_text(base + "/ddf--concepts.csv")
        for row in csv.DictReader(io.StringIO(text)):
            out = {k: (row.get(k) or None) for k in CONCEPT_KEYS}
            out["repo"] = repo
            rows.append(out)
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="gapminder-concepts", fn=fetch_concepts, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="gapminder-concepts-transform",
        deps=["gapminder-concepts"],
        sql='''
            SELECT
                concept,
                concept_type,
                name,
                name_short,
                description,
                unit,
                tags,
                scales,
                domain,
                source_url,
                repo
            FROM "gapminder-concepts"
            WHERE concept IS NOT NULL
        ''',
    ),
]
