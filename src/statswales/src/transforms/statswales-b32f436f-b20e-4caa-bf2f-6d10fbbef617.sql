-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Academic year" AS academic_year,
    "Provision type" AS provision_type,
    "Provider" AS provider,
    "Age group" AS age_group,
    "Gender" AS gender,
    "Demographic measure" AS demographic_measure,
    "Demographic value" AS demographic_value,
    "Notes" AS notes
FROM "statswales-b32f436f-b20e-4caa-bf2f-6d10fbbef617"
