-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Commodities" AS commodities,
    CAST("Year" AS BIGINT) AS year,
    "Notes" AS notes
FROM "statswales-3cab1202-8f85-4a0e-b36d-b77d16051146"
