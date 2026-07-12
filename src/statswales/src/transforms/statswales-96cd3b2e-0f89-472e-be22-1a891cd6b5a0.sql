-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    strptime("Date", '%d/%m/%Y')::DATE AS date,
    "Characteristics" AS characteristics,
    "Outcome" AS outcome,
    "Notes" AS notes
FROM "statswales-96cd3b2e-0f89-472e-be22-1a891cd6b5a0"
