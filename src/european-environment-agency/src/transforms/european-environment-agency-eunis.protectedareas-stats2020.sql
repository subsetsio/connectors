SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("covLandPercentage" AS VARCHAR) AS "covLandPercentage",
    CAST("covMarinePercentage" AS VARCHAR) AS "covMarinePercentage"
FROM "european-environment-agency-eunis.protectedareas-stats2020"
