-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Local Authority" AS local_authority,
    "Sex" AS sex,
    "Boarding Type" AS boarding_type,
    "Notes" AS notes
FROM "statswales-05c7242b-4e5e-42ff-acee-f44e2de5fedd"
