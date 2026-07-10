SELECT
    CAST("CountryCode" AS VARCHAR) AS "CountryCode",
    CAST("CountryName" AS VARCHAR) AS "CountryName",
    CAST("EnergyInput" AS VARCHAR) AS "EnergyInput",
    CAST("FuelInput" AS VARCHAR) AS "FuelInput",
    CAST("reportingYear" AS VARCHAR) AS "reportingYear"
FROM "european-environment-agency-ied.lcp-energyinput-2004-2015"
