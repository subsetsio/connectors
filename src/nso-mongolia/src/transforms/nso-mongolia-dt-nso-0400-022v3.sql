-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Sex" AS sex,
    "Sector" AS sector,
    strptime("Month", '%Y-%m')::DATE AS month,
    "value",
    "unit"
FROM "nso-mongolia-dt-nso-0400-022v3"
