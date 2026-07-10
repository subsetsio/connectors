SELECT
    CAST("article_6_6_Applied" AS VARCHAR) AS "article_6_6_Applied",
    CAST("article_6_6_JustificationOther" AS VARCHAR) AS "article_6_6_JustificationOther",
    CAST("article_6_7_Applied" AS VARCHAR) AS "article_6_7_Applied",
    CAST("article_6_7_JustificationOther" AS VARCHAR) AS "article_6_7_JustificationOther",
    CAST("characteristicsOfFlooding" AS VARCHAR) AS "characteristicsOfFlooding",
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("euFloodsRiskZoneCode" AS VARCHAR) AS "euFloodsRiskZoneCode",
    CAST("euFloodsUnitOfManagementCode" AS VARCHAR) AS "euFloodsUnitOfManagementCode",
    CAST("metadata_beginLifeSpanVersion" AS VARCHAR) AS "metadata_beginLifeSpanVersion",
    CAST("metadata_statusCode" AS VARCHAR) AS "metadata_statusCode",
    CAST("metadata_versionId" AS VARCHAR) AS "metadata_versionId",
    CAST("otherCharacteristicsDescription" AS VARCHAR) AS "otherCharacteristicsDescription",
    CAST("otherMechanismDescription" AS VARCHAR) AS "otherMechanismDescription",
    CAST("otherSourceDescription" AS VARCHAR) AS "otherSourceDescription"
FROM "european-environment-agency-wise-floods.floodhazardsrisksmaps-apsfr-characteristicsofflooding"
