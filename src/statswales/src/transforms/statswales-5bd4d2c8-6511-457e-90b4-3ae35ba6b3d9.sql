-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Geography" AS geography,
    "Sex" AS sex,
    "Duration of unemployment" AS duration_of_unemployment,
    "Notes" AS notes
FROM "statswales-5bd4d2c8-6511-457e-90b4-3ae35ba6b3d9"
