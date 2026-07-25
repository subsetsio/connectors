-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "MEASURES_" AS measures,
    CAST("Category_Parent" AS BIGINT) AS category_parent,
    "Oktmo_Parent" AS oktmo_parent,
    CAST("Dim_Service_Provider_Code" AS BIGINT) AS dim_service_provider_code,
    CAST("time" AS BIGINT) AS time,
    "value"
FROM "rosstat-7708234640-vshp2016435"
