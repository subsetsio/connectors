SELECT
    CAST("Biomass" AS VARCHAR) AS "Biomass",
    CAST("carbon_forest_above_ground" AS VARCHAR) AS "carbon_forest_above_ground",
    CAST("carbon_forest_below_ground" AS VARCHAR) AS "carbon_forest_below_ground",
    CAST("carbon_forest_deadwood" AS VARCHAR) AS "carbon_forest_deadwood",
    CAST("carbon_forest_litter" AS VARCHAR) AS "carbon_forest_litter",
    CAST("carbon_forest_soil" AS VARCHAR) AS "carbon_forest_soil",
    CAST("country" AS VARCHAR) AS "country",
    CAST("Deadwood" AS VARCHAR) AS "Deadwood",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("Soil and litter" AS VARCHAR) AS "Soil and litter",
    CAST("Stored forest" AS VARCHAR) AS "Stored forest",
    CAST("Units" AS VARCHAR) AS "Units",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-countryfact-gfra-clim-carbon-stock"
