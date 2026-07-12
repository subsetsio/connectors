-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Row" AS row,
    "Column" AS column,
    "Authority" AS authority,
    "Notes" AS notes
FROM "statswales-04eb4d05-55ab-4c1c-80fa-627fa809fc14"
