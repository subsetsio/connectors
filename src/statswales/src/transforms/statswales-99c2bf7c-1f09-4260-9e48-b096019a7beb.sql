-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Area" AS area,
    "Appointment type" AS appointment_type,
    "Outcome" AS outcome,
    "Year" AS year,
    "Notes" AS notes
FROM "statswales-99c2bf7c-1f09-4260-9e48-b096019a7beb"
