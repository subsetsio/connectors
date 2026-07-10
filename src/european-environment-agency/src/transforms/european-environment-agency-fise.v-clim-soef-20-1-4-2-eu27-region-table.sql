SELECT
    CAST("1990" AS VARCHAR) AS "1990",
    CAST("2000" AS VARCHAR) AS "2000",
    CAST("2005" AS VARCHAR) AS "2005",
    CAST("2010" AS VARCHAR) AS "2010",
    CAST("2015" AS VARCHAR) AS "2015",
    CAST("2020" AS VARCHAR) AS "2020",
    CAST("Annual_change_1990_2020" AS VARCHAR) AS "Annual_change_1990_2020",
    CAST("Annual_change_2010_2020" AS VARCHAR) AS "Annual_change_2010_2020",
    CAST("Annual_change_perc_1990_2020" AS VARCHAR) AS "Annual_change_perc_1990_2020",
    CAST("Annual_change_perc_2010_2020" AS VARCHAR) AS "Annual_change_perc_2010_2020",
    CAST("country" AS VARCHAR) AS "country",
    CAST("list" AS VARCHAR) AS "list",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("Region" AS VARCHAR) AS "Region",
    CAST("Units" AS VARCHAR) AS "Units"
FROM "european-environment-agency-fise.v-clim-soef-20-1-4-2-eu27-region-table"
