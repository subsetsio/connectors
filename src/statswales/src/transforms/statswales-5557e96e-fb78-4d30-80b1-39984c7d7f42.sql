-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Staff Measure" AS staff_measure,
    "Number of staff" AS number_of_staff,
    strptime("Date", '%d/%m/%Y')::DATE AS date,
    "Local health board" AS local_health_board,
    "Notes" AS notes
FROM "statswales-5557e96e-fb78-4d30-80b1-39984c7d7f42"
