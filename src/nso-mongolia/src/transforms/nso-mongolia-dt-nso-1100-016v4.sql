-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Statistical indicator" AS statistical_indicator,
    "Sector" AS sector,
    "Time" AS time,
    "value",
    "unit"
FROM "nso-mongolia-dt-nso-1100-016v4"
