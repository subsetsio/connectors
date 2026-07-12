-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "szenario",
    "geschlecht",
    "bildungsniveau",
    CAST("jahr" AS BIGINT) AS jahr,
    "variablen",
    "value",
    "cube_id",
    "updated"
FROM "federal-statistical-office-px-x-1509090000-201"
