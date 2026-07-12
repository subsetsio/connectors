-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Patient type" AS patient_type,
    "Treatment band" AS treatment_band,
    "Other clinical activity" AS other_clinical_activity,
    "Year" AS year,
    "Notes" AS notes
FROM "statswales-d6edfc1f-07c6-4640-bb3d-206102bcd3af"
