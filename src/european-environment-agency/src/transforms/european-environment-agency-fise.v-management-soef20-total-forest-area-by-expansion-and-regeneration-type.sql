SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("forest" AS VARCHAR) AS "forest",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("units" AS VARCHAR) AS "units",
    CAST("variable" AS VARCHAR) AS "variable",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-management-soef20-total-forest-area-by-expansion-and-regeneration-type"
