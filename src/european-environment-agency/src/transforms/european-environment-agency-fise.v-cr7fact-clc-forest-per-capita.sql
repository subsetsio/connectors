SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("forest_per_capita" AS VARCHAR) AS "forest_per_capita",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("population" AS VARCHAR) AS "population",
    CAST("total_area" AS VARCHAR) AS "total_area",
    CAST("units" AS VARCHAR) AS "units",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-cr7fact-clc-forest-per-capita"
