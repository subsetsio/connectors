"""World Justice Project — EuroVoices.

EU expert-scorecard indicators, delivered as a CSV inside a ZIP. Stateless full
re-pull each run.

URL-stability caveat (from research): the download URL embeds the release year
(e.g. ..._2024.zip). Bump the year token below on each annual release. The
CSV-in-ZIP is parsed and normalized HERE into parquet so the SQL transform can
read it (a SQL transform cannot read a zip).
"""

import csv
import io
import zipfile

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import clean_str, download, to_float

EUROVOICES_URL = "https://eurovoices.worldjusticeproject.org/files/WJP-expert_scorecard_data-and-codebook-2024.zip"
EUROVOICES_CSV_MEMBER = "WJP expert_scorecard_data 2024.csv"


_EUROVOICES_SCHEMA = pa.schema(
    [
        ("country", pa.string()),
        ("level", pa.string()),
        ("region_name", pa.string()),
        ("nuts_id", pa.string()),
        ("report", pa.string()),
        ("chapter", pa.string()),
        ("chapter_number", pa.string()),
        ("topic_number", pa.string()),
        ("topic", pa.string()),
        ("subtitle", pa.string()),
        ("score", pa.float64()),
    ]
)


def fetch_eurovoices(node_id: str) -> None:
    asset = node_id
    content = download(EUROVOICES_URL)
    zf = zipfile.ZipFile(io.BytesIO(content))
    raw_bytes = zf.read(EUROVOICES_CSV_MEMBER)
    # Excel-exported CSV: utf-8-sig when clean, else Windows-1252 (smart quotes).
    try:
        raw = raw_bytes.decode("utf-8-sig")
    except UnicodeDecodeError:
        raw = raw_bytes.decode("cp1252")
    reader = csv.DictReader(io.StringIO(raw))
    cols = {k: [] for k in _EUROVOICES_SCHEMA.names}
    for r in reader:
        cols["country"].append(clean_str(r.get("Country")))
        cols["level"].append(clean_str(r.get("Level")))
        cols["region_name"].append(clean_str(r.get("nuts_ltn")))
        cols["nuts_id"].append(clean_str(r.get("nuts_id")))
        cols["report"].append(clean_str(r.get("Report")))
        cols["chapter"].append(clean_str(r.get("Chapter")))
        cols["chapter_number"].append(clean_str(r.get("Chapter number")))
        cols["topic_number"].append(clean_str(r.get("Topic number")))
        cols["topic"].append(clean_str(r.get("Topic")))
        cols["subtitle"].append(clean_str(r.get("Subtitle")))
        cols["score"].append(to_float(r.get("score")))

    table = pa.table(cols, schema=_EUROVOICES_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="world-justice-project-eurovoices",
        fn=fetch_eurovoices,
        kind="download",
    ),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="world-justice-project-eurovoices-transform",
        deps=["world-justice-project-eurovoices"],
        sql='''
            SELECT
                country,
                level,
                region_name,
                nuts_id,
                report,
                chapter,
                chapter_number,
                topic_number,
                topic,
                subtitle,
                CAST(score AS DOUBLE) AS score
            FROM "world-justice-project-eurovoices"
            WHERE score IS NOT NULL
              AND country IS NOT NULL
        ''',
    ),
]
