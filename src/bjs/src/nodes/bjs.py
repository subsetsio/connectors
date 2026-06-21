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
    SqlNodeSpec,
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

    total = 0
    pages = 0
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as f:
        for page_idx in range(MAX_PAGES):
            rows = _fetch_page(url, page_idx * PAGE_SIZE)
            for row in rows:
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


# ---------------------------------------------------------------------------
# Transform — one published Delta table per subset
# ---------------------------------------------------------------------------

def _entity_of(spec_id: str) -> str:
    return spec_id[len(_PREFIX):]


def _nibrs_sql(view: str) -> str:
    """Curated, typed projection of the shared NIBRS National Estimates schema.

    Drops the internal derivation/permutation columns and keeps the published
    estimate plus its uncertainty bounds. TRY_CAST tolerates the source's
    string-typed sentinels (e.g. "-9") by mapping them to NULL.
    """
    return f'''
        SELECT
            TRY_CAST(time_series_start_year AS INTEGER) AS time_series_start_year,
            indicator_name,
            full_table,
            estimate_type,
            estimate_geographic_location,
            estimate_domain_1,
            TRY_CAST(estimate AS DOUBLE)                 AS estimate,
            TRY_CAST(estimate_unweighted AS DOUBLE)      AS estimate_unweighted,
            TRY_CAST(estimate_standard_error AS DOUBLE)  AS estimate_standard_error,
            TRY_CAST(estimate_lower_bound AS DOUBLE)     AS estimate_lower_bound,
            TRY_CAST(estimate_upper_bound AS DOUBLE)     AS estimate_upper_bound,
            TRY_CAST(relative_standard_error AS DOUBLE)  AS relative_standard_error,
            TRY_CAST(population_estimate AS DOUBLE)      AS population_estimate,
            TRY_CAST(agency_counts AS BIGINT)            AS agency_counts,
            estimates_version,
            suppression_flag_indicator
        FROM "{view}"
    '''


def _ncvs_sql(view: str, weight_cols: list[str]) -> str:
    """Keep the full microdata row (categorical codes stay VARCHAR), typing
    only the year and survey-weight columns. SELECT * REPLACE makes this a thin
    pass without enumerating every per-file analysis variable."""
    replaces = [
        "TRY_CAST(year AS INTEGER) AS year",
        "TRY_CAST(yearq AS DOUBLE) AS yearq",
    ]
    replaces += [f"TRY_CAST({w} AS DOUBLE) AS {w}" for w in weight_cols]
    repl = ",\n            ".join(replaces)
    return f'''
        SELECT * REPLACE (
            {repl}
        )
        FROM "{view}"
    '''


def _transform_sql(spec_id: str) -> str:
    eid = _entity_of(spec_id)
    if eid in _NIBRS_IDS:
        return _nibrs_sql(spec_id)
    return _ncvs_sql(spec_id, _NCVS_WEIGHTS[eid])


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_transform_sql(s.id),
    )
    for s in DOWNLOAD_SPECS
]
