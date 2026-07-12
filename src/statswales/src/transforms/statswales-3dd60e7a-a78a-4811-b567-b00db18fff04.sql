-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Deprivation group" AS deprivation_group,
    "Area name" AS area_name,
    "Area code" AS area_code,
    "Domain" AS domain,
    "Notes" AS notes
FROM "statswales-3dd60e7a-a78a-4811-b567-b00db18fff04"
