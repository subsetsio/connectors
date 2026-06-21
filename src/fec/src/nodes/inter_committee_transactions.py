"""FEC inter-committee transactions (oth): large headerless pipe file streamed
cycle-by-cycle into batched parquet via the shared streaming loader; per-cycle
state makes it resumable."""

from __future__ import annotations

from subsets_utils import NodeSpec, SqlNodeSpec
from utils import _fetch_stream

OTH_COLS = [
    "CMTE_ID", "AMNDT_IND", "RPT_TP", "TRANSACTION_PGI", "IMAGE_NUM",
    "TRANSACTION_TP", "ENTITY_TP", "NAME", "CITY", "STATE", "ZIP_CODE",
    "EMPLOYER", "OCCUPATION", "TRANSACTION_DT", "TRANSACTION_AMT", "OTHER_ID",
    "TRAN_ID", "FILE_NUM", "MEMO_CD", "MEMO_TEXT", "SUB_ID",
]


def fetch_inter_committee(node_id: str) -> None:
    _fetch_stream(node_id, "oth", OTH_COLS)


DOWNLOAD_SPECS = [
    NodeSpec(id="fec-inter-committee-transactions", fn=fetch_inter_committee, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="fec-inter-committee-transactions-transform",
        deps=["fec-inter-committee-transactions"],
        sql="""
            SELECT
                cycle,
                SUB_ID                                    AS sub_id,
                CMTE_ID                                   AS cmte_id,
                OTHER_ID                                  AS other_id,
                NAME                                      AS name,
                ENTITY_TP                                 AS entity_type,
                TRANSACTION_TP                            AS transaction_type,
                TRY_STRPTIME(TRANSACTION_DT, '%m%d%Y')::DATE AS transaction_date,
                TRY_CAST(TRANSACTION_AMT AS DOUBLE)       AS amount,
                CITY                                      AS city,
                STATE                                     AS state,
                ZIP_CODE                                  AS zip_code,
                TRAN_ID                                   AS tran_id,
                TRY_CAST(FILE_NUM AS BIGINT)              AS file_num,
                MEMO_CD                                   AS memo_code,
                MEMO_TEXT                                 AS memo_text,
                AMNDT_IND                                 AS amendment_ind,
                RPT_TP                                    AS report_type,
                TRANSACTION_PGI                           AS transaction_pgi,
                IMAGE_NUM                                 AS image_num
            FROM "fec-inter-committee-transactions"
            WHERE SUB_ID IS NOT NULL AND SUB_ID <> ''
        """,
    ),
]
