"""WRI NDC-SDG linkages (Climate Watch)."""

import csv

import pyarrow as pa

from subsets_utils import save_raw_parquet
from utils import download_zip, open_member

_SDG_SCHEMA = pa.schema([
    ("iso_code3", pa.string()),
    ("country", pa.string()),
    ("sdg", pa.string()),
    ("sdg_target", pa.string()),
    ("indc_text", pa.string()),
    ("status", pa.string()),
    ("sector", pa.string()),
    ("climate_response", pa.string()),
    ("type_of_information", pa.string()),
])

_SDG_HEADER = [
    "iso", "country", "sdg", "sdg target", "indc text", "status", "sector",
    "climate response", "type of information",
]


def fetch_sdg(node_id: str) -> None:
    content = download_zip("ndc_sdg")
    reader = csv.reader(open_member(content, "ndc_sdg.csv"))
    header = [c.strip().lower() for c in next(reader)]
    assert header == _SDG_HEADER, f"unexpected ndc_sdg header: {header}"

    rows = []
    for row in reader:
        row = (row + [None] * len(_SDG_HEADER))[: len(_SDG_HEADER)]
        rows.append({
            "iso_code3": row[0],
            "country": row[1],
            "sdg": row[2],
            "sdg_target": row[3],
            "indc_text": row[4],
            "status": row[5],
            "sector": row[6],
            "climate_response": row[7],
            "type_of_information": row[8],
        })

    assert rows, "ndc_sdg produced 0 rows"
    table = pa.Table.from_pylist(rows, schema=_SDG_SCHEMA)
    save_raw_parquet(table, node_id)
