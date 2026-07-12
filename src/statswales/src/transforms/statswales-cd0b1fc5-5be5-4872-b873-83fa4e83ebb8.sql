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
FROM "statswales-cd0b1fc5-5be5-4872-b873-83fa4e83ebb8"
