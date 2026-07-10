SELECT
    CAST("cArea" AS VARCHAR) AS "cArea",
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryGroup" AS VARCHAR) AS "countryGroup",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("lat" AS VARCHAR) AS "lat",
    CAST("lon" AS VARCHAR) AS "lon"
FROM "european-environment-agency-wise-indicators.spatialdata-country"
