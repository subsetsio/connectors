-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Age group" AS age_group,
    "Geography" AS geography,
    "Duration" AS duration,
    CAST("Year" AS BIGINT) AS year,
    "Notes" AS notes
FROM "statswales-dd6076b0-7266-4eab-85b1-40f052125325"
