SELECT
    CAST("area" AS VARCHAR) AS "area",
    CAST("country" AS VARCHAR) AS "country",
    CAST("land_use_class" AS VARCHAR) AS "land_use_class",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("percentage" AS VARCHAR) AS "percentage",
    CAST("units" AS VARCHAR) AS "units",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-countryfact-clc-landcover-use"
