"""Bank Negara Malaysia — snapshot resources (base-rate,
renminbi-fx-forward-price).

Access pattern: single latest-state call (/<res>), no history endpoint. Both
resources share the same fetch body (parametric on resource) but have distinct
payload shapes and therefore distinct published schemas:
  - base-rate: a list of per-bank rates, stamped with the snapshot effective_date
  - renminbi-fx-forward-price: one nested record flattened into selling_*/buying_*
Stateless full re-pull.
"""
from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson

from utils import PREFIX, _fetch, _has_rows


def _collect_snapshot(resource: str):
    payload = _fetch(resource)
    if not _has_rows(payload):
        raise RuntimeError(f"{resource}: empty snapshot")
    data = payload.get("data")
    meta = payload.get("meta") or {}
    rows = []
    if resource == "base-rate":
        eff = meta.get("effective_date")
        for rec in data:
            row = dict(rec)
            row["effective_date"] = eff
            rows.append(row)
    else:  # renminbi-fx-forward-price: single nested record
        rec = data
        row = {"date": rec.get("date")}
        for side in ("selling", "buying"):
            for k, v in (rec.get(side) or {}).items():
                row[f"{side}_{k}"] = v
        rows.append(row)
    return rows


def fetch_one(node_id: str) -> None:
    resource = node_id[len(PREFIX):]
    rows = _collect_snapshot(resource)
    if not rows:
        raise RuntimeError(f"{resource}: collected 0 rows")
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{PREFIX}base-rate", fn=fetch_one, kind="download"),
    NodeSpec(id=f"{PREFIX}renminbi-fx-forward-price", fn=fetch_one, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{PREFIX}base-rate-transform",
        deps=[f"{PREFIX}base-rate"],
        sql=f'''
            SELECT bank_code, bank_name,
                   CAST(base_rate AS DOUBLE)                  AS base_rate,
                   CAST(base_lending_rate AS DOUBLE)          AS base_lending_rate,
                   CAST(indicative_eff_lending_rate AS DOUBLE) AS indicative_eff_lending_rate,
                   CAST(effective_date AS DATE)               AS effective_date
            FROM "{PREFIX}base-rate"
            WHERE bank_code IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id=f"{PREFIX}renminbi-fx-forward-price-transform",
        deps=[f"{PREFIX}renminbi-fx-forward-price"],
        sql=f'''
            SELECT CAST(date AS DATE) AS date, * EXCLUDE (date)
            FROM "{PREFIX}renminbi-fx-forward-price"
            WHERE date IS NOT NULL
        ''',
    ),
]
