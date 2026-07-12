-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Farm Type" AS farm_type,
    "Asset Type" AS asset_type,
    "Year" AS year,
    "Notes" AS notes
FROM "statswales-91ac7384-8bf2-41f7-8dcd-aca0f036884d"
