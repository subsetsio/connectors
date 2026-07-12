-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Age" AS age,
    "Sex" AS sex,
    "Area" AS area,
    "Notes" AS notes
FROM "statswales-f7c81eb8-cf29-4d14-b964-04c155527e4d"
