-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Area" AS area,
    "Initial assessment within 10 weeks" AS initial_assessment_within_10_weeks,
    "Mental health condition reported" AS mental_health_condition_reported,
    "BMI" AS bmi,
    "Notes" AS notes
FROM "statswales-26c2f5be-c556-4739-83e0-5d0cfbc92205"
