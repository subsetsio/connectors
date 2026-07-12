-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Local Authority" AS local_authority,
    "Age group" AS age_group,
    "Sex" AS sex,
    "Notes" AS notes
FROM "statswales-a1fc1a7e-b255-4b16-9f2e-9ffe4a241ed2"
