"""Census and Statistics Department (Hong Kong) — web-table connector.

Catalog connector: one download node per C&SD "web table" (tb_code), one
published Delta table per web table. Mechanism = the first-party MDT bulk CSVs
(research mechanism 'bulk_csv'), the optimal path.

Per table the fetch fn:
  1. GETs https://www.censtatd.gov.hk/data/table_<tb_code>_comp.json for the
     theme_id and the table_component_list ((stat_var, stat_pres) components).
  2. For each component GETs the bulk CSV
       https://www.censtatd.gov.hk/data/MDT_<theme_id>_<tb_code>_<stat_var>_<stat_pres>.csv
     ('%' in stat_pres written as the literal 'percent'). Each CSV is the full
     labelled history for that component: one column per classification
     dimension (SEX, AGE, ACTIVITY, ...), a year column CCYY, an optional
     frequency/reference code (H=mid/year-end, Q=quarter, ...), plus obs_value
     and sd_value.
  3. Concatenates the components (they share identical dimension columns within
     a table), tagging each row with stat_var + stat_pres, and writes one
     ndjson raw asset. ndjson because the dimension column set differs from
     table to table — there is no single fixed schema across the 512 subsets.

Fetch shape = stateless full re-pull (shape 1): the whole corpus is small
(typical CSV tens-to-hundreds of KB, whole source well under ~1GB) and the file
endpoints expose no incremental filter, so every run re-fetches in full and
overwrites. Revisions are picked up for free.
"""

import csv
import io

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_ndjson, transient_retry
from constants import ENTITY_IDS

SLUG = "census-and-statistics-department"
PREFIX = f"{SLUG}-"
BASE = "https://www.censtatd.gov.hk"

# spec-id image (lower-cased, '_'->'-') -> original tb_code. Pure computation
# over the imported id list; no I/O at import time.
_TB_BY_IMAGE = {eid.lower().replace("_", "-"): eid for eid in ENTITY_IDS}


@transient_retry()
def _fetch(url):
    """GET with the standard transient policy. Returns the response, or None on
    a permanent 404 (a missing table component is skipped, not retried)."""
    resp = get(url, timeout=(10.0, 120.0))
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp


def _num(value):
    """Cast a bulk-CSV numeric cell (e.g. '528.9000000000') to float; '' -> None."""
    if value is None:
        return None
    value = value.strip()
    if value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    tb_code = _TB_BY_IMAGE[node_id[len(PREFIX):]]

    comp_resp = _fetch(f"{BASE}/data/table_{tb_code}_comp.json")
    if comp_resp is None:
        raise RuntimeError(f"{tb_code}: comp.json missing (404)")
    comp = comp_resp.json()
    theme_id = comp.get("theme_id")
    components = comp.get("table_component_list") or []
    if not theme_id or not components:
        raise RuntimeError(f"{tb_code}: no theme_id / components in comp.json")

    rows = []
    for c in components:
        sv = c.get("stat_var")
        sp = c.get("stat_pres")
        if not sv or not sp:
            continue
        sp_file = sp.replace("%", "percent")
        url = f"{BASE}/data/MDT_{theme_id}_{tb_code}_{sv}_{sp_file}.csv"
        resp = _fetch(url)
        if resp is None:
            # this presentation has no bulk file — skip it, keep other components
            print(f"WARN {tb_code}: component {sv}/{sp} MDT 404 ({url})")
            continue
        reader = csv.DictReader(io.StringIO(resp.text))
        for r in reader:
            r["obs_value"] = _num(r.get("obs_value"))
            sd = (r.get("sd_value") or "").strip()
            r["sd_value"] = sd or None
            r["stat_var"] = sv
            r["stat_pres"] = sp
            rows.append(r)

    if not rows:
        raise RuntimeError(f"{tb_code}: no rows from any component")

    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One published Delta table per web table: pass the long-format rows through,
# guaranteeing obs_value is DOUBLE and dropping rows with no observation.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT * EXCLUDE (obs_value),
                   CAST(obs_value AS DOUBLE) AS obs_value
            FROM "{s.id}"
            WHERE obs_value IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
