SELECT
    CAST("DATASET" AS VARCHAR) AS "DATASET",
    CAST("FORES_AREA" AS VARCHAR) AS "FORES_AREA",
    CAST("geometry" AS VARCHAR) AS "geometry",
    CAST("LargePatch_ha" AS VARCHAR) AS "LargePatch_ha",
    CAST("LargePatch_pct" AS VARCHAR) AS "LargePatch_pct",
    CAST("LEVL_CODE" AS VARCHAR) AS "LEVL_CODE",
    CAST("MediumPatch_ha" AS VARCHAR) AS "MediumPatch_ha",
    CAST("MediumPatch_pct" AS VARCHAR) AS "MediumPatch_pct",
    CAST("NUTS_AREA" AS VARCHAR) AS "NUTS_AREA",
    CAST("NUTS_ID" AS VARCHAR) AS "NUTS_ID",
    CAST("NUTS_NAME" AS VARCHAR) AS "NUTS_NAME",
    CAST("NUTS0" AS VARCHAR) AS "NUTS0",
    CAST("NUTS0_NAME" AS VARCHAR) AS "NUTS0_NAME",
    CAST("PERCT_FOR" AS VARCHAR) AS "PERCT_FOR",
    CAST("SmallPatch_ha" AS VARCHAR) AS "SmallPatch_ha",
    CAST("SmallPatch_pct" AS VARCHAR) AS "SmallPatch_pct",
    CAST("YEAR" AS VARCHAR) AS "YEAR"
FROM "european-environment-agency-fise.ms-forestarea"
