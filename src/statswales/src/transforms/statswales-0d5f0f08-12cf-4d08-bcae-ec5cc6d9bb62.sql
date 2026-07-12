-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Date" AS date,
    "Area" AS area,
    "Type of vehicle" AS type_of_vehicle,
    "Age of driver" AS age_of_driver,
    "Sex of driver" AS sex_of_driver,
    "Hit and run" AS hit_and_run,
    "Notes" AS notes
FROM "statswales-0d5f0f08-12cf-4d08-bcae-ec5cc6d9bb62"
