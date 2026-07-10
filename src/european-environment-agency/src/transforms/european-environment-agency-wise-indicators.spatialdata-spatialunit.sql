SELECT
    CAST("cArea" AS VARCHAR) AS "cArea",
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryGroup" AS VARCHAR) AS "countryGroup",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("geography" AS VARCHAR) AS "geography",
    CAST("geometry" AS VARCHAR) AS "geometry",
    CAST("lat" AS VARCHAR) AS "lat",
    CAST("lon" AS VARCHAR) AS "lon",
    CAST("spatialUnitIdentifier" AS VARCHAR) AS "spatialUnitIdentifier",
    CAST("spatialUnitIdentifierScheme" AS VARCHAR) AS "spatialUnitIdentifierScheme",
    CAST("spatialUnitName" AS VARCHAR) AS "spatialUnitName",
    CAST("statusCode" AS VARCHAR) AS "statusCode",
    CAST("statusDate" AS VARCHAR) AS "statusDate",
    CAST("statusRemarks" AS VARCHAR) AS "statusRemarks"
FROM "european-environment-agency-wise-indicators.spatialdata-spatialunit"
