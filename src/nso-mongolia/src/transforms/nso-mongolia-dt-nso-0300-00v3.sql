-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "District" AS district,
    strptime("Quarter", '%Y-%m')::DATE AS quarter,
    "value",
    "unit"
FROM "nso-mongolia-dt-nso-0300-00v3"
