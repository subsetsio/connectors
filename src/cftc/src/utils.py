"""Shared CFTC COT fetch + SQL helpers.

Source: CFTC Socrata portal (publicreporting.cftc.gov). Each COT report *family*
is one published table; within a family the Futures-Only and Combined Socrata
resources share an identical column list and differ only in the value of
`futonly_or_combined`, so both resources stream into one raw asset and that flag
becomes the `report_type` column.

Fetch shape: stateless full re-pull. The largest family is ~570k rows of wide
(60-194 column) records across two resources — cheap to re-pull every refresh,
so no watermark/cursor state. Values arrive as JSON strings; typing happens in
the SQL transform via TRY_CAST. Raw is NDJSON (wide, heterogeneous-width records
across families) streamed to gzip to stay memory-bounded.
"""
import json
import os

from subsets_utils import get, raw_writer, transient_retry

PAGE_SIZE = 50000
MAX_PAGES_PER_RESOURCE = 200  # safety ceiling: 200 * 50k = 10M rows >> any family


def _headers() -> dict:
    # Socrata requires no auth; an app token only lifts the shared throttle.
    token = os.environ.get("CFTC_APP_TOKEN")
    return {"X-App-Token": token} if token else {}


@transient_retry()
def _fetch_page(resource_id: str, offset: int) -> list:
    url = f"https://publicreporting.cftc.gov/resource/{resource_id}.json"
    params = {"$limit": PAGE_SIZE, "$offset": offset, "$order": ":id"}
    resp = get(url, params=params, headers=_headers(), timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


def fetch_family(node_id: str, resource_ids: list) -> None:
    asset = node_id
    total = 0
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as f:
        for resource_id in resource_ids:
            offset = 0
            pages = 0
            while True:
                if pages >= MAX_PAGES_PER_RESOURCE:
                    raise RuntimeError(
                        f"{asset}: resource {resource_id} exceeded "
                        f"{MAX_PAGES_PER_RESOURCE} pages — source grew past the "
                        "safety ceiling; raise the cap deliberately"
                    )
                rows = _fetch_page(resource_id, offset)
                pages += 1
                if not rows:
                    break
                for row in rows:
                    f.write(json.dumps(row, separators=(",", ":")))
                    f.write("\n")
                total += len(rows)
                if len(rows) < PAGE_SIZE:
                    break
                offset += PAGE_SIZE
    print(f"  {asset}: wrote {total:,} rows from {len(resource_ids)} resource(s)")


# Shared identity/aggregate columns present in every family resource.
COMMON_COLS = '''
    CAST(report_date_as_yyyy_mm_dd[1:10] AS DATE)      AS report_date,
    market_and_exchange_names                          AS market,
    contract_market_name                               AS contract,
    cftc_contract_market_code                          AS cftc_code,
    cftc_market_code                                   AS exchange_code,
    commodity_name,
    commodity_group_name,
    commodity_subgroup_name,
    contract_units,
    TRY_CAST(open_interest_all AS DOUBLE)              AS open_interest,
    TRY_CAST(tot_rept_positions_long_all AS DOUBLE)    AS total_reportable_long,
    TRY_CAST(tot_rept_positions_short AS DOUBLE)       AS total_reportable_short,
    TRY_CAST(nonrept_positions_long_all AS DOUBLE)     AS nonreportable_long,
    TRY_CAST(nonrept_positions_short_all AS DOUBLE)    AS nonreportable_short,
    TRY_CAST(traders_tot_all AS DOUBLE)                AS total_traders
'''
