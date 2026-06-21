"""CFTC TFF (Traders in Financial Futures) COT — FutOnly (gpe5-46if) + Combined (yw9f-hn96), back to 2006."""
from subsets_utils import NodeSpec, SqlNodeSpec

from utils import COMMON_COLS, fetch_family

RESOURCES = ["gpe5-46if", "yw9f-hn96"]


def fetch(node_id: str) -> None:
    fetch_family(node_id, RESOURCES)


DOWNLOAD_SPECS = [NodeSpec(id="cftc-tff", fn=fetch, kind="download")]

_SQL = f'''
    SELECT
        {COMMON_COLS},
        futonly_or_combined                                AS report_type,
        TRY_CAST(change_in_open_interest_all AS DOUBLE)    AS change_in_open_interest,
        TRY_CAST(dealer_positions_long_all AS DOUBLE)      AS dealer_long,
        TRY_CAST(dealer_positions_short_all AS DOUBLE)     AS dealer_short,
        TRY_CAST(dealer_positions_spread_all AS DOUBLE)    AS dealer_spread,
        TRY_CAST(asset_mgr_positions_long AS DOUBLE)       AS asset_manager_long,
        TRY_CAST(asset_mgr_positions_short AS DOUBLE)      AS asset_manager_short,
        TRY_CAST(asset_mgr_positions_spread AS DOUBLE)     AS asset_manager_spread,
        TRY_CAST(lev_money_positions_long AS DOUBLE)       AS leveraged_funds_long,
        TRY_CAST(lev_money_positions_short AS DOUBLE)      AS leveraged_funds_short,
        TRY_CAST(lev_money_positions_spread AS DOUBLE)     AS leveraged_funds_spread,
        TRY_CAST(other_rept_positions_long AS DOUBLE)      AS other_reportable_long,
        TRY_CAST(other_rept_positions_short AS DOUBLE)     AS other_reportable_short,
        TRY_CAST(other_rept_positions_spread AS DOUBLE)    AS other_reportable_spread
    FROM "cftc-tff"
    WHERE report_date_as_yyyy_mm_dd IS NOT NULL
'''

TRANSFORM_SPECS = [
    SqlNodeSpec(id="cftc-tff-transform", deps=["cftc-tff"], sql=_SQL)
]
