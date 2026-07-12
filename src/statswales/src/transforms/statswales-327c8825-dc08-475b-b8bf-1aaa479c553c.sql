-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "School" AS school,
    "Category" AS category,
    "Notes" AS notes
FROM "statswales-327c8825-dc08-475b-b8bf-1aaa479c553c"
