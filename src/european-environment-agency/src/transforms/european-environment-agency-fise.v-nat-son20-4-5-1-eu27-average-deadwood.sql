SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("regimes" AS VARCHAR) AS "regimes",
    CAST("units" AS VARCHAR) AS "units",
    CAST("value" AS VARCHAR) AS "value",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-nat-son20-4-5-1-eu27-average-deadwood"
