SELECT
    CAST("Country_name" AS VARCHAR) AS "Country_name",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("Share_of_woody_biomass_in_RES" AS VARCHAR) AS "Share_of_woody_biomass_in_RES",
    CAST("Share_of_woody_biomass_in_TPES" AS VARCHAR) AS "Share_of_woody_biomass_in_TPES",
    CAST("Year" AS VARCHAR) AS "Year"
FROM "european-environment-agency-fise.unece-jwee-woodenergy"
