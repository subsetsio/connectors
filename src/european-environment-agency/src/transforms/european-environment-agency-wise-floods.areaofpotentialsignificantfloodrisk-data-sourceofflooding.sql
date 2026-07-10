SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("crossBorderRelationship" AS VARCHAR) AS "crossBorderRelationship",
    CAST("euFloodsRiskZoneCode" AS VARCHAR) AS "euFloodsRiskZoneCode",
    CAST("euFloodsUnitOfManagementCode" AS VARCHAR) AS "euFloodsUnitOfManagementCode",
    CAST("metadata_beginLifeSpanVersion" AS VARCHAR) AS "metadata_beginLifeSpanVersion",
    CAST("metadata_statusCode" AS VARCHAR) AS "metadata_statusCode",
    CAST("metadata_versionId" AS VARCHAR) AS "metadata_versionId",
    CAST("otherCharacteristicsFloodingDescription" AS VARCHAR) AS "otherCharacteristicsFloodingDescription",
    CAST("otherMechanismFloodingDescription" AS VARCHAR) AS "otherMechanismFloodingDescription",
    CAST("otherSourceFloodingDescription" AS VARCHAR) AS "otherSourceFloodingDescription",
    CAST("sourceOfFlooding" AS VARCHAR) AS "sourceOfFlooding"
FROM "european-environment-agency-wise-floods.areaofpotentialsignificantfloodrisk-data-sourceofflooding"
