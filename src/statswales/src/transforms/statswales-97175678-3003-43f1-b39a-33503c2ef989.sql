-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    strptime("Date", '%d/%m/%Y')::DATE AS date,
    "Practice" AS practice,
    "Method" AS method,
    "Notes" AS notes
FROM "statswales-97175678-3003-43f1-b39a-33503c2ef989"
