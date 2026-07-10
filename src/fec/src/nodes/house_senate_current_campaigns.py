"""FEC House/Senate current campaigns (webl): headerless pipe file with the
same column layout as weball, fetched across all cycles via the shared simple
loader."""

from __future__ import annotations

from subsets_utils import NodeSpec, SqlNodeSpec
from utils import _save_simple

# House/Senate current campaigns: identical layout to weball.
WEBL_COLS = [
    "CAND_ID", "CAND_NAME", "CAND_ICI", "PTY_CD", "CAND_PTY_AFFILIATION",
    "TTL_RECEIPTS", "TRANS_FROM_AUTH", "TTL_DISB", "TRANS_TO_AUTH", "COH_BOP",
    "COH_COP", "CAND_CONTRIB", "CAND_LOANS", "OTHER_LOANS", "CAND_LOAN_REPAY",
    "OTHER_LOAN_REPAY", "DEBTS_OWED_BY", "TTL_INDIV_CONTRIB", "CAND_OFFICE_ST",
    "CAND_OFFICE_DISTRICT", "SPEC_ELECTION", "PRIM_ELECTION", "RUN_ELECTION",
    "GEN_ELECTION", "GEN_ELECTION_PRECENT", "OTHER_POL_CMTE_CONTRIB",
    "POL_PTY_CONTRIB", "CVG_END_DT", "INDIV_REFUNDS", "CMTE_REFUNDS",
]

_ICI_CASE = (
    "CASE CAND_ICI WHEN 'I' THEN 'Incumbent' WHEN 'C' THEN 'Challenger' "
    "WHEN 'O' THEN 'Open Seat' ELSE CAND_ICI END"
)


def fetch_house_senate(node_id: str) -> None:
    _save_simple(node_id, "webl", WEBL_COLS)


DOWNLOAD_SPECS = []

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="fec-house-senate-current-campaigns-transform",
        deps=["fec-house-senate-current-campaigns"],
        sql=f"""
            SELECT
                cycle,
                CAND_ID                                       AS cand_id,
                CAND_NAME                                     AS cand_name,
                CAND_PTY_AFFILIATION                          AS party,
                CAND_OFFICE_ST                                AS state,
                CAND_OFFICE_DISTRICT                          AS district,
                {_ICI_CASE}                                   AS incumbent_challenger,
                TRY_CAST(TTL_RECEIPTS AS DOUBLE)              AS total_receipts,
                TRY_CAST(TTL_DISB AS DOUBLE)                  AS total_disbursements,
                TRY_CAST(TTL_INDIV_CONTRIB AS DOUBLE)         AS total_individual_contrib,
                TRY_CAST(OTHER_POL_CMTE_CONTRIB AS DOUBLE)    AS other_cmte_contrib,
                TRY_CAST(POL_PTY_CONTRIB AS DOUBLE)           AS party_contrib,
                TRY_CAST(COH_COP AS DOUBLE)                   AS cash_on_hand_end,
                TRY_CAST(DEBTS_OWED_BY AS DOUBLE)             AS debts_owed_by,
                TRY_STRPTIME(CVG_END_DT, '%m/%d/%Y')::DATE    AS coverage_end_date
            FROM "fec-house-senate-current-campaigns"
            WHERE CAND_ID IS NOT NULL AND CAND_ID <> ''
            QUALIFY row_number() OVER (
                PARTITION BY cycle, CAND_ID
                ORDER BY TRY_CAST(TTL_RECEIPTS AS DOUBLE) DESC NULLS LAST
            ) = 1
        """,
    ),
]
