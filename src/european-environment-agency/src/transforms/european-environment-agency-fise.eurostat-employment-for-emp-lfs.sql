SELECT
    CAST("isced11" AS VARCHAR) AS "isced11",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("Sector" AS VARCHAR) AS "Sector",
    CAST("sex" AS VARCHAR) AS "sex",
    CAST("units" AS VARCHAR) AS "units",
    CAST("value" AS VARCHAR) AS "value",
    CAST("wstatus" AS VARCHAR) AS "wstatus",
    CAST("Year" AS VARCHAR) AS "Year"
FROM "european-environment-agency-fise.eurostat-employment-for-emp-lfs"
