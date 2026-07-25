-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "receipt_disbursement",
    "type",
    CAST("dollars" AS BIGINT) AS dollars,
    CAST("percent" AS DOUBLE) AS percent
FROM "u-s-department-of-transportation-amq9-vv6k"
