-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Patient type" AS patient_type,
    "Treatment band" AS treatment_band,
    "Clinical item" AS clinical_item,
    "Notes" AS notes
FROM "statswales-1b593099-9033-42df-9a2e-4d529932c340"
