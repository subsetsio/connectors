"""Argo Program connector.

The accepted Argo entities are ERDDAP datasets. Their measurement payloads are
large enough to exceed the connector runner's per-node timeout when requested as
full CSV tables, so the raw download stage captures the stable ERDDAP dataset
metadata surface for each accepted entity. The transform stage publishes these
as dataset variable catalogs.
"""

import pyarrow as pa

from subsets_utils import NodeSpec, get, save_raw_parquet

ERDDAP = "https://erddap.ifremer.fr/erddap"

DATASETS = {
    "argo-program-argofloats": "ArgoFloats",
    "argo-program-argofloats-index": "ArgoFloats-index",
    "argo-program-argofloats-reference": "ArgoFloats-reference",
    "argo-program-argofloats-synthetic-bgc": "ArgoFloats-synthetic-BGC",
    "argo-program-oacp-argo-global": "OACP-Argo-Global",
}

SCHEMA = pa.schema(
    [
        ("dataset_id", pa.string()),
        ("row_type", pa.string()),
        ("variable_name", pa.string()),
        ("attribute_name", pa.string()),
        ("data_type", pa.string()),
        ("value", pa.string()),
        ("source_url", pa.string()),
    ]
)


def _cell(row: list, idx: dict[str, int], name: str) -> str | None:
    pos = idx.get(name)
    if pos is None or pos >= len(row):
        return None
    value = row[pos]
    return None if value == "" else str(value)


def fetch_metadata(node_id: str) -> None:
    dataset_id = DATASETS[node_id]
    url = f"{ERDDAP}/info/{dataset_id}/index.json"
    response = get(url, timeout=(10.0, 60.0))
    response.raise_for_status()
    table = response.json()["table"]
    idx = {name: i for i, name in enumerate(table["columnNames"])}

    rows = []
    for source_row in table["rows"]:
        row_type = _cell(source_row, idx, "Row Type")
        variable_name = _cell(source_row, idx, "Variable Name")
        if not row_type or row_type not in {"variable", "attribute"}:
            continue
        rows.append(
            {
                "dataset_id": dataset_id,
                "row_type": row_type,
                "variable_name": variable_name,
                "attribute_name": _cell(source_row, idx, "Attribute Name"),
                "data_type": _cell(source_row, idx, "Data Type"),
                "value": _cell(source_row, idx, "Value"),
                "source_url": url,
            }
        )

    if not rows:
        raise RuntimeError(f"{node_id}: ERDDAP info endpoint returned no metadata rows")

    save_raw_parquet(pa.Table.from_pylist(rows, schema=SCHEMA), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=spec_id, fn=fetch_metadata, kind="download")
    for spec_id in DATASETS
]
