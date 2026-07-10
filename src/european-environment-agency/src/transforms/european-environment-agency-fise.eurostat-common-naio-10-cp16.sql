SELECT
    CAST("induse" AS VARCHAR) AS "induse",
    CAST("induse_description" AS VARCHAR) AS "induse_description",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("prod_na" AS VARCHAR) AS "prod_na",
    CAST("prod_na_description" AS VARCHAR) AS "prod_na_description",
    CAST("stk_flow" AS VARCHAR) AS "stk_flow",
    CAST("unit" AS VARCHAR) AS "unit",
    CAST("value" AS VARCHAR) AS "value",
    CAST("Year" AS VARCHAR) AS "Year"
FROM "european-environment-agency-fise.eurostat-common-naio-10-cp16"
