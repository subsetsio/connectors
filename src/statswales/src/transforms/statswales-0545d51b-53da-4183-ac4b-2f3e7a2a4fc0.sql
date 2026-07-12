-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Date" AS date,
    "Local health board" AS local_health_board,
    "Service" AS service,
    "Notes" AS notes
FROM "statswales-0545d51b-53da-4183-ac4b-2f3e7a2a4fc0"
