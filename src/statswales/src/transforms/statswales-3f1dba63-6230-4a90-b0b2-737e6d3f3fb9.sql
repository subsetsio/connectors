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
FROM "statswales-3f1dba63-6230-4a90-b0b2-737e6d3f3fb9"
