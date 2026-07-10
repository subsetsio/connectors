SELECT
    CAST("CountryCode" AS VARCHAR) AS "CountryCode",
    CAST("CountryName" AS VARCHAR) AS "CountryName",
    CAST("EnergyInput" AS VARCHAR) AS "EnergyInput",
    CAST("fuelInput" AS VARCHAR) AS "fuelInput",
    CAST("reportingYear" AS VARCHAR) AS "reportingYear"
FROM "european-environment-agency-ied.tableau-analysis-lcp-energyinput"
