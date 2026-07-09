"""BJS connector — Bureau of Justice Statistics open data.

Source: Socrata/SODA-flavored REST API fronted by an OJP nginx proxy at
`https://api.ojp.gov/bjsdataset/v1/`. Each dataset is one Socrata 4x4 resource
id reachable at `<base>/<4x4>.json`, accepting SoQL params ($limit, $offset,
$order, $select). The default page is capped at 1000 rows; $limit=50000 is the
verified max, so the full table is paged with $order=:id + $offset.

Two schema families are covered (10 datasets, the rank-accepted entity union):
  * NIBRS National Estimates (6): a shared 34-field aggregate-estimate schema
    (iv7i-eah6, kj7p-vx4s, ms42-n765, r32q-bdaw, uy37-xgmh, x3sz-eb6y).
  * NCVS Select microdata (4): one row per respondent, a distinct column set
    per file (gcuy-rt5g, gkck-euys, r4j4-fdwx, ya4e-n9zp).

Fetch shape: stateless full re-pull. The SODA API exposes no change cursor /
ETag, the corpus is fixed, and revisions are picked up for free by never
trusting a stored watermark. Every value comes back as a JSON string and the
column set differs across datasets, so raw is written as NDJSON (gzip-streamed,
page by page to stay memory-bounded — the largest files run to millions of
rows) and the transforms re-type on read with TRY_CAST.
"""

import json


from subsets_utils import (
    NodeSpec,
    get,
    raw_writer,
    transient_retry,
)

BASE_URL = "https://api.ojp.gov/bjsdataset/v1/"
_PREFIX = "bjs-"

PAGE_SIZE = 50000          # verified SoQL $limit ceiling on this proxy
# Safety ceiling: the largest known dataset (r4j4-fdwx) is ~6.3M rows = ~127
# pages. 1000 pages covers 50M rows; hitting it means the source grew far past
# expectations, so we raise rather than silently truncate.
MAX_PAGES = 1000

# The entity union — copied from
# data/sources/bjs/work/entity_union.json
ENTITY_IDS = [
    "gcuy-rt5g",
    "gkck-euys",
    "iv7i-eah6",
    "kj7p-vx4s",
    "ms42-n765",
    "r32q-bdaw",
    "r4j4-fdwx",
    "uy37-xgmh",
    "x3sz-eb6y",
    "ya4e-n9zp",
]

# NIBRS National Estimates datasets share one aggregate schema; the rest are
# NCVS Select microdata with per-file column sets and their own weight columns.
_NIBRS_IDS = {
    "iv7i-eah6",
    "kj7p-vx4s",
    "ms42-n765",
    "r32q-bdaw",
    "uy37-xgmh",
    "x3sz-eb6y",
}
_NCVS_WEIGHTS = {
    "gcuy-rt5g": ["wgtviccy", "newwgt"],   # Personal Victimization
    "gkck-euys": ["wgtviccy", "newwgt"],   # Household Victimization
    "r4j4-fdwx": ["wgtpercy"],             # Personal Population
    "ya4e-n9zp": ["wgthhcy"],              # Household Population
}

# The NIBRS National Estimates datasets all share this fixed 40-field schema
# (verified identical across every profiled NIBRS asset). Socrata OMITS keys
# whose value is null, so the raw rows are otherwise sparse — and a key that
# is null across the first ~millions of rows (e.g. `estimate_copula`) then
# appears late, which breaks any schema-inference reader (DuckDB read_json's
# auto-detect sample window in particular). We densify every NIBRS row to the
# full canonical key set (absent keys -> explicit null) so the raw NDJSON has
# one stable, self-describing schema. NCVS microdata is already dense and is
# left untouched.
_NIBRS_FIELDS = (
    "indicator_name",
    "estimate",
    "estimate_unweighted",
    "estimate_geographic_location",
    "estimate_type",
    "estimate_type_num",
    "estimate_domain_1",
    "estimate_domain_2",
    "estimate_standard_error",
    "estimate_upper_bound",
    "estimate_lower_bound",
    "relative_standard_error",
    "analysis_weight_name",
    "estimate_prb",
    "estimate_bias",
    "estimate_rmse",
    "relative_rmse",
    "estimate_copula",
    "estimate_type_detail",
    "estimate_type_detail_rate",
    "suppression_flag_indicator",
    "der_elig_suppression",
    "der_perm_group_suppression",
    "der_perm_group_unsuppression",
    "der_rrmse_30",
    "der_rrmse_gt_30_se_estimate",
    "der_rrmse_gt_30_se_estimate_1",
    "der_variable_name",
    "pop_cov",
    "agency_counts",
    "population_estimate",
    "poptotal_orig_univ_elig_perm",
    "poptotal_orig_elig_perm_agency",
    "prop_elig_oris_nonzero_count",
    "permutation_number",
    "prb_actual",
    "correlation_with_prior_year",
    "time_series_start_year",
    "full_table",
    "estimates_version",
)


# ---------------------------------------------------------------------------
# Fetch
# ---------------------------------------------------------------------------


@transient_retry()
def _fetch_page(url: str, offset: int) -> list[dict]:
    resp = get(
        url,
        params={"$order": ":id", "$limit": PAGE_SIZE, "$offset": offset},
        timeout=(10.0, 180.0),
    )
    resp.raise_for_status()
    return resp.json()


def fetch_one(node_id: str) -> None:
    """Page the full table for one resource and stream it to NDJSON.

    The runtime passes the spec id, which IS the asset name; the Socrata
    resource id is the id minus the `bjs-` prefix. Stateless full re-pull —
    freshness is the maintain step's concern.
    """
    asset = node_id
    resource_id = node_id[len(_PREFIX):]
    url = f"{BASE_URL}{resource_id}.json"
    # NIBRS rows are densified to the fixed schema so the raw NDJSON stays
    # schema-stable regardless of which optional fields the source omits.
    densify = resource_id in _NIBRS_IDS

    total = 0
    pages = 0
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as f:
        for page_idx in range(MAX_PAGES):
            rows = _fetch_page(url, page_idx * PAGE_SIZE)
            for row in rows:
                if densify:
                    row = {k: row.get(k) for k in _NIBRS_FIELDS}
                f.write(json.dumps(row, separators=(",", ":")))
                f.write("\n")
            total += len(rows)
            pages += 1
            if len(rows) < PAGE_SIZE:
                break
        else:
            raise RuntimeError(
                f"{asset}: exceeded MAX_PAGES={MAX_PAGES} "
                f"(offset {MAX_PAGES * PAGE_SIZE}); source larger than expected"
            )

    print(f"  -> {asset}: {total:,} rows across {pages} page(s)")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"bjs-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

