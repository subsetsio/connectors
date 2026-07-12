-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Area code" AS area_code,
    "Area name" AS area_name,
    CAST("Year" AS BIGINT) AS year,
    "Deep-rooted deprivation category" AS deep_rooted_deprivation_category,
    "Notes" AS notes
FROM "statswales-cbecfd4a-2984-4c2e-b9e2-4010fd2348ef"
