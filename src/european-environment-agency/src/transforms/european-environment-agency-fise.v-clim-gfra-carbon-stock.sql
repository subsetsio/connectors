SELECT
    CAST("eu27" AS VARCHAR) AS "eu27",
    CAST("eu27_carbon_stock_biomass" AS VARCHAR) AS "eu27_carbon_stock_biomass",
    CAST("eu27_total_carbon_stock" AS VARCHAR) AS "eu27_total_carbon_stock",
    CAST("units" AS VARCHAR) AS "units",
    CAST("world" AS VARCHAR) AS "world",
    CAST("world_carbon_stock_biomass" AS VARCHAR) AS "world_carbon_stock_biomass",
    CAST("world_total_carbon_stock" AS VARCHAR) AS "world_total_carbon_stock",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-clim-gfra-carbon-stock"
