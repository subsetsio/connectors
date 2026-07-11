-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Type" AS type,
    strptime("Monthly", '%Y-%m')::DATE AS monthly,
    "value",
    "unit"
FROM "nso-mongolia-dt-nso-2026-31v1"
