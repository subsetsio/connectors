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
    "Carer status" AS carer_status,
    "Ethnicity" AS ethnicity,
    "Notes" AS notes
FROM "statswales-a0bfe7d4-2653-4690-aaa6-c9a4b40b9c92"
