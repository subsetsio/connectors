SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("lying" AS VARCHAR) AS "lying",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("standing" AS VARCHAR) AS "standing",
    CAST("total" AS VARCHAR) AS "total",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-biodiv-soef20-deadwood-pivot"
