-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "case_number",
    strptime("issue_date", '%m/%d/%Y')::DATE AS issue_date,
    "check_number",
    "bbl",
    strptime("effectivedate", '%m/%d/%Y')::DATE AS effectivedate,
    CAST("refund_year" AS BIGINT) AS refund_year,
    CAST("refund_number" AS BIGINT) AS refund_number,
    CAST("amount" AS DOUBLE) AS amount
FROM "nyc-open-data-w5ea-ydu3"
