SELECT
    CAST("CDDACovLandArea" AS VARCHAR) AS "CDDACovLandArea",
    CAST("CDDAcovLandPercentage" AS VARCHAR) AS "CDDAcovLandPercentage",
    CAST("CDDACovMarineArea" AS VARCHAR) AS "CDDACovMarineArea",
    CAST("CDDACovMarinePercentage" AS VARCHAR) AS "CDDACovMarinePercentage",
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("CountryName" AS VARCHAR) AS "CountryName",
    CAST("Discodata_update_marine" AS VARCHAR) AS "Discodata_update_marine",
    CAST("Discodata_update_terrestrial" AS VARCHAR) AS "Discodata_update_terrestrial",
    CAST("N2KCovLandArea" AS VARCHAR) AS "N2KCovLandArea",
    CAST("N2KcovLandPercentage" AS VARCHAR) AS "N2KcovLandPercentage",
    CAST("N2KCovMarineArea" AS VARCHAR) AS "N2KCovMarineArea",
    CAST("N2KCovMarinePercentage" AS VARCHAR) AS "N2KCovMarinePercentage",
    CAST("Temporal_coverage" AS VARCHAR) AS "Temporal_coverage",
    CAST("totalCovLandArea" AS VARCHAR) AS "totalCovLandArea",
    CAST("totalCovLandPercentage" AS VARCHAR) AS "totalCovLandPercentage",
    CAST("totalCovMarineArea" AS VARCHAR) AS "totalCovMarineArea",
    CAST("totalCovMarinePercentage" AS VARCHAR) AS "totalCovMarinePercentage"
FROM "european-environment-agency-bise.protectedareas-stats"
