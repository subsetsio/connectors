-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    strptime("Date", '%d/%m/%Y')::DATE AS date,
    "Staff" AS staff,
    "Sex" AS sex,
    "Local health board" AS local_health_board,
    "Notes" AS notes
FROM "statswales-ec92c8ef-4e4e-453e-9ff6-2c8dd901a946"
