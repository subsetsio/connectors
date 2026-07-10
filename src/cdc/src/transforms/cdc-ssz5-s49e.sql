-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("YearName" AS BIGINT) AS yearname,
    "Topic" AS topic,
    "ViewBy" AS viewby,
    "Series" AS series,
    CAST("Value" AS DOUBLE) AS value
FROM "cdc-ssz5-s49e"
