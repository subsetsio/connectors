SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("forest_above_ground" AS VARCHAR) AS "forest_above_ground",
    CAST("forest_below_ground" AS VARCHAR) AS "forest_below_ground",
    CAST("forest_deadwood" AS VARCHAR) AS "forest_deadwood",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("units" AS VARCHAR) AS "units",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-countryfact-soef20-biomass-stock"
