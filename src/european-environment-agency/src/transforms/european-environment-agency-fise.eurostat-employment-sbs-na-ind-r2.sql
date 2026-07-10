SELECT
    CAST("indic_sb" AS VARCHAR) AS "indic_sb",
    CAST("nace_r2" AS VARCHAR) AS "nace_r2",
    CAST("nace_r2_description" AS VARCHAR) AS "nace_r2_description",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("value" AS VARCHAR) AS "value",
    CAST("Year" AS VARCHAR) AS "Year"
FROM "european-environment-agency-fise.eurostat-employment-sbs-na-ind-r2"
