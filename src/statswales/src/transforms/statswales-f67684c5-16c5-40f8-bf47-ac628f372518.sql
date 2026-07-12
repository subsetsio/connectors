-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Geography" AS geography,
    "Sex" AS sex,
    "Notes" AS notes
FROM "statswales-f67684c5-16c5-40f8-bf47-ac628f372518"
