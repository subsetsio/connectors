-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Academic year" AS academic_year,
    "Home region" AS home_region,
    "Gender" AS gender,
    "Ethnic background" AS ethnic_background,
    "Age group" AS age_group,
    "Notes" AS notes
FROM "statswales-31064862-72d5-42cf-a029-6ee93a9cb86c"
