"""FEC individual contributions (indiv): a very large headerless pipe file
(~20GB uncompressed per cycle) streamed cycle-by-cycle into batched parquet via
the shared streaming loader; per-cycle state makes it resumable."""

from __future__ import annotations

from subsets_utils import NodeSpec, SqlNodeSpec
from utils import _fetch_stream

INDIV_COLS = [
    "CMTE_ID", "AMNDT_IND", "RPT_TP", "TRANSACTION_PGI", "IMAGE_NUM",
    "TRANSACTION_TP", "ENTITY_TP", "NAME", "CITY", "STATE", "ZIP_CODE",
    "EMPLOYER", "OCCUPATION", "TRANSACTION_DT", "TRANSACTION_AMT", "OTHER_ID",
    "TRAN_ID", "FILE_NUM", "MEMO_CD", "MEMO_TEXT", "SUB_ID",
]


def fetch_individual_contributions(node_id: str) -> None:
    _fetch_stream(node_id, "indiv", INDIV_COLS)


DOWNLOAD_SPECS = []

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="fec-individual-contributions-transform",
        deps=["fec-individual-contributions"],
        sql="""
            SELECT
                cycle,
                SUB_ID                                    AS sub_id,
                CMTE_ID                                   AS cmte_id,
                NAME                                      AS contributor_name,
                CITY                                      AS city,
                STATE                                     AS state,
                ZIP_CODE                                  AS zip_code,
                EMPLOYER                                  AS employer,
                OCCUPATION                                AS occupation,
                ENTITY_TP                                 AS entity_type,
                TRANSACTION_TP                            AS transaction_type,
                TRY_STRPTIME(TRANSACTION_DT, '%m%d%Y')::DATE AS transaction_date,
                TRY_CAST(TRANSACTION_AMT AS DOUBLE)       AS amount,
                OTHER_ID                                  AS other_id,
                TRAN_ID                                   AS tran_id,
                TRY_CAST(FILE_NUM AS BIGINT)              AS file_num,
                MEMO_CD                                   AS memo_code,
                MEMO_TEXT                                 AS memo_text,
                AMNDT_IND                                 AS amendment_ind,
                RPT_TP                                    AS report_type,
                TRANSACTION_PGI                           AS transaction_pgi,
                IMAGE_NUM                                 AS image_num
            FROM "fec-individual-contributions"
            WHERE SUB_ID IS NOT NULL AND SUB_ID <> ''
        """,
    ),
]
