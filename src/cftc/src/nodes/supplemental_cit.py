"""CFTC Supplemental CIT COT — Combined only (4zgm-a668), back to 2006.

CIT is combined-only (no futonly_or_combined column) and uses mixed-case names
for the no-CIT commercial/non-commercial breakdown.
"""
from subsets_utils import NodeSpec, SqlNodeSpec

from utils import COMMON_COLS, fetch_family

RESOURCES = ["4zgm-a668"]


def fetch(node_id: str) -> None:
    fetch_family(node_id, RESOURCES)


DOWNLOAD_SPECS = [NodeSpec(id="cftc-supplemental-cit", fn=fetch, kind="download")]

_SQL = f'''
    SELECT
        {COMMON_COLS},
        'Combined'                                            AS report_type,
        TRY_CAST(change_open_interest_all AS DOUBLE)          AS change_in_open_interest,
        TRY_CAST(cit_positions_long_all AS DOUBLE)            AS index_trader_long,
        TRY_CAST(cit_positions_short_all AS DOUBLE)           AS index_trader_short,
        TRY_CAST("NComm_Postions_Long_All_NoCIT" AS DOUBLE)   AS noncommercial_long_excl_cit,
        TRY_CAST("NComm_Postions_Short_All_NoCIT" AS DOUBLE)  AS noncommercial_short_excl_cit,
        TRY_CAST("NComm_Postions_Spread_All_NoCIT" AS DOUBLE) AS noncommercial_spread_excl_cit,
        TRY_CAST(comm_positions_long_all_nocit AS DOUBLE)     AS commercial_long_excl_cit,
        TRY_CAST("Comm_Positions_Short_All_NoCIT" AS DOUBLE)  AS commercial_short_excl_cit
    FROM "cftc-supplemental-cit"
    WHERE report_date_as_yyyy_mm_dd IS NOT NULL
'''

TRANSFORM_SPECS = [
    SqlNodeSpec(id="cftc-supplemental-cit-transform", deps=["cftc-supplemental-cit"], sql=_SQL)
]
