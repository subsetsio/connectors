"""Stack Overflow Annual Developer Survey -- schema codebook.

The `schema-codebook` subset stacks every year's schema.csv into one tidy
reference table (survey_year, column_name, question_text); the upstream
schema.csv layout drifts across years, so it is normalized to those three
columns before concatenation. Joinable to the results tables by
(survey_year, column_name) for the years that publish a codebook (2016+).
"""
import httpx

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet

from utils import RAW_BASE, fetch_bytes, read_csv

SLUG = "stack-overflow-annual-developer-survey"

# Entity union (rank-active), copied verbatim from work/entity_union.json.
from constants import RESULTS_YEARS


def fetch_codebook(node_id: str) -> None:
    """Stack every available year's schema.csv into one tidy codebook.

    schema.csv first appears in 2016 and its column layout drifts year to year
    (Column/QuestionText/Note -> qid/qname/question/...). Normalize each year to
    (survey_year, column_name, question_text); skip years with no schema.csv (404).
    """
    import pandas as pd
    import pyarrow as pa

    asset = node_id
    frames = []
    for year in RESULTS_YEARS:
        try:
            content = fetch_bytes(f"{RAW_BASE}/{year}/schema.csv")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                continue  # year ships no codebook (2011-2015)
            raise

        df = read_csv(content)
        lower = {c.lower(): c for c in df.columns}

        def pick(*names):
            for n in names:
                if n in lower:
                    return df[lower[n]]
            return pd.Series([None] * len(df))

        frames.append(pd.DataFrame({
            "survey_year": int(year),
            # newer layouts: qname is the results-column code; older: Column.
            "column_name": pick("qname", "column", "qid"),
            "question_text": pick("question", "questiontext", "question_text"),
        }))

    combined = pd.concat(frames, ignore_index=True)
    schema = pa.schema([
        ("survey_year", pa.int64()),
        ("column_name", pa.string()),
        ("question_text", pa.string()),
    ])
    table = pa.Table.from_pandas(combined, schema=schema, preserve_index=False)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-schema-codebook", fn=fetch_codebook, kind="download"),
]


_CODEBOOK_SQL = f'''
    SELECT
        CAST(survey_year AS INTEGER) AS survey_year,
        column_name,
        question_text
    FROM "{SLUG}-schema-codebook"
    WHERE column_name IS NOT NULL
'''

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{SLUG}-schema-codebook-transform",
        deps=[f"{SLUG}-schema-codebook"],
        sql=_CODEBOOK_SQL,
    ),
]
