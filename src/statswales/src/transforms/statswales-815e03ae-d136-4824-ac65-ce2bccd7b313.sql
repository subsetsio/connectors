-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Month" AS month,
    "Local authority" AS local_authority,
    "Notes" AS notes
FROM "statswales-815e03ae-d136-4824-ac65-ce2bccd7b313"
