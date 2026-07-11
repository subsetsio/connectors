-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Indicator" AS indicator,
    strptime("Year", '%Y-%m')::DATE AS year,
    "value",
    "unit"
FROM "nso-mongolia-dt-nso-2001-035v1"
