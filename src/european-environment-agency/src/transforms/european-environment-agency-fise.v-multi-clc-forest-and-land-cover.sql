SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("fores_area_311_312_313" AS VARCHAR) AS "fores_area_311_312_313",
    CAST("fores_area_311_312_313_324" AS VARCHAR) AS "fores_area_311_312_313_324",
    CAST("nuts_area" AS VARCHAR) AS "nuts_area",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("perct_for_311_312_313_324" AS VARCHAR) AS "perct_for_311_312_313_324",
    CAST("perct_woodland" AS VARCHAR) AS "perct_woodland",
    CAST("units" AS VARCHAR) AS "units",
    CAST("woodland_area" AS VARCHAR) AS "woodland_area",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-multi-clc-forest-and-land-cover"
