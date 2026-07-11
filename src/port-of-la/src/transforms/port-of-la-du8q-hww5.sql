-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "fiscal_year",
    "account_name",
    CAST("appropriation_amount" AS DOUBLE) AS appropriation_amount,
    "expense_categories"
FROM "port-of-la-du8q-hww5"
