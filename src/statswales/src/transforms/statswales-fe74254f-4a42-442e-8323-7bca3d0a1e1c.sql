-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Subject" AS subject,
    "Sex" AS sex,
    "Assessment type" AS assessment_type,
    "Notes" AS notes
FROM "statswales-fe74254f-4a42-442e-8323-7bca3d0a1e1c"
