-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Farm Type" AS farm_type,
    "NPK Type" AS npk_type,
    "Year" AS year,
    "Notes" AS notes
FROM "statswales-6133565c-36d2-4392-b8ca-d947d680fedd"
