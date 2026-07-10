SELECT
    CAST("airPollutionPerCapita" AS VARCHAR) AS "airPollutionPerCapita",
    CAST("CountryCode" AS VARCHAR) AS "CountryCode",
    CAST("countryGroupId" AS VARCHAR) AS "countryGroupId",
    CAST("population" AS VARCHAR) AS "population",
    CAST("reportingYear" AS VARCHAR) AS "reportingYear",
    CAST("waterPollutionPerCapita" AS VARCHAR) AS "waterPollutionPerCapita"
FROM "european-environment-agency-ied.pollutantquantitypercapita"
