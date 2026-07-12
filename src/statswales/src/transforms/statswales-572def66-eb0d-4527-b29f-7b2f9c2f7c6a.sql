-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Academic year" AS academic_year,
    "Home region" AS home_region,
    "Programme type" AS programme_type,
    "Sector" AS sector,
    "Age group" AS age_group,
    "Gender" AS gender,
    "Notes" AS notes
FROM "statswales-572def66-eb0d-4527-b29f-7b2f9c2f7c6a"
