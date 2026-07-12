-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Head of household used a foodbank" AS head_of_household_used_a_foodbank,
    "Time period" AS time_period,
    "Notes" AS notes
FROM "statswales-edd58442-c7b6-480e-9578-891d51930c3c"
