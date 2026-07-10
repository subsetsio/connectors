SELECT
    CAST("Country" AS VARCHAR) AS "Country",
    CAST("fores_area" AS VARCHAR) AS "fores_area",
    CAST("nuts_area" AS VARCHAR) AS "nuts_area",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("perct_for" AS VARCHAR) AS "perct_for"
FROM "european-environment-agency-fise.v-home-clc-top-6-countries-forest-tree-cover"
