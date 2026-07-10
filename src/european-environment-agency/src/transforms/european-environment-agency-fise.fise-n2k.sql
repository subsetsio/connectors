SELECT
    CAST("forestN2K" AS VARCHAR) AS "forestN2K",
    CAST("ForestN2kPerc" AS VARCHAR) AS "ForestN2kPerc",
    CAST("ForestN2KTotal" AS VARCHAR) AS "ForestN2KTotal",
    CAST("forestNo_N2K" AS VARCHAR) AS "forestNo_N2K",
    CAST("ForestTotal" AS VARCHAR) AS "ForestTotal",
    CAST("No_forestN2K" AS VARCHAR) AS "No_forestN2K",
    CAST("No_forestNo_N2K" AS VARCHAR) AS "No_forestNo_N2K",
    CAST("NUT_ID" AS VARCHAR) AS "NUT_ID",
    CAST("NUT_LEVL" AS VARCHAR) AS "NUT_LEVL",
    CAST("transitional_forestN2k" AS VARCHAR) AS "transitional_forestN2k",
    CAST("transitional_forestNo_N2k" AS VARCHAR) AS "transitional_forestNo_N2k",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.fise-n2k"
