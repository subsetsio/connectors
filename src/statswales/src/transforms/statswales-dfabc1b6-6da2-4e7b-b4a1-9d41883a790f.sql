-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Area" AS area,
    "Birthweight" AS birthweight,
    "Gestational age completed weeks" AS gestational_age_completed_weeks,
    "Age of mother" AS age_of_mother,
    "Number of babies" AS number_of_babies,
    "Notes" AS notes
FROM "statswales-dfabc1b6-6da2-4e7b-b4a1-9d41883a790f"
