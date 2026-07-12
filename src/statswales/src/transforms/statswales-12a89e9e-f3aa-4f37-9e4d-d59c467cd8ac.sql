-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Data values" AS data_values,
    "Data description" AS data_description,
    "Date" AS date,
    "Notes" AS notes
FROM "statswales-12a89e9e-f3aa-4f37-9e4d-d59c467cd8ac"
