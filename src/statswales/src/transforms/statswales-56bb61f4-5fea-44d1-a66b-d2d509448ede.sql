-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Tenure" AS tenure,
    "Region" AS region,
    "Notes" AS notes
FROM "statswales-56bb61f4-5fea-44d1-a66b-d2d509448ede"
