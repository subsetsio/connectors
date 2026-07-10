SELECT
    CAST("characteristicsOfFlooding" AS VARCHAR) AS "characteristicsOfFlooding",
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("euFloodsHazardAreaCode" AS VARCHAR) AS "euFloodsHazardAreaCode",
    CAST("euFloodsRiskZoneCode" AS VARCHAR) AS "euFloodsRiskZoneCode",
    CAST("floodEventCode" AS VARCHAR) AS "floodEventCode",
    CAST("metadata_beginLifeSpanVersion" AS VARCHAR) AS "metadata_beginLifeSpanVersion",
    CAST("metadata_statusCode" AS VARCHAR) AS "metadata_statusCode",
    CAST("metadata_versionId" AS VARCHAR) AS "metadata_versionId",
    CAST("otherCharacteristicsDescription" AS VARCHAR) AS "otherCharacteristicsDescription",
    CAST("otherMechanismDescription" AS VARCHAR) AS "otherMechanismDescription",
    CAST("otherSourceDescription" AS VARCHAR) AS "otherSourceDescription"
FROM "european-environment-agency-wise-floods.preliminaryfloodriskassessment-floodeventlocation-characteristicsofflooding"
