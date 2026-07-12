-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Area" AS area,
    "Specialty" AS specialty,
    "Appointment Purpose" AS appointment_purpose,
    "Outcome" AS outcome,
    "Year" AS year,
    "Notes" AS notes
FROM "statswales-08fe70d2-036c-4f99-881b-6e3cbbccb6be"
