"""UNDP MPI — global Multidimensional Poverty Index (gMPI Table 1).

MPI value, headcount, intensity, population in poverty and inequality among the
poor, by country and survey period. Parsed from a presentation-formatted XLSX.

Static, versioned bulk artefact (the year stamp in the URL is bumped by HDRO
once a year with each new Human Development Report). Full re-pull every run; the
payload is tiny (~140KB).
"""
import io
import re

import openpyxl
import pyarrow as pa

from subsets_utils import save_raw_parquet
from utils import fetch_bytes, num

MPI_URL = "https://hdr.undp.org/sites/default/files/publications/additional-files/2025-10/2025_gMPI_Table1and2.xlsx"

# gMPI Table 1 value columns (fixed positions, validated by probing — footnote
# columns sit at the odd offsets between them). col index -> output field.
MPI_VALUE_COLS = {
    "mpi_value": 3,
    "headcount_pct": 5,
    "pop_poor_survey_thousands": 7,
    "pop_poor_2023_thousands": 9,
    "intensity_pct": 11,
    "inequality": 13,
    "severe_poverty_pct": 15,
    "vulnerable_pct": 17,
    "contrib_health_pct": 19,
    "contrib_education_pct": 21,
    "contrib_living_standards_pct": 23,
    "national_poverty_pct": 25,
    "ppp300_poverty_pct": 27,
}

MPI_SCHEMA = pa.schema(
    [("country", pa.string()), ("survey", pa.string())]
    + [(name, pa.float64()) for name in MPI_VALUE_COLS]
)


def fetch_mpi(node_id: str) -> None:
    asset = node_id
    content = fetch_bytes(MPI_URL)
    wb = openpyxl.load_workbook(io.BytesIO(content), read_only=True, data_only=True)
    ws = wb["gMPI_Table1"]

    # Presentation-formatted sheet: multi-row header, then country rows with
    # footnote columns interleaved between value columns (see MPI_VALUE_COLS for
    # the validated fixed positions). country=0, survey=1.
    rows = []
    for record in ws.iter_rows(values_only=True):
        if record is None or len(record) <= max(MPI_VALUE_COLS.values()):
            continue
        country = record[0]
        survey = record[1]
        # A data row has a country name, a survey label containing a year, and a
        # numeric MPI value. Section subheaders / note rows fail this guard.
        if not isinstance(country, str) or not country.strip():
            continue
        if not isinstance(survey, str) or not re.search(r"\d{4}", survey):
            continue
        mpi = num(record[MPI_VALUE_COLS["mpi_value"]])
        if mpi is None:
            continue
        row = {"country": country.strip(), "survey": survey.strip()}
        for name, col in MPI_VALUE_COLS.items():
            row[name] = num(record[col])
        rows.append(row)
    wb.close()

    if not rows:
        raise AssertionError(f"{asset}: parsed 0 country rows from gMPI Table 1")
    table = pa.Table.from_pylist(rows, schema=MPI_SCHEMA)
    save_raw_parquet(table, asset)
