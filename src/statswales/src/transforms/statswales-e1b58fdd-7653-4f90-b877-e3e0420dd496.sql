-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Area" AS area,
    "Place of birth" AS place_of_birth,
    "Birthweight" AS birthweight,
    "Ethnic group" AS ethnic_group,
    "Gestational age completed weeks" AS gestational_age_completed_weeks,
    "Age of mother" AS age_of_mother,
    "Number of babies" AS number_of_babies,
    "Notes" AS notes
FROM "statswales-e1b58fdd-7653-4f90-b877-e3e0420dd496"
