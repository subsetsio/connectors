-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Local Authority" AS local_authority,
    "Year" AS year,
    "Staff group" AS staff_group,
    "Notes" AS notes
FROM "statswales-48b3f47c-8bd7-462b-9c64-7218a0bb488e"
