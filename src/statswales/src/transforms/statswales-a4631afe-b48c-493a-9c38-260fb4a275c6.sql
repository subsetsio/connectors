-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Area of learning" AS area_of_learning,
    "Sex" AS sex,
    "Notes" AS notes
FROM "statswales-a4631afe-b48c-493a-9c38-260fb4a275c6"
