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
