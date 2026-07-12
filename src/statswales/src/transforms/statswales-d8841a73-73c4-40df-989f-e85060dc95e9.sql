-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Service Health Board" AS service_health_board,
    "Patient Health Board" AS patient_health_board,
    "Notes" AS notes
FROM "statswales-d8841a73-73c4-40df-989f-e85060dc95e9"
