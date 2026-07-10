SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("euFloodsRiskZoneCode" AS VARCHAR) AS "euFloodsRiskZoneCode",
    CAST("euFloodsUnitOfManagementCode" AS VARCHAR) AS "euFloodsUnitOfManagementCode",
    CAST("impactConsequence" AS VARCHAR) AS "impactConsequence",
    CAST("metadata_beginLifeSpanVersion" AS VARCHAR) AS "metadata_beginLifeSpanVersion",
    CAST("metadata_statusCode" AS VARCHAR) AS "metadata_statusCode",
    CAST("metadata_versionId" AS VARCHAR) AS "metadata_versionId",
    CAST("otherImpactConsequence" AS VARCHAR) AS "otherImpactConsequence",
    CAST("typeImpactConsequence" AS VARCHAR) AS "typeImpactConsequence"
FROM "european-environment-agency-wise-floods.areaofpotentialsignificantfloodrisk-potencialconsequence"
