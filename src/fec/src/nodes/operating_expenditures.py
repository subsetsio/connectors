"""FEC operating expenditures (oppexp): large headerless pipe file streamed
cycle-by-cycle into batched parquet via the shared streaming loader; per-cycle
state makes it resumable."""

from __future__ import annotations

from subsets_utils import NodeSpec, SqlNodeSpec
from utils import _fetch_stream

OPPEXP_COLS = [
    "CMTE_ID", "AMNDT_IND", "RPT_YR", "RPT_TP", "IMAGE_NUM", "LINE_NUM",
    "FORM_TP_CD", "SCHED_TP_CD", "NAME", "CITY", "STATE", "ZIP_CODE",
    "TRANSACTION_DT", "TRANSACTION_AMT", "TRANSACTION_PGI", "PURPOSE",
    "CATEGORY", "CATEGORY_DESC", "MEMO_CD", "MEMO_TEXT", "ENTITY_TP", "SUB_ID",
    "FILE_NUM", "TRAN_ID", "BACK_REF_TRAN_ID",
]


def fetch_operating_expenditures(node_id: str) -> None:
    _fetch_stream(node_id, "oppexp", OPPEXP_COLS)


DOWNLOAD_SPECS = [
    NodeSpec(id="fec-operating-expenditures", fn=fetch_operating_expenditures, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="fec-operating-expenditures-transform",
        deps=["fec-operating-expenditures"],
        sql="""
            SELECT
                cycle,
                SUB_ID                                    AS sub_id,
                CMTE_ID                                   AS cmte_id,
                NAME                                      AS payee_name,
                CITY                                      AS city,
                STATE                                     AS state,
                ZIP_CODE                                  AS zip_code,
                TRY_STRPTIME(TRANSACTION_DT, '%m/%d/%Y')::DATE AS transaction_date,
                TRY_CAST(TRANSACTION_AMT AS DOUBLE)       AS amount,
                PURPOSE                                   AS purpose,
                CATEGORY                                  AS category,
                CATEGORY_DESC                             AS category_desc,
                FORM_TP_CD                                AS form_type,
                SCHED_TP_CD                               AS schedule_type,
                LINE_NUM                                  AS line_num,
                ENTITY_TP                                 AS entity_type,
                TRAN_ID                                   AS tran_id,
                TRY_CAST(FILE_NUM AS BIGINT)              AS file_num,
                IMAGE_NUM                                 AS image_num,
                MEMO_CD                                   AS memo_code,
                MEMO_TEXT                                 AS memo_text,
                AMNDT_IND                                 AS amendment_ind,
                RPT_TP                                    AS report_type,
                TRANSACTION_PGI                           AS transaction_pgi
            FROM "fec-operating-expenditures"
            WHERE SUB_ID IS NOT NULL AND SUB_ID <> ''
        """,
    ),
]
