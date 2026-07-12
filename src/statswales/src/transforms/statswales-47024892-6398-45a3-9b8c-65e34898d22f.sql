-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Age" AS age,
    "Reason for attendance" AS reason_for_attendance,
    "Year" AS year,
    "Notes" AS notes
FROM "statswales-47024892-6398-45a3-9b8c-65e34898d22f"
