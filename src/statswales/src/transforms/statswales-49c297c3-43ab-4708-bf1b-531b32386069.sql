-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "BNF" AS bnf,
    "Year" AS year,
    "Area" AS area,
    "Notes" AS notes
FROM "statswales-49c297c3-43ab-4708-bf1b-531b32386069"
