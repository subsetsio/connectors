SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("NSME" AS VARCHAR) AS "NSME",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("SME" AS VARCHAR) AS "SME",
    CAST("SME_LW95" AS VARCHAR) AS "SME_LW95",
    CAST("SME_UP95" AS VARCHAR) AS "SME_UP95",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-nat-son20-6-11-trend-status-common-forest-birds-europe"
