-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Vessel" AS vessel,
    "Welsh port" AS welsh_port,
    "Notes" AS notes
FROM "statswales-fbe356c8-383a-4877-8e9b-a87380c7d952"
