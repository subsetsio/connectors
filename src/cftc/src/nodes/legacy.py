"""CFTC Legacy COT — Futures-Only (6dca-aqww) + Combined (jun7-fc8e), back to 1986."""
from subsets_utils import NodeSpec, SqlNodeSpec

from utils import COMMON_COLS, fetch_family

RESOURCES = ["6dca-aqww", "jun7-fc8e"]


def fetch(node_id: str) -> None:
    fetch_family(node_id, RESOURCES)


DOWNLOAD_SPECS = [NodeSpec(id="cftc-legacy", fn=fetch, kind="download")]

_SQL = f'''
    SELECT
        {COMMON_COLS},
        futonly_or_combined                                AS report_type,
        TRY_CAST(change_in_open_interest_all AS DOUBLE)    AS change_in_open_interest,
        TRY_CAST(noncomm_positions_long_all AS DOUBLE)     AS noncommercial_long,
        TRY_CAST(noncomm_positions_short_all AS DOUBLE)    AS noncommercial_short,
        TRY_CAST(noncomm_postions_spread_all AS DOUBLE)    AS noncommercial_spread,
        TRY_CAST(comm_positions_long_all AS DOUBLE)        AS commercial_long,
        TRY_CAST(comm_positions_short_all AS DOUBLE)       AS commercial_short,
        TRY_CAST(conc_net_le_4_tdr_long_all AS DOUBLE)     AS conc_net_4_long_pct,
        TRY_CAST(conc_net_le_4_tdr_short_all AS DOUBLE)    AS conc_net_4_short_pct,
        TRY_CAST(conc_net_le_8_tdr_long_all AS DOUBLE)     AS conc_net_8_long_pct,
        TRY_CAST(conc_net_le_8_tdr_short_all AS DOUBLE)    AS conc_net_8_short_pct
    FROM "cftc-legacy"
    WHERE report_date_as_yyyy_mm_dd IS NOT NULL
'''

TRANSFORM_SPECS = [
    SqlNodeSpec(id="cftc-legacy-transform", deps=["cftc-legacy"], sql=_SQL)
]
