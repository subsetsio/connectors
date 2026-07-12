-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Date" AS date,
    "Hospital" AS hospital,
    "Hospital Type" AS hospital_type,
    "Target" AS target,
    "Notes" AS notes
FROM "statswales-3ce1cc28-0625-4674-89d6-9cf3a56f2d9c"
