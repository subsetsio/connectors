-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Year" AS BIGINT) AS year,
    CAST("Value" AS DOUBLE) AS value,
    "Units" AS units,
    "Bacteria" AS bacteria,
    "Topic" AS topic,
    "ViewBy" AS viewby,
    "ViewBy2" AS viewby2
FROM "cdc-uxwq-vny5"
