SELECT
    CAST("CNTR_CODE" AS VARCHAR) AS "CNTR_CODE",
    CAST("ctry_Name" AS VARCHAR) AS "ctry_Name",
    CAST("forestN2K" AS VARCHAR) AS "forestN2K",
    CAST("ForestN2kPerc" AS VARCHAR) AS "ForestN2kPerc",
    CAST("ForestN2KTotal" AS VARCHAR) AS "ForestN2KTotal",
    CAST("forestNo_N2K" AS VARCHAR) AS "forestNo_N2K",
    CAST("ForestTotal" AS VARCHAR) AS "ForestTotal",
    CAST("LEVL_CODE" AS VARCHAR) AS "LEVL_CODE",
    CAST("No_forestN2K" AS VARCHAR) AS "No_forestN2K",
    CAST("No_forestNo_N2K" AS VARCHAR) AS "No_forestNo_N2K",
    CAST("NUTS_ID" AS VARCHAR) AS "NUTS_ID",
    CAST("NUTS_NAME" AS VARCHAR) AS "NUTS_NAME",
    CAST("transitional_forestN2k" AS VARCHAR) AS "transitional_forestN2k",
    CAST("transitional_forestNo_N2k" AS VARCHAR) AS "transitional_forestNo_N2k",
    CAST("YEAR" AS VARCHAR) AS "YEAR"
FROM "european-environment-agency-fise.jedi-n2k"
