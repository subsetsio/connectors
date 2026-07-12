-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Area" AS area,
    "Appointment Category" AS appointment_category,
    "Date" AS date,
    "Notes" AS notes
FROM "statswales-1bf4056a-e599-4051-aafd-8fe303d4c563"
