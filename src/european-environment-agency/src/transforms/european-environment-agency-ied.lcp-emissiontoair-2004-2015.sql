SELECT
    CAST("CountryCode" AS VARCHAR) AS "CountryCode",
    CAST("CountryName" AS VARCHAR) AS "CountryName",
    CAST("Emissions" AS VARCHAR) AS "Emissions",
    CAST("Pollutant" AS VARCHAR) AS "Pollutant",
    CAST("reportingYear" AS VARCHAR) AS "reportingYear"
FROM "european-environment-agency-ied.lcp-emissiontoair-2004-2015"
