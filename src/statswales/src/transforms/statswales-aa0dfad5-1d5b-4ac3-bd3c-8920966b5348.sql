-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    strptime("Date", '%d/%m/%Y')::DATE AS date,
    "Staff" AS staff,
    "Age" AS age,
    "Local health board" AS local_health_board,
    "Notes" AS notes
FROM "statswales-aa0dfad5-1d5b-4ac3-bd3c-8920966b5348"
