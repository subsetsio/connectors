-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Provision" AS provision,
    "Support" AS support,
    "Notes" AS notes
FROM "statswales-ed4c6994-e078-4a37-9709-5d7e90e24e7a"
