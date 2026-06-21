"""World Justice Project — Atlas of Legal Needs.

Legal-needs survey catalog, delivered as an xlsx. Stateless full re-pull each
run.

URL-stability caveat (from research): the download URL embeds the release date
(e.g. AOLNS_April2024.xlsx). Bump the date token below on each annual release.
The xlsx is parsed and normalized HERE into parquet so the SQL transform can
read it (a SQL transform cannot read xlsx).
"""

import io

import openpyxl
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import clean_str, download

ATLAS_URL = "https://worldjusticeproject.org/sites/default/files/documents/AOLNS_April2024.xlsx"


_ATLAS_SCHEMA = pa.schema(
    [
        ("country", pa.string()),
        ("subnational_focus", pa.string()),
        ("study_name", pa.string()),
        ("implementer", pa.string()),
        ("year_polled", pa.string()),
        ("sample_size", pa.string()),
        ("mode", pa.string()),
        ("target_population", pa.string()),
        ("targeted_vulnerable_population", pa.string()),
        ("data_official", pa.string()),
    ]
)

# Header order in the "Legal Needs Surveys" sheet (row index 1; row 0 is a title).
_ATLAS_FIELDS = list(_ATLAS_SCHEMA.names)


def fetch_atlas_of_legal_needs(node_id: str) -> None:
    asset = node_id
    content = download(ATLAS_URL)
    wb = openpyxl.load_workbook(io.BytesIO(content), read_only=True, data_only=True)
    try:
        ws = wb["Legal Needs Surveys"]
        cols = {k: [] for k in _ATLAS_FIELDS}
        for i, row in enumerate(ws.iter_rows(values_only=True)):
            if i <= 1:  # 0 = title banner, 1 = column header
                continue
            if row is None or clean_str(row[0]) is None:
                continue
            # Map the first 10 cells positionally; cell 10 ("Data and Reports")
            # is a per-study URL and is intentionally dropped.
            for j, field in enumerate(_ATLAS_FIELDS):
                cols[field].append(clean_str(row[j]) if j < len(row) else None)
    finally:
        wb.close()

    table = pa.table(cols, schema=_ATLAS_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="world-justice-project-atlas-of-legal-needs",
        fn=fetch_atlas_of_legal_needs,
        kind="download",
    ),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="world-justice-project-atlas-of-legal-needs-transform",
        deps=["world-justice-project-atlas-of-legal-needs"],
        sql='''
            SELECT
                country,
                subnational_focus,
                study_name,
                implementer,
                year_polled,
                TRY_CAST(sample_size AS BIGINT) AS sample_size,
                mode,
                target_population,
                targeted_vulnerable_population,
                data_official
            FROM "world-justice-project-atlas-of-legal-needs"
            WHERE country IS NOT NULL
        ''',
    ),
]
