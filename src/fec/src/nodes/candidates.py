"""FEC candidates: weball (financial summary, driver) LEFT JOIN cn (master,
for office + principal committee) per cycle, joined inside the download so the
SQL transform stays a thin cast/rename pass."""

from __future__ import annotations

import os

import duckdb
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import _bytes_to_tempfile, _csv_clause, _cycles, _zip_member_bytes

WEBALL_COLS = [
    "CAND_ID", "CAND_NAME", "CAND_ICI", "PTY_CD", "CAND_PTY_AFFILIATION",
    "TTL_RECEIPTS", "TRANS_FROM_AUTH", "TTL_DISB", "TRANS_TO_AUTH", "COH_BOP",
    "COH_COP", "CAND_CONTRIB", "CAND_LOANS", "OTHER_LOANS", "CAND_LOAN_REPAY",
    "OTHER_LOAN_REPAY", "DEBTS_OWED_BY", "TTL_INDIV_CONTRIB", "CAND_OFFICE_ST",
    "CAND_OFFICE_DISTRICT", "SPEC_ELECTION", "PRIM_ELECTION", "RUN_ELECTION",
    "GEN_ELECTION", "GEN_ELECTION_PRECENT", "OTHER_POL_CMTE_CONTRIB",
    "POL_PTY_CONTRIB", "CVG_END_DT", "INDIV_REFUNDS", "CMTE_REFUNDS",
]

CN_COLS = [
    "CAND_ID", "CAND_NAME", "CAND_PTY_AFFILIATION", "CAND_ELECTION_YR",
    "CAND_OFFICE_ST", "CAND_OFFICE", "CAND_OFFICE_DISTRICT", "CAND_ICI",
    "CAND_STATUS", "CAND_PCC", "CAND_ST1", "CAND_ST2", "CAND_CITY", "CAND_ST",
    "CAND_ZIP",
]

_OFFICE_CASE = (
    "CASE CN_OFFICE WHEN 'H' THEN 'House' WHEN 'S' THEN 'Senate' "
    "WHEN 'P' THEN 'President' ELSE CN_OFFICE END"
)
_ICI_CASE = (
    "CASE CAND_ICI WHEN 'I' THEN 'Incumbent' WHEN 'C' THEN 'Challenger' "
    "WHEN 'O' THEN 'Open Seat' ELSE CAND_ICI END"
)


def fetch_candidates(node_id: str) -> None:
    """weball (financial summary, driver) LEFT JOIN cn (master, for office +
    principal committee) per cycle, joined inside the download so the transform
    stays thin."""
    parts = []
    for cycle in _cycles():
        wb = _zip_member_bytes(cycle, "weball")
        if wb is None:
            print(f"  {node_id}: weball {cycle} not published, skipping")
            continue
        cn = _zip_member_bytes(cycle, "cn")
        wb_path = _bytes_to_tempfile(wb)
        cn_path = _bytes_to_tempfile(cn) if cn is not None else None
        try:
            if cn_path is not None:
                cn_sub = (
                    f"(SELECT CAND_ID, ANY_VALUE(CAND_OFFICE) AS CAND_OFFICE, "
                    f"ANY_VALUE(CAND_PCC) AS CAND_PCC "
                    f"FROM {_csv_clause(cn_path, CN_COLS)} GROUP BY CAND_ID)"
                )
                sql = (
                    f"SELECT '{cycle}' AS cycle, w.*, "
                    f"c.CAND_OFFICE AS CN_OFFICE, c.CAND_PCC AS CN_PCC "
                    f"FROM {_csv_clause(wb_path, WEBALL_COLS)} w "
                    f"LEFT JOIN {cn_sub} c ON w.CAND_ID = c.CAND_ID"
                )
            else:
                sql = (
                    f"SELECT '{cycle}' AS cycle, w.*, "
                    f"NULL AS CN_OFFICE, NULL AS CN_PCC "
                    f"FROM {_csv_clause(wb_path, WEBALL_COLS)} w"
                )
            tbl = duckdb.sql(sql).to_arrow_table()
            parts.append(tbl)
            print(f"  {node_id}: {cycle} -> {tbl.num_rows:,} rows")
        finally:
            os.unlink(wb_path)
            if cn_path is not None:
                os.unlink(cn_path)
    if not parts:
        raise RuntimeError(f"{node_id}: no cycles fetched")
    save_raw_parquet(pa.concat_tables(parts), node_id)


DOWNLOAD_SPECS = []

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="fec-candidates-transform",
        deps=["fec-candidates"],
        sql=f"""
            SELECT
                cycle,
                CAND_ID                                       AS cand_id,
                CAND_NAME                                     AS cand_name,
                CAND_PTY_AFFILIATION                          AS party,
                {_OFFICE_CASE}                                AS office,
                CAND_OFFICE_ST                                AS state,
                CAND_OFFICE_DISTRICT                          AS district,
                {_ICI_CASE}                                   AS incumbent_challenger,
                CN_PCC                                        AS principal_cmte_id,
                TRY_CAST(TTL_RECEIPTS AS DOUBLE)              AS total_receipts,
                TRY_CAST(TTL_DISB AS DOUBLE)                  AS total_disbursements,
                TRY_CAST(TTL_INDIV_CONTRIB AS DOUBLE)         AS total_individual_contrib,
                TRY_CAST(OTHER_POL_CMTE_CONTRIB AS DOUBLE)    AS other_cmte_contrib,
                TRY_CAST(POL_PTY_CONTRIB AS DOUBLE)           AS party_contrib,
                TRY_CAST(CAND_CONTRIB AS DOUBLE)              AS cand_contributions,
                TRY_CAST(CAND_LOANS AS DOUBLE)               AS cand_loans,
                TRY_CAST(COH_COP AS DOUBLE)                   AS cash_on_hand_end,
                TRY_CAST(DEBTS_OWED_BY AS DOUBLE)             AS debts_owed_by,
                TRY_STRPTIME(CVG_END_DT, '%m/%d/%Y')::DATE    AS coverage_end_date
            FROM "fec-candidates"
            WHERE CAND_ID IS NOT NULL AND CAND_ID <> ''
            QUALIFY row_number() OVER (
                PARTITION BY cycle, CAND_ID
                ORDER BY TRY_CAST(TTL_RECEIPTS AS DOUBLE) DESC NULLS LAST
            ) = 1
        """,
    ),
]
