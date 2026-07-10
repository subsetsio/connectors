SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("key_fact" AS VARCHAR) AS "key_fact",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("units" AS VARCHAR) AS "units",
    CAST("value" AS VARCHAR) AS "value",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-fe2020-keyfacts"
