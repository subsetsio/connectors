SELECT
    CAST("age" AS VARCHAR) AS "age",
    CAST("nace_r2" AS VARCHAR) AS "nace_r2",
    CAST("nace_r2_description" AS VARCHAR) AS "nace_r2_description",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("sex" AS VARCHAR) AS "sex",
    CAST("unit" AS VARCHAR) AS "unit",
    CAST("value" AS VARCHAR) AS "value",
    CAST("Year" AS VARCHAR) AS "Year"
FROM "european-environment-agency-fise.eurostat-employment-lsfa-egan22d"
