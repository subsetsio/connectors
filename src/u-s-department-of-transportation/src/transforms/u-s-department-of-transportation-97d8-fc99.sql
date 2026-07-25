-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("report_date" AS TIMESTAMP) AS report_date,
    "manufacturer",
    "accounting_category",
    CAST("number_of_inflators" AS BIGINT) AS number_of_inflators,
    CAST("percent_of_accounting_category" AS DOUBLE) AS percent_of_accounting_category
FROM "u-s-department-of-transportation-97d8-fc99"
