SELECT
    CAST("AccidentalEmissions" AS VARCHAR) AS "AccidentalEmissions",
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("CountryName" AS VARCHAR) AS "CountryName",
    CAST("Emissions" AS VARCHAR) AS "Emissions",
    CAST("eprtrActivityCode" AS VARCHAR) AS "eprtrActivityCode",
    CAST("eprtrActivityName" AS VARCHAR) AS "eprtrActivityName",
    CAST("eprtrSectorName" AS VARCHAR) AS "eprtrSectorName",
    CAST("Pollutant" AS VARCHAR) AS "Pollutant",
    CAST("PollutantGroup" AS VARCHAR) AS "PollutantGroup",
    CAST("reportingYear" AS VARCHAR) AS "reportingYear",
    CAST("TargetRelease" AS VARCHAR) AS "TargetRelease"
FROM "european-environment-agency-ied.tableau-analysis-pollutantsector-trend"
