SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("cropCategory" AS VARCHAR) AS "cropCategory",
    CAST("cropIrrigationIdentifier" AS VARCHAR) AS "cropIrrigationIdentifier",
    CAST("cYear" AS VARCHAR) AS "cYear",
    CAST("irrigatedArea" AS VARCHAR) AS "irrigatedArea",
    CAST("irrigationSystemType" AS VARCHAR) AS "irrigationSystemType",
    CAST("metadata_beginLifeSpanVersion" AS VARCHAR) AS "metadata_beginLifeSpanVersion",
    CAST("metadata_statusCode" AS VARCHAR) AS "metadata_statusCode",
    CAST("metadata_versionId" AS VARCHAR) AS "metadata_versionId",
    CAST("placeOfUseIdentifier" AS VARCHAR) AS "placeOfUseIdentifier",
    CAST("remarks" AS VARCHAR) AS "remarks",
    CAST("waterQualityClass" AS VARCHAR) AS "waterQualityClass"
FROM "european-environment-agency-wise-wrr.cropirrigation"
