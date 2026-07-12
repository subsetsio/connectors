-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Treatment status" AS treatment_status,
    "Age" AS age,
    "Date" AS date,
    "Notes" AS notes
FROM "statswales-a4bbe4b4-f849-4cb4-9e09-f0273cf1ed7e"
