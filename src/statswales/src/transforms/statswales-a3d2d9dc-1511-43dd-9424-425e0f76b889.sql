-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Subject" AS subject,
    "Sex" AS sex,
    "Notes" AS notes
FROM "statswales-a3d2d9dc-1511-43dd-9424-425e0f76b889"
