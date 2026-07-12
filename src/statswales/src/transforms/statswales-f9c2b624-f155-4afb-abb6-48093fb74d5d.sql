-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "School" AS school,
    "Age group" AS age_group,
    "Sex" AS sex,
    "Notes" AS notes
FROM "statswales-f9c2b624-f155-4afb-abb6-48093fb74d5d"
