"""ITU DataHub - source database/provenance catalogue."""

import pyarrow as pa

from subsets_utils import save_raw_parquet
from utils import _as_int, _get_json

_DATASETS_SCHEMA = pa.schema([
    ("dataset_id", pa.int64()),
    ("dataset_short_name", pa.string()),
    ("dataset_type", pa.string()),
    ("team_short_name", pa.string()),
    ("team_name", pa.string()),
    ("email", pa.string()),
    ("publicly_visible", pa.bool_()),
    ("has_frozen_public_data", pa.bool_()),
])


def fetch_datasets(node_id: str) -> None:
    rows = _get_json("methodology/dataset")
    cols = {k: [] for k in _DATASETS_SCHEMA.names}
    for row in rows:
        cols["dataset_id"].append(_as_int(row.get("datasetID")))
        cols["dataset_short_name"].append(row.get("datasetShortName"))
        cols["dataset_type"].append(row.get("datasetType"))
        cols["team_short_name"].append(row.get("teamShortName"))
        cols["team_name"].append(row.get("teamName"))
        cols["email"].append(row.get("email"))
        cols["publicly_visible"].append(row.get("publiclyVisible"))
        cols["has_frozen_public_data"].append(row.get("hasFrozenPublicData"))

    table = pa.table(cols, schema=_DATASETS_SCHEMA)
    save_raw_parquet(table, node_id)
