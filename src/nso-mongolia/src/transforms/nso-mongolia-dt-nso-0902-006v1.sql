-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Indicator" AS indicator,
    "Quarter (cumulative)" AS quarter_cumulative,
    "value",
    "unit"
FROM "nso-mongolia-dt-nso-0902-006v1"
