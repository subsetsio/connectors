-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    strptime("Date", '%d/%m/%Y')::DATE AS date,
    "Patient Residence" AS patient_residence,
    "Country of general practice" AS country_of_general_practice,
    "Notes" AS notes
FROM "statswales-3ba96615-4707-49ea-a519-cfde41b0a4d1"
