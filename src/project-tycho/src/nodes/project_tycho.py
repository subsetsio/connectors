"""Project Tycho HealthData.gov mirror downloads.

The current Project Tycho website and API require a registered user/API key.
The public path verified for this connector is the HealthData.gov mirror:
Level 1 as a Socrata CSV export, and Level 2 as a ZIP containing one CSV.
Both are frozen historical NNDSS releases covering 1888-2013.
"""

import csv
import io
import zipfile

import pyarrow as pa
import pyarrow.csv as pacsv

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get,
    raw_asset_exists,
    record_source_signature,
    save_raw_parquet,
    source_unchanged,
)

LEVEL_1_URL = "https://healthdata.gov/api/views/g89t-x93h/rows.csv?accessType=DOWNLOAD"
LEVEL_2_URL = "https://healthdata.gov/download/8ihh-ztee/application/zip"

LEVEL_1_ID = "project-tycho-level-1-data"
LEVEL_2_ID = "project-tycho-level-2-data"


def _csv_to_string_table(raw: bytes) -> pa.Table:
    sample = raw[:65536].decode("utf-8-sig", errors="replace")
    header = next(csv.reader(io.StringIO(sample)))
    names = [name.strip().replace(" ", "_") for name in header]
    return pacsv.read_csv(
        pa.py_buffer(raw),
        read_options=pacsv.ReadOptions(column_names=names, skip_rows=1),
        convert_options=pacsv.ConvertOptions(
            column_types={name: pa.string() for name in names},
            strings_can_be_null=False,
        ),
    )


def fetch_level_1(node_id: str) -> None:
    resp = get(LEVEL_1_URL, timeout=(30.0, 300.0))
    resp.raise_for_status()
    table = _csv_to_string_table(resp.content)
    save_raw_parquet(table, node_id)
    record_source_signature(node_id, LEVEL_1_URL, response=resp)


def fetch_level_2(node_id: str) -> None:
    resp = get(LEVEL_2_URL, timeout=(30.0, 300.0))
    resp.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        csv_members = [name for name in zf.namelist() if name.lower().endswith(".csv")]
        if csv_members != ["ProjectTycho_Level2_v1.1.0.csv"]:
            raise ValueError(f"unexpected Level 2 ZIP members: {zf.namelist()}")
        raw = zf.read(csv_members[0])
    table = _csv_to_string_table(raw)
    save_raw_parquet(table, node_id)
    record_source_signature(node_id, LEVEL_2_URL, response=resp)


DOWNLOAD_SPECS = [
    NodeSpec(id=LEVEL_1_ID, fn=fetch_level_1, kind="download"),
    NodeSpec(id=LEVEL_2_ID, fn=fetch_level_2, kind="download"),
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=LEVEL_1_ID,
        description="Frozen historical HealthData.gov mirror; skip when source validators are unchanged.",
        check=lambda aid: source_unchanged(aid, LEVEL_1_URL) and raw_asset_exists(aid, "parquet"),
    ),
    MaintainSpec(
        asset_id=LEVEL_2_ID,
        description="Frozen historical HealthData.gov mirror; skip when source validators are unchanged.",
        check=lambda aid: source_unchanged(aid, LEVEL_2_URL) and raw_asset_exists(aid, "parquet"),
    ),
]
