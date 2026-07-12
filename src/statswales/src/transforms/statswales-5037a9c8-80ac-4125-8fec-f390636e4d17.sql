-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Area of residence" AS area_of_residence,
    "Age" AS age,
    "Country of birth (outside the UK)" AS country_of_birth_outside_the_uk,
    "Notes" AS notes
FROM "statswales-5037a9c8-80ac-4125-8fec-f390636e4d17"
