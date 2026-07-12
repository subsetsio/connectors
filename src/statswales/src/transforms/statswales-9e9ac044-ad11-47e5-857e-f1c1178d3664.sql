-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Free School Meals" AS free_school_meals,
    "Subject" AS subject,
    "Notes" AS notes
FROM "statswales-9e9ac044-ad11-47e5-857e-f1c1178d3664"
