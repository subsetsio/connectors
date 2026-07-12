-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    strptime("Date", '%d/%m/%Y')::DATE AS date,
    "Staff type" AS staff_type,
    "Area" AS area,
    "Notes" AS notes
FROM "statswales-3525ae7c-3d10-4fde-b558-56cab4b77847"
