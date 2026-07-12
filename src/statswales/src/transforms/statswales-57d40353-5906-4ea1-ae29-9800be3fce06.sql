-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Measure" AS measure,
    strptime("Date", '%d/%m/%Y')::DATE AS date,
    "Local health board" AS local_health_board,
    "Notes" AS notes
FROM "statswales-57d40353-5906-4ea1-ae29-9800be3fce06"
