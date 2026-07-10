SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("emissions" AS VARCHAR) AS "emissions",
    CAST("emissions_gdp" AS VARCHAR) AS "emissions_gdp",
    CAST("emissions_per_capita" AS VARCHAR) AS "emissions_per_capita",
    CAST("gas" AS VARCHAR) AS "gas",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("sector_name" AS VARCHAR) AS "sector_name",
    CAST("unit" AS VARCHAR) AS "unit",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-countryfact-ghg-clim-lulucf-emissions"
