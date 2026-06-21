"""Zillow Research public CSVs.

Mechanism: bulk_csv. One GET per (metric, geography) at
https://files.zillowstatic.com/research/public_csvs/{folder}/{Region}_{slug}.csv
No auth, no pagination, persistent URLs. No incremental query support — each CSV
already carries the full monthly history, so this is a stateless full re-pull
every run (overwrite). Not every metric exists at every geography; missing
combos return 404 and are skipped.

Each download entity (a theme: home_value, rent, inventory, sales, market_heat)
fetches all of its metric variants across all geography levels, melts each wide
CSV (id columns + one column per month-end date) into long rows
(region_id, region_type, region_name, state_code, date, metric, value), and
streams them to one parquet asset — one batch per source CSV, so peak memory is
bounded to a single file's melt. The SQL transform pivots the long raw back to
one wide column per metric, keyed (date, region_id). Geography level is carried
as the region_type column (Zillow's RegionID is globally unique across levels).
"""

import io

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_parquet_writer,
    transient_retry,
)

BASE_URL = "https://files.zillowstatic.com/research/public_csvs"

# Geography levels published by Zillow. Not every metric exists at every level
# (e.g. ZORI has no State file) — missing combinations return 404 and are skipped.
GEOGRAPHIES = ["Metro", "State", "County", "City", "Zip"]

# entity_id -> list of (metric_column, folder, filename_slug).
# url = {BASE_URL}/{folder}/{Region}_{slug}.csv
METRICS = {
    "home_value": [
        ("all_homes", "zhvi", "zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month"),
        ("single_family", "zhvi", "zhvi_uc_sfr_tier_0.33_0.67_sm_sa_month"),
        ("condo", "zhvi", "zhvi_uc_condo_tier_0.33_0.67_sm_sa_month"),
        ("bed_1", "zhvi", "zhvi_bdrmcnt_1_uc_sfrcondo_tier_0.33_0.67_sm_sa_month"),
        ("bed_2", "zhvi", "zhvi_bdrmcnt_2_uc_sfrcondo_tier_0.33_0.67_sm_sa_month"),
        ("bed_3", "zhvi", "zhvi_bdrmcnt_3_uc_sfrcondo_tier_0.33_0.67_sm_sa_month"),
        ("bed_4", "zhvi", "zhvi_bdrmcnt_4_uc_sfrcondo_tier_0.33_0.67_sm_sa_month"),
        ("bed_5_plus", "zhvi", "zhvi_bdrmcnt_5_uc_sfrcondo_tier_0.33_0.67_sm_sa_month"),
        ("bottom_tier", "zhvi", "zhvi_uc_sfrcondo_tier_0.0_0.33_sm_sa_month"),
        ("top_tier", "zhvi", "zhvi_uc_sfrcondo_tier_0.67_1.0_sm_sa_month"),
    ],
    "rent": [
        ("rent", "zori", "zori_uc_sfrcondomfr_sm_sa_month"),
    ],
    "inventory": [
        ("for_sale_inventory", "invt_fs", "invt_fs_uc_sfrcondo_sm_month"),
        ("new_listings", "new_listings", "new_listings_uc_sfrcondo_sm_month"),
        ("new_pending", "new_pending", "new_pending_uc_sfrcondo_sm_month"),
    ],
    "sales": [
        ("median_list_price", "mlp", "mlp_uc_sfrcondo_sm_month"),
        ("median_sale_price", "median_sale_price", "median_sale_price_uc_sfrcondo_sm_sa_month"),
        ("sales_count", "sales_count_now", "sales_count_now_uc_sfrcondo_month"),
        ("pct_sold_above_list", "pct_sold_above_list", "pct_sold_above_list_uc_sfrcondo_sm_month"),
        ("pct_sold_below_list", "pct_sold_below_list", "pct_sold_below_list_uc_sfrcondo_sm_month"),
        ("days_to_pending", "mean_doz_pending", "mean_doz_pending_uc_sfrcondo_sm_month"),
        ("pct_price_cut", "perc_listings_price_cut", "perc_listings_price_cut_uc_sfrcondo_sm_month"),
    ],
    "market_heat": [
        ("market_heat", "market_temp_index", "market_temp_index_uc_sfrcondo_month"),
    ],
}

