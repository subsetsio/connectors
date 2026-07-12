-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Area" AS area,
    "BNF" AS bnf,
    "Year" AS year,
    "Notes" AS notes
FROM "statswales-5dc38a04-cc59-42a9-bce7-31ae8c5b15db"
