SELECT
    CAST("employment" AS VARCHAR) AS "employment",
    CAST("nace_r2" AS VARCHAR) AS "nace_r2",
    CAST("nace_r2_description" AS VARCHAR) AS "nace_r2_description",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("sex" AS VARCHAR) AS "sex",
    CAST("unit" AS VARCHAR) AS "unit",
    CAST("woodShare" AS VARCHAR) AS "woodShare",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.eurostat-employment-for-emp-lfsa-cwood"
