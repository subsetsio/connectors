-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Patient type" AS patient_type,
    "Treatment band" AS treatment_band,
    "Prescribed item" AS prescribed_item,
    "Year" AS year,
    "Notes" AS notes
FROM "statswales-91c5089f-4a8a-4a1f-b8e8-b7acaed57912"
