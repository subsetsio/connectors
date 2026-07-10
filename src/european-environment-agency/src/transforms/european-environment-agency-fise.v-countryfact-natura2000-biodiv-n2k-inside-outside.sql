SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("forest_percentage" AS VARCHAR) AS "forest_percentage",
    CAST("forestN2K_percentage" AS VARCHAR) AS "forestN2K_percentage",
    CAST("group_type" AS VARCHAR) AS "group_type",
    CAST("group_value" AS VARCHAR) AS "group_value",
    CAST("LEVL_CODE" AS VARCHAR) AS "LEVL_CODE",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("total" AS VARCHAR) AS "total",
    CAST("units" AS VARCHAR) AS "units",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-countryfact-natura2000-biodiv-n2k-inside-outside"
