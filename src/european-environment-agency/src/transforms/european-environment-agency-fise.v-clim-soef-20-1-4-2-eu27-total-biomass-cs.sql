SELECT
    CAST("biomass" AS VARCHAR) AS "biomass",
    CAST("country" AS VARCHAR) AS "country",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("Region" AS VARCHAR) AS "Region",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-clim-soef-20-1-4-2-eu27-total-biomass-cs"
