-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Time Period" AS time_period,
    "Local Authority" AS local_authority,
    "Notes" AS notes
FROM "statswales-bda840af-9f93-41ab-b4a3-05625dac39b8"
