-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Memo and subitemization rows can describe underlying spending details; exclude memo-coded rows when computing disbursement totals that should avoid double counting.
SELECT
    CAST("cycle" AS BIGINT) AS cycle,
    "CMTE_ID" AS cmte_id,
    "AMNDT_IND" AS amndt_ind,
    CAST("RPT_YR" AS BIGINT) AS rpt_yr,
    "RPT_TP" AS rpt_tp,
    CAST("IMAGE_NUM" AS BIGINT) AS image_num,
    "LINE_NUM" AS line_num,
    "FORM_TP_CD" AS form_tp_cd,
    "SCHED_TP_CD" AS sched_tp_cd,
    "NAME" AS name,
    "CITY" AS city,
    "STATE" AS state,
    "ZIP_CODE" AS zip_code,
    strptime("TRANSACTION_DT", '%m/%d/%Y')::DATE AS transaction_dt,
    CAST("TRANSACTION_AMT" AS BIGINT) AS transaction_amt,
    "TRANSACTION_PGI" AS transaction_pgi,
    "PURPOSE" AS purpose,
    "CATEGORY" AS category,
    "CATEGORY_DESC" AS category_desc,
    "MEMO_CD" AS memo_cd,
    "MEMO_TEXT" AS memo_text,
    "ENTITY_TP" AS entity_tp,
    "SUB_ID" AS sub_id,
    CAST("FILE_NUM" AS BIGINT) AS file_num,
    "TRAN_ID" AS tran_id,
    "BACK_REF_TRAN_ID" AS back_ref_tran_id
FROM "fec-operating-expenditures"
