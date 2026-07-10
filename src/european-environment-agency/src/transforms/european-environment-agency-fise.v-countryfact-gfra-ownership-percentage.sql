SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("group_type" AS VARCHAR) AS "group_type",
    CAST("group_value" AS VARCHAR) AS "group_value",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("units" AS VARCHAR) AS "units",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-countryfact-gfra-ownership-percentage"
