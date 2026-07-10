SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("regime" AS VARCHAR) AS "regime",
    CAST("volume" AS VARCHAR) AS "volume",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-biodiv-son20-4-5-1-average-deadwood"
