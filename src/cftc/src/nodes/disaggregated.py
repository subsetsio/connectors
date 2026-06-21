"""CFTC Disaggregated COT — FutOnly (72hh-3qpy) + Combined (kh3c-gbw2), back to 2006."""
from subsets_utils import NodeSpec, SqlNodeSpec

from utils import COMMON_COLS, fetch_family

RESOURCES = ["72hh-3qpy", "kh3c-gbw2"]


def fetch(node_id: str) -> None:
    fetch_family(node_id, RESOURCES)


DOWNLOAD_SPECS = [NodeSpec(id="cftc-disaggregated", fn=fetch, kind="download")]

_SQL = f'''
    SELECT
        {COMMON_COLS},
        futonly_or_combined                                AS report_type,
        TRY_CAST(change_in_open_interest_all AS DOUBLE)    AS change_in_open_interest,
        TRY_CAST(prod_merc_positions_long AS DOUBLE)       AS producer_merchant_long,
        TRY_CAST(prod_merc_positions_short AS DOUBLE)      AS producer_merchant_short,
        TRY_CAST(swap_positions_long_all AS DOUBLE)        AS swap_dealer_long,
        TRY_CAST(swap__positions_short_all AS DOUBLE)      AS swap_dealer_short,
        TRY_CAST(swap__positions_spread_all AS DOUBLE)     AS swap_dealer_spread,
        TRY_CAST(m_money_positions_long_all AS DOUBLE)     AS managed_money_long,
        TRY_CAST(m_money_positions_short_all AS DOUBLE)    AS managed_money_short,
        TRY_CAST(m_money_positions_spread AS DOUBLE)       AS managed_money_spread,
        TRY_CAST(other_rept_positions_long AS DOUBLE)      AS other_reportable_long,
        TRY_CAST(other_rept_positions_short AS DOUBLE)     AS other_reportable_short,
        TRY_CAST(other_rept_positions_spread AS DOUBLE)    AS other_reportable_spread
    FROM "cftc-disaggregated"
    WHERE report_date_as_yyyy_mm_dd IS NOT NULL
'''

TRANSFORM_SPECS = [
    SqlNodeSpec(id="cftc-disaggregated-transform", deps=["cftc-disaggregated"], sql=_SQL)
]
