"""Central Bank of Russia — statistics REST warehouse (cbr.ru/dataservice).

Catalog connector. One download spec per indicator (collect entity
``pub-<publicationId>-ds-<datasetId>``); one SQL transform publishing a tidy
long-format Delta table per indicator.

Fetch shape: stateless full re-pull (shape 1). Each indicator's whole history
fits in one small JSON call (a few hundred rows), so every run re-pulls the
full series and overwrites — revisions are picked up for free. The data-service
exposes no incremental/`since` filter (only a year window), so there is no
watermark to keep.

Per indicator the flow is: /measures?datasetId= -> measure ids (type-1
indicators carry a cross-section like RUB/USD/EUR; type-2 have none ->
measureId=-1). For each measure id, /years gives the available span and
/data?y1=&y2=&publicationId=&datasetId=&measureId= returns the full series.
Each RawData row is self-describing (element_id/colId -> headerData label,
measure_id -> measure label, unit_id -> unit label, obs_val a JSON number,
ISO `date`, `periodicity`), so the raw is a flat long-format parquet.
"""

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

BASE = "https://www.cbr.ru/dataservice"

# Entity union — copied from data/sources/central-bank-of-russia/work/entity_union.json
from constants import ENTITY_IDS

SLUG = "central-bank-of-russia"

# Raw long-format schema — one row per (date, measure, series-column) observation.
SCHEMA = pa.schema([
    ("publication_id", pa.int64()),
    ("dataset_id", pa.int64()),
    ("date", pa.timestamp("s")),
    ("period_label", pa.string()),
    ("periodicity", pa.string()),
    ("measure_id", pa.int64()),       # null for type-2 indicators
    ("measure_name", pa.string()),    # null for type-2 indicators
    ("element_id", pa.int64()),       # headerData column id
    ("element_name", pa.string()),
    ("unit_id", pa.int64()),
    ("unit", pa.string()),
    ("obs_val", pa.float64()),
])


@transient_retry()
def _get_json(path: str, params: dict):
    resp = get(BASE + "/" + path, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _parse_id(node_id: str) -> tuple[int, int]:
    """central-bank-of-russia-pub-14-ds-25 -> (14, 25)."""
    entity = node_id[len(SLUG) + 1:]  # strip "central-bank-of-russia-"
    parts = entity.split("-")
    # parts == ["pub", "<pubid>", "ds", "<dsid>"]
    return int(parts[1]), int(parts[3])


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    pub_id, ds_id = _parse_id(node_id)

    measures = _get_json("measures", {"datasetId": ds_id, "lang": "ru"}).get("measure", [])
    # type-1 -> iterate the cross-section measure ids; type-2 -> single -1 call.
    measure_ids = [m["id"] for m in measures] if measures else [-1]
    measure_names = {m["id"]: m.get("name") for m in measures}

    rows = []
    for mid in measure_ids:
        years = _get_json("years", {"datasetId": ds_id, "measureId": mid, "lang": "ru"})
        if not years:
            continue
        y1 = min(y["FromYear"] for y in years)
        y2 = max(y["ToYear"] for y in years)

        payload = _get_json("data", {
            "y1": y1, "y2": y2,
            "publicationId": pub_id, "datasetId": ds_id, "measureId": mid,
            "lang": "ru",
        })
        header = {h["id"]: h.get("elname") for h in payload.get("headerData", [])}
        units = {u["id"]: u.get("val") for u in payload.get("units", [])}

        for r in payload.get("RawData", []):
            if r.get("obs_val") is None:
                continue
            eid = r.get("element_id", r.get("colId"))
            rmid = r.get("measure_id")
            rows.append({
                "publication_id": pub_id,
                "dataset_id": ds_id,
                "date": r.get("date"),
                "period_label": r.get("dt"),
                "periodicity": r.get("periodicity"),
                "measure_id": rmid,
                "measure_name": measure_names.get(rmid),
                "element_id": eid,
                "element_name": header.get(eid),
                "unit_id": r.get("unit_id"),
                "unit": units.get(r.get("unit_id")),
                "obs_val": r.get("obs_val"),
            })

    if not rows:
        raise AssertionError(f"{asset}: data-service returned no observations for ds={ds_id}")

    # Coerce ISO datetime strings to pyarrow timestamps.
    dates = pa.array([row["date"] for row in rows], type=pa.string())
    table = pa.table({
        "publication_id": pa.array([r["publication_id"] for r in rows], pa.int64()),
        "dataset_id": pa.array([r["dataset_id"] for r in rows], pa.int64()),
        "date": dates.cast(pa.timestamp("s")),
        "period_label": pa.array([r["period_label"] for r in rows], pa.string()),
        "periodicity": pa.array([r["periodicity"] for r in rows], pa.string()),
        "measure_id": pa.array([r["measure_id"] for r in rows], pa.int64()),
        "measure_name": pa.array([r["measure_name"] for r in rows], pa.string()),
        "element_id": pa.array([r["element_id"] for r in rows], pa.int64()),
        "element_name": pa.array([r["element_name"] for r in rows], pa.string()),
        "unit_id": pa.array([r["unit_id"] for r in rows], pa.int64()),
        "unit": pa.array([r["unit"] for r in rows], pa.string()),
        "obs_val": pa.array([r["obs_val"] for r in rows], pa.float64()),
    }, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
