SELECT
    CAST("carbon_forest_above_ground" AS VARCHAR) AS "carbon_forest_above_ground",
    CAST("carbon_forest_below_ground" AS VARCHAR) AS "carbon_forest_below_ground",
    CAST("carbon_forest_deadwood" AS VARCHAR) AS "carbon_forest_deadwood",
    CAST("carbon_forest_litter" AS VARCHAR) AS "carbon_forest_litter",
    CAST("carbon_forest_soil" AS VARCHAR) AS "carbon_forest_soil",
    CAST("country" AS VARCHAR) AS "country",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("units" AS VARCHAR) AS "units",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-clim-gfra-carbon-stock-country"
