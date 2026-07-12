-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "GPType" AS gptype,
    strptime("Date", '%d/%m/%Y')::DATE AS date,
    "Area" AS area,
    "Notes" AS notes
FROM "statswales-733ab30a-2d98-4186-b0de-1b93fe5dd48a"
