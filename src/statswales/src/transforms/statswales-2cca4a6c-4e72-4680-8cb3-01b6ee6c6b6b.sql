-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Local Authority" AS local_authority,
    "Age Group" AS age_group,
    "Gender" AS gender,
    "Ethnicity" AS ethnicity,
    "Disability" AS disability,
    "Notes" AS notes
FROM "statswales-2cca4a6c-4e72-4680-8cb3-01b6ee6c6b6b"
