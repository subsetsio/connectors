-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Statistical indicator" AS statistical_indicator,
    "Composition" AS composition,
    "Time (Quarterly)" AS time_quarterly,
    "value",
    "unit"
FROM "nso-mongolia-dt-nso-0500-004v1"
