-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Area" AS area,
    "Characteristic" AS characteristic,
    "Year" AS year,
    "Notes" AS notes
FROM "statswales-20171885-5e00-465b-a5a9-36572753e477"
