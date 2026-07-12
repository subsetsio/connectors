-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Area" AS area,
    "Ethnic group" AS ethnic_group,
    "Initial assessment within 10 weeks" AS initial_assessment_within_10_weeks,
    "Mental health condition reported" AS mental_health_condition_reported,
    "BMI" AS bmi,
    "Notes" AS notes
FROM "statswales-abf09161-e544-45fe-be2b-771004ab3522"
