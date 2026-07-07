from __future__ import annotations

import csv
import io
import zipfile

import pyarrow as pa
from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get,
    raw_asset_exists,
    save_raw_parquet,
)


DATASET_PID = "doi:10.7910/DVN/LM4OWF"
METADATA_URL = "https://dataverse.harvard.edu/api/datasets/:persistentId/"

SUMMARY_SCHEMA = pa.schema(
    [
        ("country", pa.string()),
        ("year", pa.int64()),
        ("gini_disp", pa.float64()),
        ("gini_disp_se", pa.float64()),
        ("gini_mkt", pa.float64()),
        ("gini_mkt_se", pa.float64()),
        ("abs_red", pa.float64()),
        ("abs_red_se", pa.float64()),
        ("rel_red", pa.float64()),
        ("rel_red_se", pa.float64()),
        ("release_label", pa.string()),
        ("release_description", pa.string()),
        ("release_time", pa.string()),
        ("file_md5", pa.string()),
    ]
)


def _current_release_file() -> tuple[dict, dict]:
    response = get(METADATA_URL, params={"persistentId": DATASET_PID}, timeout=60.0)
    response.raise_for_status()
    latest = response.json()["data"]["latestVersion"]
    files = latest.get("files", [])
    current_files = [
        item
        for item in files
        if item.get("label", "").startswith("swiid")
        and item.get("label", "").endswith(".zip")
        and not item.get("label", "").startswith("x_")
        and item.get("restricted") is False
    ]
    if not current_files:
        raise RuntimeError("Dataverse metadata did not contain an unrestricted current SWIID ZIP")
    return current_files[0], latest


def _as_float(value: str) -> float | None:
    value = value.strip()
    return float(value) if value else None


def fetch_swiid(node_id: str) -> None:
    release_file, latest = _current_release_file()
    data_file = release_file["dataFile"]
    file_id = data_file["id"]
    response = get(f"https://dataverse.harvard.edu/api/access/datafile/{file_id}", timeout=180.0)
    response.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(response.content)) as archive:
        summary_names = [name for name in archive.namelist() if name.endswith("_summary.csv")]
        if len(summary_names) != 1:
            raise RuntimeError(f"expected exactly one summary CSV in SWIID ZIP, found {summary_names!r}")
        text = archive.read(summary_names[0]).decode("utf-8-sig")

    rows = []
    for row in csv.DictReader(io.StringIO(text)):
        rows.append(
            {
                "country": row["country"],
                "year": int(row["year"]),
                "gini_disp": _as_float(row["gini_disp"]),
                "gini_disp_se": _as_float(row["gini_disp_se"]),
                "gini_mkt": _as_float(row["gini_mkt"]),
                "gini_mkt_se": _as_float(row["gini_mkt_se"]),
                "abs_red": _as_float(row["abs_red"]),
                "abs_red_se": _as_float(row["abs_red_se"]),
                "rel_red": _as_float(row["rel_red"]),
                "rel_red_se": _as_float(row["rel_red_se"]),
                "release_label": release_file.get("label"),
                "release_description": release_file.get("description"),
                "release_time": latest.get("releaseTime"),
                "file_md5": data_file.get("md5"),
            }
        )

    table = pa.Table.from_pylist(rows, schema=SUMMARY_SCHEMA)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="swiid-swiid", fn=fetch_swiid),
]


MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id="swiid-swiid",
        description=(
            "SWIID releases are periodic Dataverse ZIP updates; refresh at most "
            "weekly while production cadence is semiannual/inferred from recent releases."
        ),
        check=lambda asset_id: raw_asset_exists(asset_id, "parquet", max_age_days=7),
    )
]
