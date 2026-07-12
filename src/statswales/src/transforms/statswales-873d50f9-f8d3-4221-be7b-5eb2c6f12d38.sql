-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Local Authority" AS local_authority,
    "Sector" AS sector,
    "Sex" AS sex,
    "Tenure" AS tenure,
    "Allowance type" AS allowance_type,
    "Notes" AS notes
FROM "statswales-873d50f9-f8d3-4221-be7b-5eb2c6f12d38"
