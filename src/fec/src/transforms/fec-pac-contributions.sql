-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Amounts include direct contributions, coordinated expenditures, refunds, and earmarked activity; group by transaction type before interpreting totals as candidate support.
SELECT
    CAST("cycle" AS BIGINT) AS cycle,
    "CMTE_ID" AS cmte_id,
    "AMNDT_IND" AS amndt_ind,
    "RPT_TP" AS rpt_tp,
    "TRANSACTION_PGI" AS transaction_pgi,
    "IMAGE_NUM" AS image_num,
    "TRANSACTION_TP" AS transaction_tp,
    "ENTITY_TP" AS entity_tp,
    "NAME" AS name,
    "CITY" AS city,
    "STATE" AS state,
    "ZIP_CODE" AS zip_code,
    "EMPLOYER" AS employer,
    "OCCUPATION" AS occupation,
    strptime("TRANSACTION_DT", '%m%d%Y')::DATE AS transaction_dt,
    CAST("TRANSACTION_AMT" AS BIGINT) AS transaction_amt,
    "OTHER_ID" AS other_id,
    "CAND_ID" AS cand_id,
    "TRAN_ID" AS tran_id,
    CAST("FILE_NUM" AS BIGINT) AS file_num,
    "MEMO_CD" AS memo_cd,
    "MEMO_TEXT" AS memo_text,
    "SUB_ID" AS sub_id
FROM "fec-pac-contributions"
