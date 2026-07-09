"""Legacy module kept for reference; active specs live in nodes/cftc.py and src/transforms."""

from utils import COMMON_COLS, fetch_family

RESOURCES = ["72hh-3qpy", "kh3c-gbw2"]


def fetch(node_id: str) -> None:
    fetch_family(node_id, RESOURCES)


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
