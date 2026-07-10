SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("type" AS VARCHAR) AS "type",
    CAST("value" AS VARCHAR) AS "value",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-countryfact-gfra-forest-area-within-protected-areas"
