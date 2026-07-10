SELECT
    CAST("Country_name" AS VARCHAR) AS "Country_name",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("Share_of_woody_biomass_in_RES_percentage" AS VARCHAR) AS "Share_of_woody_biomass_in_RES_percentage",
    CAST("Share_of_woody_biomass_in_TPES_percentage" AS VARCHAR) AS "Share_of_woody_biomass_in_TPES_percentage",
    CAST("Year" AS VARCHAR) AS "Year"
FROM "european-environment-agency-fise.v-bioeco-unece-jwee-woodenergy"
