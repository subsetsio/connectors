-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Local Authority" AS local_authority,
    "Disabled or non-disabled people" AS disabled_or_non_disabled_people,
    "Age group" AS age_group,
    "Notes" AS notes
FROM "statswales-54e5cbcf-adf2-4484-95e7-76e03c8a33c4"
