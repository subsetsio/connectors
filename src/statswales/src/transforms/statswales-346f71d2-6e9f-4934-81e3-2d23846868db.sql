-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Academic year" AS academic_year,
    "Provision type" AS provision_type,
    "Provider type" AS provider_type,
    "Home region" AS home_region,
    "Age group" AS age_group,
    "Gender" AS gender,
    "Demographic measure" AS demographic_measure,
    "Demographic value" AS demographic_value,
    "Notes" AS notes
FROM "statswales-346f71d2-6e9f-4934-81e3-2d23846868db"
