-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Age" AS age,
    "Employment" AS employment,
    "Gender" AS gender,
    "Notes" AS notes
FROM "statswales-9745d051-b579-48fe-ae8c-a60b2962afee"
