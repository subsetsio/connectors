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
    "Gender" AS gender,
    "Age group" AS age_group,
    "Demographic measure" AS demographic_measure,
    "Demographic value" AS demographic_value,
    "Notes" AS notes
FROM "statswales-19b54b94-78c1-4b74-86d0-57ad74f1d994"
