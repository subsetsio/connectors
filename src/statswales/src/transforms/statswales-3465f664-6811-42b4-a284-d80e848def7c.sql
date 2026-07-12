-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Resident Health Board" AS resident_health_board,
    "Date" AS date,
    "Age and Service" AS age_and_service,
    "Notes" AS notes
FROM "statswales-3465f664-6811-42b4-a284-d80e848def7c"
