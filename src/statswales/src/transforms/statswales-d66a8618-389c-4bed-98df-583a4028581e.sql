-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Type of staff" AS type_of_staff,
    "Year" AS year,
    "Notes" AS notes
FROM "statswales-d66a8618-389c-4bed-98df-583a4028581e"
