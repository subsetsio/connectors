-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Area" AS area,
    "Gender identity" AS gender_identity,
    "Age group" AS age_group,
    "Notes" AS notes
FROM "statswales-6631b74b-dfcf-4db4-a4f4-e0c38f7b9a31"
