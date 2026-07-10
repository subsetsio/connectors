SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("EU27" AS VARCHAR) AS "EU27",
    CAST("forest_area" AS VARCHAR) AS "forest_area",
    CAST("forest_percentage" AS VARCHAR) AS "forest_percentage",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("units" AS VARCHAR) AS "units",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-basicforest-clc-area-and-perct-of-forest-cover-in-europe"
