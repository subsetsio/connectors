-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Statistical Indicator" AS statistical_indicator,
    "Components" AS components,
    "year",
    "value",
    "unit"
FROM "nso-mongolia-dt-nso-0500-022v2"
