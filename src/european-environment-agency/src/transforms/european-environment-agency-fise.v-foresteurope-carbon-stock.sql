SELECT
    CAST("carbon_forest_above_ground" AS VARCHAR) AS "carbon_forest_above_ground",
    CAST("carbon_forest_below_ground" AS VARCHAR) AS "carbon_forest_below_ground",
    CAST("carbon_forest_deadwood" AS VARCHAR) AS "carbon_forest_deadwood",
    CAST("carbon_forest_litter" AS VARCHAR) AS "carbon_forest_litter",
    CAST("carbon_forest_soil" AS VARCHAR) AS "carbon_forest_soil",
    CAST("country" AS VARCHAR) AS "country",
    CAST("Country_name" AS VARCHAR) AS "Country_name",
    CAST("perc_above_ground" AS VARCHAR) AS "perc_above_ground",
    CAST("perc_below_ground" AS VARCHAR) AS "perc_below_ground",
    CAST("perc_deadwood" AS VARCHAR) AS "perc_deadwood",
    CAST("perc_litter" AS VARCHAR) AS "perc_litter",
    CAST("perc_soil" AS VARCHAR) AS "perc_soil",
    CAST("total" AS VARCHAR) AS "total",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-foresteurope-carbon-stock"
