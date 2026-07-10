SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("lying" AS VARCHAR) AS "lying",
    CAST("standing" AS VARCHAR) AS "standing",
    CAST("total" AS VARCHAR) AS "total",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-countryfact-biodiv-soef20-deadwood"
