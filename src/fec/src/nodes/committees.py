"""FEC committees: webk (PAC/party financial summary, driver) LEFT JOIN cm
(committee master, for org type / connected org / affiliation / associated
candidate) per cycle, joined inside the download so the SQL transform stays a
thin cast/rename pass."""

from __future__ import annotations

import os

import duckdb
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import _bytes_to_tempfile, _csv_clause, _cycles, _zip_member_bytes

WEBK_COLS = [
    "CMTE_ID", "CMTE_NM", "CMTE_TP", "CMTE_DSGN", "CMTE_FILING_FREQ",
    "TTL_RECEIPTS", "TRANS_FROM_AFF", "INDV_CONTRIB", "OTHER_POL_CMTE_CONTRIB",
    "CAND_CONTRIB", "CAND_LOANS", "TTL_LOANS_RECEIVED", "TTL_DISB",
    "TRANF_TO_AFF", "INDV_REFUNDS", "OTHER_POL_CMTE_REFUNDS", "CAND_LOAN_REPAY",
    "LOAN_REPAY", "COH_BOP", "COH_COP", "DEBTS_OWED_BY", "NONFED_TRANS_RECEIVED",
    "CONTRIB_TO_OTHER_CMTE", "IND_EXP", "PTY_COORD_EXP", "NONFED_SHARE_EXP",
    "CVG_END_DT",
]

CM_COLS = [
    "CMTE_ID", "CMTE_NM", "TRES_NM", "CMTE_ST1", "CMTE_ST2", "CMTE_CITY",
    "CMTE_ST", "CMTE_ZIP", "CMTE_DSGN", "CMTE_TP", "CMTE_PTY_AFFILIATION",
    "CMTE_FILING_FREQ", "ORG_TP", "CONNECTED_ORG_NM", "CAND_ID",
]


def fetch_committees(node_id: str) -> None:
    """webk (PAC/party financial summary, driver) LEFT JOIN cm (committee
    master, for org type / connected org / affiliation / associated candidate)
    per cycle."""
    parts = []
    for cycle in _cycles():
        wk = _zip_member_bytes(cycle, "webk")
        if wk is None:
            print(f"  {node_id}: webk {cycle} not published, skipping")
            continue
        cm = _zip_member_bytes(cycle, "cm")
        wk_path = _bytes_to_tempfile(wk)
        cm_path = _bytes_to_tempfile(cm) if cm is not None else None
        try:
            if cm_path is not None:
                cm_sub = (
                    f"(SELECT CMTE_ID, "
                    f"ANY_VALUE(CMTE_PTY_AFFILIATION) AS CMTE_PTY_AFFILIATION, "
                    f"ANY_VALUE(CMTE_ST) AS CMTE_ST, "
                    f"ANY_VALUE(ORG_TP) AS ORG_TP, "
                    f"ANY_VALUE(CONNECTED_ORG_NM) AS CONNECTED_ORG_NM, "
                    f"ANY_VALUE(CAND_ID) AS CAND_ID "
                    f"FROM {_csv_clause(cm_path, CM_COLS)} GROUP BY CMTE_ID)"
                )
                sql = (
                    f"SELECT '{cycle}' AS cycle, k.*, "
                    f"m.CMTE_PTY_AFFILIATION AS CM_PTY, m.CMTE_ST AS CM_ST, "
                    f"m.ORG_TP AS CM_ORG_TP, "
                    f"m.CONNECTED_ORG_NM AS CM_CONNECTED_ORG, "
                    f"m.CAND_ID AS CM_CAND_ID "
                    f"FROM {_csv_clause(wk_path, WEBK_COLS)} k "
                    f"LEFT JOIN {cm_sub} m ON k.CMTE_ID = m.CMTE_ID"
                )
            else:
                sql = (
                    f"SELECT '{cycle}' AS cycle, k.*, "
                    f"NULL AS CM_PTY, NULL AS CM_ST, NULL AS CM_ORG_TP, "
                    f"NULL AS CM_CONNECTED_ORG, NULL AS CM_CAND_ID "
                    f"FROM {_csv_clause(wk_path, WEBK_COLS)} k"
                )
            tbl = duckdb.sql(sql).to_arrow_table()
            parts.append(tbl)
            print(f"  {node_id}: {cycle} -> {tbl.num_rows:,} rows")
        finally:
            os.unlink(wk_path)
            if cm_path is not None:
                os.unlink(cm_path)
    if not parts:
        raise RuntimeError(f"{node_id}: no cycles fetched")
    save_raw_parquet(pa.concat_tables(parts), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="fec-committees", fn=fetch_committees, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="fec-committees-transform",
        deps=["fec-committees"],
        sql="""
            SELECT
                cycle,
                CMTE_ID                                       AS cmte_id,
                CMTE_NM                                       AS cmte_name,
                CMTE_TP                                       AS cmte_type,
                CMTE_DSGN                                     AS cmte_designation,
                CM_PTY                                        AS party,
                CM_ST                                         AS state,
                CM_ORG_TP                                     AS org_type,
                CM_CONNECTED_ORG                              AS connected_org,
                CM_CAND_ID                                    AS cand_id,
                TRY_CAST(TTL_RECEIPTS AS DOUBLE)              AS total_receipts,
                TRY_CAST(TTL_DISB AS DOUBLE)                  AS total_disbursements,
                TRY_CAST(INDV_CONTRIB AS DOUBLE)             AS individual_contrib,
                TRY_CAST(OTHER_POL_CMTE_CONTRIB AS DOUBLE)    AS other_cmte_contrib,
                TRY_CAST(CONTRIB_TO_OTHER_CMTE AS DOUBLE)     AS contrib_to_other_cmte,
                TRY_CAST(IND_EXP AS DOUBLE)                   AS independent_expenditures,
                TRY_CAST(PTY_COORD_EXP AS DOUBLE)             AS party_coordinated_exp,
                TRY_CAST(COH_COP AS DOUBLE)                   AS cash_on_hand_end,
                TRY_CAST(DEBTS_OWED_BY AS DOUBLE)             AS debts_owed_by,
                TRY_STRPTIME(CVG_END_DT, '%m/%d/%Y')::DATE    AS coverage_end_date
            FROM "fec-committees"
            WHERE CMTE_ID IS NOT NULL AND CMTE_ID <> ''
            QUALIFY row_number() OVER (
                PARTITION BY cycle, CMTE_ID
                ORDER BY TRY_CAST(TTL_RECEIPTS AS DOUBLE) DESC NULLS LAST
            ) = 1
        """,
    ),
]
