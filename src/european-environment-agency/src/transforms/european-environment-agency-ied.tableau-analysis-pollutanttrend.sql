SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("CountryName" AS VARCHAR) AS "CountryName",
    CAST("Emissions" AS VARCHAR) AS "Emissions",
    CAST("Pollutant" AS VARCHAR) AS "Pollutant",
    CAST("reportingYear" AS VARCHAR) AS "reportingYear",
    CAST("TargetRelease" AS VARCHAR) AS "TargetRelease"
FROM "european-environment-agency-ied.tableau-analysis-pollutanttrend"
