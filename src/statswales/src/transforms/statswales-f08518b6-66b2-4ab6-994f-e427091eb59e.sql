-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Family type" AS family_type,
    "Time period" AS time_period,
    "Notes" AS notes
FROM "statswales-f08518b6-66b2-4ab6-994f-e427091eb59e"
