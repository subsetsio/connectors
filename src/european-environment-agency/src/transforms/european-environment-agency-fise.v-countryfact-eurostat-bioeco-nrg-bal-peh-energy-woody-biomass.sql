SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("share_of_primary_solid_fuels_in_total_electricity_production" AS VARCHAR) AS "share_of_primary_solid_fuels_in_total_electricity_production",
    CAST("share_of_primary_solid_fuels_in_total_renewable_production" AS VARCHAR) AS "share_of_primary_solid_fuels_in_total_renewable_production",
    CAST("Year" AS VARCHAR) AS "Year"
FROM "european-environment-agency-fise.v-countryfact-eurostat-bioeco-nrg-bal-peh-energy-woody-biomass"
