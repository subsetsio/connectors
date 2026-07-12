-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Local authority" AS local_authority,
    "Sex" AS sex,
    "Free School Meals" AS free_school_meals,
    "Notes" AS notes
FROM "statswales-38e7000c-e2d0-4935-89e0-b705093a4683"
