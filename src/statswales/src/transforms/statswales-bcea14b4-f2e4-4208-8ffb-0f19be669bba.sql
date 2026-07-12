-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Appointment Status" AS appointment_status,
    "Area" AS area,
    "Date" AS date,
    "Notes" AS notes
FROM "statswales-bcea14b4-f2e4-4208-8ffb-0f19be669bba"
