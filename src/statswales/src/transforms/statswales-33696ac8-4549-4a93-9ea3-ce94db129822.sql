-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Area name" AS area_name,
    "Area code" AS area_code,
    "Deep-rooted deprivation category" AS deep_rooted_deprivation_category,
    "Domain" AS domain,
    CAST("Year" AS BIGINT) AS year,
    "Notes" AS notes
FROM "statswales-33696ac8-4549-4a93-9ea3-ce94db129822"
