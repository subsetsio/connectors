-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Age of head of household" AS age_of_head_of_household,
    "Time period" AS time_period,
    "Notes" AS notes
FROM "statswales-23267d3c-cc76-4f03-bce0-98102eb32062"
