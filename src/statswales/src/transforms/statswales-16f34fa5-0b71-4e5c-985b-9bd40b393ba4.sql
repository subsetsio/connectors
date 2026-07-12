-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Local Authority" AS local_authority,
    "Sector" AS sector,
    "Sex" AS sex,
    "Tenure" AS tenure,
    "Allowance Type" AS allowance_type,
    "Notes" AS notes
FROM "statswales-16f34fa5-0b71-4e5c-985b-9bd40b393ba4"
