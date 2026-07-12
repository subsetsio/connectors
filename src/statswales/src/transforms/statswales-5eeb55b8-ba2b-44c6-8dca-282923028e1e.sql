-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Authority" AS authority,
    "Row" AS row,
    "Notes" AS notes
FROM "statswales-5eeb55b8-ba2b-44c6-8dca-282923028e1e"
