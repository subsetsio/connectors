-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The document index does not expose a stable unique row identifier; duplicate document rows can occur and should not be collapsed without a query-specific rule.
SELECT
    CAST("TYPE-COLLATERAL" AS BIGINT) AS type_collateral,
    "COLLATERAL" AS collateral,
    "PARTY" AS party,
    "DOC-ID" AS doc_id,
    strptime("DRDATE", '%Y%m%d')::DATE AS drdate,
    strptime("PROCESSING-DATE", '%Y%m%d')::DATE AS processing_date,
    "CORR-DATE" AS corr_date,
    "CORR-ID" AS corr_id,
    "SERIAL-ID" AS serial_id,
    "DOC-TYPE" AS doc_type
FROM "faa-docindex"
