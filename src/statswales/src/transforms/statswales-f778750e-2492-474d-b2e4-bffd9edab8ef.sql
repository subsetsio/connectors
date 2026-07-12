-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Geography" AS geography,
    "Sex" AS sex,
    CAST("Year" AS BIGINT) AS year,
    "Notes" AS notes
FROM "statswales-f778750e-2492-474d-b2e4-bffd9edab8ef"
