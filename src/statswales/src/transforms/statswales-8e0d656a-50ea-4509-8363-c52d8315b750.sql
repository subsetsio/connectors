-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Row description" AS row_description,
    "Authority" AS authority,
    "Notes" AS notes
FROM "statswales-8e0d656a-50ea-4509-8363-c52d8315b750"
