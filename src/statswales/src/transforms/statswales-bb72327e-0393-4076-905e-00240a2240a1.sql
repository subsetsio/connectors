-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Medium" AS medium,
    "Provision" AS provision,
    "Notes" AS notes
FROM "statswales-bb72327e-0393-4076-905e-00240a2240a1"
