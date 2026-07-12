-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Area" AS area,
    "Age" AS age,
    "Notes" AS notes
FROM "statswales-2a926db9-c61d-4a1c-93f7-95d2bb9c6d0e"
