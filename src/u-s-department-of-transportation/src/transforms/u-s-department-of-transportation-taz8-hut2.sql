-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("fiscal_year" AS BIGINT) AS fiscal_year,
    CAST("receipts" AS BIGINT) AS receipts,
    CAST("expenditures" AS BIGINT) AS expenditures,
    CAST("balance" AS BIGINT) AS balance
FROM "u-s-department-of-transportation-taz8-hut2"
