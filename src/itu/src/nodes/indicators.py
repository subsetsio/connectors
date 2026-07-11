"""ITU DataHub — indicators subset.

Metadata catalogue of the ICT indicators / series. The catalogue codeIDs are
expanded via dictionaries/getbyids (which unfolds collections to their member
series), capturing both parent and child series. Stateless full re-pull.
"""

import json

import pyarrow as pa

from subsets_utils import save_raw_parquet
from utils import _as_int, _catalogue_code_ids, _get_json

_INDICATORS_SCHEMA = pa.schema([
    ("code_id", pa.int64()),
    ("code", pa.string()),
    ("label", pa.string()),
    ("category", pa.string()),
    ("sub_category", pa.string()),
    ("units", pa.string()),
    ("units_type", pa.string()),
    ("answer_type", pa.string()),
    ("series_type", pa.string()),
    ("start_year", pa.int64()),
    ("end_year", pa.int64()),
    ("database_id", pa.int64()),
    ("is_collection", pa.bool_()),
    ("parent_code_id", pa.int64()),
    ("collection_indicator", pa.string()),
    ("disaggregation", pa.string()),
    ("code_desc", pa.string()),
])


def _as_str(v):
    """Coerce a metadata value to a string column value. Some indicator fields
    (e.g. disaggregation) are arrays/objects — JSON-encode those rather than
    forcing pyarrow to choke on a non-scalar."""
    if v is None or isinstance(v, str):
        return v
    if isinstance(v, (list, dict)):
        return json.dumps(v, ensure_ascii=False)
    return str(v)


def fetch_indicators(node_id: str) -> None:
    asset = node_id
    code_ids, info = _catalogue_code_ids()

    # getbyids expands each catalogue entry (incl. collections) to its member
    # series, so we capture both parent and child series in the catalogue.
    records: dict[int, dict] = {}
    chunk = 25
    for i in range(0, len(code_ids), chunk):
        ids = ",".join(str(x) for x in code_ids[i:i + chunk])
        for coll in _get_json("dictionaries/getbyids", params={"codeids": ids}):
            for code in coll.get("codes", []):
                cid = code.get("codeID")
                if cid is not None:
                    records[cid] = code

    cols = {k: [] for k in _INDICATORS_SCHEMA.names}
    for cid, code in records.items():
        meta = info.get(cid, {})
        cols["code_id"].append(cid)
        cols["code"].append(_as_str(code.get("code")))
        cols["label"].append(_as_str(code.get("label")))
        cols["category"].append(_as_str(code.get("category") or meta.get("category")))
        cols["sub_category"].append(_as_str(code.get("subCategory") or meta.get("sub_category")))
        cols["units"].append(_as_str(code.get("units")))
        cols["units_type"].append(_as_str(code.get("unitsType")))
        cols["answer_type"].append(_as_str(code.get("answerType")))
        cols["series_type"].append(_as_str(code.get("seriesType")))
        cols["start_year"].append(_as_int(code.get("startYear")))
        cols["end_year"].append(_as_int(code.get("endYear")))
        cols["database_id"].append(_as_int(code.get("databaseID")))
        cols["is_collection"].append(bool(meta.get("is_collection", False)))
        cols["parent_code_id"].append(_as_int(code.get("parentCodeID")))
        cols["collection_indicator"].append(_as_str(code.get("collection-indicator")))
        cols["disaggregation"].append(_as_str(code.get("disaggregation")))
        cols["code_desc"].append(_as_str(code.get("codeDesc")))
    table = pa.table(cols, schema=_INDICATORS_SCHEMA)
    save_raw_parquet(table, asset)
