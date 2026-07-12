-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Data values" AS data_values,
    "Data description" AS data_description,
    "Date" AS date,
    "Area" AS area,
    "Notes" AS notes
FROM "statswales-d5b6fe7e-6914-4261-b71b-5df3302ae6e3"
