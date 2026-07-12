-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Area code" AS area_code,
    "Area name" AS area_name,
    "Domain" AS domain,
    "Deprivation group" AS deprivation_group,
    "Notes" AS notes
FROM "statswales-2ba2a217-50d3-4fdd-9bbf-dc4c08eadfbc"
