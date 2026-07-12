-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Date" AS date,
    "Local health board" AS local_health_board,
    "Notes" AS notes
FROM "statswales-3fd5b415-0633-47c7-9861-5ffaa3ebe6f4"
