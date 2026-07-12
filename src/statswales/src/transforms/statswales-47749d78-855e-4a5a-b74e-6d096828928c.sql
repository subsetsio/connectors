-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Claim type" AS claim_type,
    "Year" AS year,
    "Area" AS area,
    "Notes" AS notes
FROM "statswales-47749d78-855e-4a5a-b74e-6d096828928c"
