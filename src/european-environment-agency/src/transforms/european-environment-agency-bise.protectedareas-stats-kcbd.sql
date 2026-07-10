SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("Discodata_update_marine" AS VARCHAR) AS "Discodata_update_marine",
    CAST("Discodata_update_terrestrial" AS VARCHAR) AS "Discodata_update_terrestrial",
    CAST("N2KcovLandPercentage" AS VARCHAR) AS "N2KcovLandPercentage",
    CAST("N2KCovMarinePercentage" AS VARCHAR) AS "N2KCovMarinePercentage",
    CAST("NatDAcovLandPercentage" AS VARCHAR) AS "NatDAcovLandPercentage",
    CAST("NatDACovMarinePercentage" AS VARCHAR) AS "NatDACovMarinePercentage",
    CAST("Temporal_coverage" AS VARCHAR) AS "Temporal_coverage",
    CAST("totalCovLandArea" AS VARCHAR) AS "totalCovLandArea",
    CAST("totalCovLandPercentage" AS VARCHAR) AS "totalCovLandPercentage",
    CAST("totalCovMarineArea" AS VARCHAR) AS "totalCovMarineArea",
    CAST("totalCovMarinePercentage" AS VARCHAR) AS "totalCovMarinePercentage"
FROM "european-environment-agency-bise.protectedareas-stats-kcbd"
