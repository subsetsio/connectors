-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "TOTAL" AS total,
    CAST("TIME (Annual)" AS BIGINT) AS time_annual,
    "value",
    "unit"
FROM "nso-mongolia-dt-nso-1001-001v1"
