-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Reference-style source extract without a verified compact key; use the source columns as descriptive records rather than aggregating rows.
SELECT
    "resource_id",
    "resource_name",
    "DataZone2022" AS datazone2022,
    "DataZone2022_Name" AS datazone2022_name,
    CAST("UrbanRural2fold2022" AS BIGINT) AS urbanrural2fold2022,
    "UrbanRural2fold2022_Name" AS urbanrural2fold2022_name,
    CAST("UrbanRural3fold2022" AS BIGINT) AS urbanrural3fold2022,
    "UrbanRural3fold2022_Name" AS urbanrural3fold2022_name,
    CAST("UrbanRural6fold2022" AS BIGINT) AS urbanrural6fold2022,
    "UrbanRural6fold2022_Name" AS urbanrural6fold2022_name,
    CAST("UrbanRural8fold2022" AS BIGINT) AS urbanrural8fold2022,
    "UrbanRural8fold2022_Name" AS urbanrural8fold2022_name,
    "DataZone" AS datazone,
    CAST("UrbanRural2fold2020" AS BIGINT) AS urbanrural2fold2020,
    CAST("UrbanRural3fold2020" AS BIGINT) AS urbanrural3fold2020,
    CAST("UrbanRural6fold2020" AS BIGINT) AS urbanrural6fold2020,
    CAST("UrbanRural8fold2020" AS BIGINT) AS urbanrural8fold2020
FROM "public-health-scotland-urban-rural-classification"
