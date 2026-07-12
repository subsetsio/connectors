-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Area" AS area,
    "Age of mother" AS age_of_mother,
    "Initial assessment within 10 weeks" AS initial_assessment_within_10_weeks,
    "Mental health condition reported" AS mental_health_condition_reported,
    "BMI" AS bmi,
    "Notes" AS notes
FROM "statswales-b28de382-19a0-47a3-b3c6-b34311284e49"