# entity union — keep in sync with data/sources/zillow/work/entity_union.json
ENTITY_IDS = ["home_value", "inventory", "market_heat", "rent", "sales"]

LONG_SCHEMA = pa.schema([
    ("region_id", pa.int64()),
    ("region_type", pa.string()),
    ("region_name", pa.string()),
    ("state_code", pa.string()),
    ("date", pa.string()),
    ("metric", pa.string()),
    ("value", pa.float64()),
])

# Standard id columns present in every Zillow research CSV.
_ID_COLS = ["RegionID", "RegionName", "RegionType", "StateName"]


@transient_retry()
def _fetch_csv(url: str) -> str | None:
    """Fetch a Zillow CSV. Returns the body, or None if the (metric, geography)
    combination does not exist (404 — an expected, permanent absence)."""
    resp = get(url, timeout=(10.0, 180.0))
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.text


def _melt_csv(text: str, metric_name: str) -> pa.Table:
    """Melt a wide Zillow CSV (id cols + one column per month) to long rows
    conforming to LONG_SCHEMA, dropping null observations."""
    import pandas as pd

    df = pd.read_csv(io.StringIO(text), dtype={"RegionName": str, "StateName": str})
    date_cols = [c for c in df.columns if c[:1].isdigit()]
    df = df[_ID_COLS + date_cols]
    long = df.melt(
        id_vars=_ID_COLS, value_vars=date_cols, var_name="date", value_name="value"
    )
    long = long.dropna(subset=["value"])

    state = [None if pd.isna(x) else str(x) for x in long["StateName"]]
    return pa.table(
        {
            "region_id": pa.array(long["RegionID"].astype("int64"), pa.int64()),
            "region_type": pa.array(long["RegionType"].astype(str), pa.string()),
            "region_name": pa.array(long["RegionName"].astype(str), pa.string()),
            "state_code": pa.array(state, pa.string()),
            "date": pa.array(long["date"].astype(str), pa.string()),
            "metric": pa.array([metric_name] * len(long), pa.string()),
            "value": pa.array(long["value"].astype("float64"), pa.float64()),
        },
        schema=LONG_SCHEMA,
    )


def fetch_one(node_id: str) -> None:
    """Fetch every metric variant x geography for one theme entity, melt to long,
    and stream to one parquet asset (one row group per source CSV)."""
    asset = node_id
    entity = node_id[len("zillow-"):].replace("-", "_")
    specs = METRICS[entity]

    wrote_any = False
    with raw_parquet_writer(asset, LONG_SCHEMA) as writer:
        for metric_name, folder, slug in specs:
            for region in GEOGRAPHIES:
                url = f"{BASE_URL}/{folder}/{region}_{slug}.csv"
                text = _fetch_csv(url)
                if text is None:
                    print(f"    {asset}: 404 (skip) {metric_name} / {region}")
                    continue
                table = _melt_csv(text, metric_name)
                if table.num_rows:
                    writer.write_table(table)
                    wrote_any = True
                    print(f"    {asset}: {metric_name} / {region} -> {table.num_rows:,} rows")

    if not wrote_any:
        raise RuntimeError(f"{asset}: no CSVs returned data — source layout may have changed")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"zillow-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


def _pivot_sql(download_id: str, metric_names: list[str]) -> str:
    """Pivot the long raw asset to one wide column per metric, keyed (date, region_id)."""
    cols = ",\n".join(
        f"            MAX(value) FILTER (WHERE metric = '{m}') AS {m}"
        for m in metric_names
    )
    return f'''
        SELECT
            CAST(date AS DATE) AS date,
            region_id,
            ANY_VALUE(region_type) AS region_type,
            ANY_VALUE(region_name) AS region_name,
            ANY_VALUE(state_code) AS state_code,
{cols}
        FROM "{download_id}"
        GROUP BY region_id, date
    '''


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"zillow-{eid.lower().replace('_', '-')}-transform",
        deps=[f"zillow-{eid.lower().replace('_', '-')}"],
        sql=_pivot_sql(
            f"zillow-{eid.lower().replace('_', '-')}",
            [m[0] for m in METRICS[eid]],
        ),
    )
    for eid in ENTITY_IDS
]
