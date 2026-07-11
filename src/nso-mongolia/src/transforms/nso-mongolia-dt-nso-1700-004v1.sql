-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Statistical indicator" AS statistical_indicator,
    "Aimag" AS aimag,
    CAST("TIME" AS BIGINT) AS time,
    "value",
    "unit"
FROM "nso-mongolia-dt-nso-1700-004v1"
