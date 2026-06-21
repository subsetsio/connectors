"""World Justice Project — Rule of Law Index.

Rule of Law Index historical scores: a wide xlsx (overall score + 8 factors +
~44 sub-factor scores per country/year) unpivoted to long form
(country x year x indicator x score). Stateless full re-pull each run; WJP
republishes a fresh full-history file per annual release, so a stored watermark
would only risk skipping revised back-years.

URL-stability caveat (from research): the download URL embeds the release year
(e.g. 2025_..._HISTORICAL_DATA_FILE.xlsx). Bump the year token below on each
annual release. The xlsx is parsed and normalized HERE into parquet so the SQL
transform can read it (a SQL transform cannot read xlsx).
"""

import io

import openpyxl
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import clean_str, download, to_float

# Latest verified product URL (year-versioned — bump on annual release).
ROL_URL = "https://worldjusticeproject.org/rule-of-law-index/downloads/2025_wjp_rule_of_law_index_HISTORICAL_DATA_FILE.xlsx"


_ROL_SCHEMA = pa.schema(
    [
        ("country", pa.string()),
        ("country_code", pa.string()),
        ("region", pa.string()),
        ("year", pa.string()),
        ("indicator", pa.string()),
        ("score", pa.float64()),
    ]
)


def fetch_rule_of_law_index(node_id: str) -> None:
    asset = node_id
    content = download(ROL_URL)
    wb = openpyxl.load_workbook(io.BytesIO(content), read_only=True, data_only=True)
    try:
        ws = wb["Historical Data"]
        rows = ws.iter_rows(values_only=True)
        header = list(next(rows))
        # Columns 0..4: Country, Year, Country_year, Country Code, Region.
        # Columns 5.. : overall score + 8 factors + ~44 sub-factor scores.
        indicator_cols = [
            (i, clean_str(header[i])) for i in range(5, len(header)) if clean_str(header[i])
        ]
        countries, codes, regions, years, indicators, scores = [], [], [], [], [], []
        for row in rows:
            if row is None or clean_str(row[0]) is None:
                continue
            country = clean_str(row[0])
            year = clean_str(row[1])
            code = clean_str(row[3]) if len(row) > 3 else None
            region = clean_str(row[4]) if len(row) > 4 else None
            for i, ind_name in indicator_cols:
                if i >= len(row):
                    continue
                score = to_float(row[i])
                countries.append(country)
                codes.append(code)
                regions.append(region)
                years.append(year)
                indicators.append(ind_name)
                scores.append(score)
    finally:
        wb.close()

    table = pa.table(
        {
            "country": countries,
            "country_code": codes,
            "region": regions,
            "year": years,
            "indicator": indicators,
            "score": scores,
        },
        schema=_ROL_SCHEMA,
    )
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="world-justice-project-rule-of-law-index",
        fn=fetch_rule_of_law_index,
        kind="download",
    ),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="world-justice-project-rule-of-law-index-transform",
        deps=["world-justice-project-rule-of-law-index"],
        sql='''
            SELECT
                country,
                country_code,
                region,
                year,
                indicator,
                CAST(score AS DOUBLE) AS score
            FROM "world-justice-project-rule-of-law-index"
            WHERE score IS NOT NULL
              AND country IS NOT NULL
              AND indicator IS NOT NULL
        ''',
    ),
]
