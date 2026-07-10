SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("growing_stock" AS VARCHAR) AS "growing_stock",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("units" AS VARCHAR) AS "units",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-countryfact-inforest-growing-stock"
