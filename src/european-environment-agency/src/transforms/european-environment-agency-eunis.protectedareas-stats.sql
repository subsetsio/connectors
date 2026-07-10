SELECT
    CAST("CDDAcovLandPercentage" AS VARCHAR) AS "CDDAcovLandPercentage",
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("N2KcovLandPercentage" AS VARCHAR) AS "N2KcovLandPercentage",
    CAST("publication_year" AS VARCHAR) AS "publication_year",
    CAST("totalCovLandPercentage" AS VARCHAR) AS "totalCovLandPercentage",
    CAST("totalCovMarinePercentage" AS VARCHAR) AS "totalCovMarinePercentage"
FROM "european-environment-agency-eunis.protectedareas-stats"
