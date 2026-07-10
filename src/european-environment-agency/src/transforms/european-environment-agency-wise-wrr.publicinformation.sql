SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("cYear" AS VARCHAR) AS "cYear",
    CAST("metadata_beginLifeSpanVersion" AS VARCHAR) AS "metadata_beginLifeSpanVersion",
    CAST("metadata_statusCode" AS VARCHAR) AS "metadata_statusCode",
    CAST("metadata_versionId" AS VARCHAR) AS "metadata_versionId",
    CAST("remarks" AS VARCHAR) AS "remarks",
    CAST("responsiblePartyIdentifier" AS VARCHAR) AS "responsiblePartyIdentifier",
    CAST("totalVolumeOfWaterSupplied" AS VARCHAR) AS "totalVolumeOfWaterSupplied",
    CAST("volumeOfTreatedUrbanWasteWater" AS VARCHAR) AS "volumeOfTreatedUrbanWasteWater",
    CAST("waterQualityClass" AS VARCHAR) AS "waterQualityClass",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-wise-wrr.publicinformation"
