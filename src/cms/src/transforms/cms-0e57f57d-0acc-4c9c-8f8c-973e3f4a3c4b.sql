-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    "hcpcs_cd",
    CAST("PRICE_AMT" AS DOUBLE) AS price_amt,
    CAST("VOL_TXT" AS BIGINT) AS vol_txt
FROM "cms-0e57f57d-0acc-4c9c-8f8c-973e3f4a3c4b"
