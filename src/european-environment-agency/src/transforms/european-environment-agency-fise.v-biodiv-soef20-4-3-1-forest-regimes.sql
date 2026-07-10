SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("regime_value" AS VARCHAR) AS "regime_value",
    CAST("regimes" AS VARCHAR) AS "regimes",
    CAST("units" AS VARCHAR) AS "units",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-biodiv-soef20-4-3-1-forest-regimes"
