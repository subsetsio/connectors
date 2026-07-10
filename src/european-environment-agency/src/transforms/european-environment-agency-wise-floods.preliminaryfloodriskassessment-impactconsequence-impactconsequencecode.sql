SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("degreeTotalDamage" AS VARCHAR) AS "degreeTotalDamage",
    CAST("degreeTotalDamageClass" AS VARCHAR) AS "degreeTotalDamageClass",
    CAST("degreeTotalDamageGDP" AS VARCHAR) AS "degreeTotalDamageGDP",
    CAST("euFloodsHazardAreaCode" AS VARCHAR) AS "euFloodsHazardAreaCode",
    CAST("fatalities" AS VARCHAR) AS "fatalities",
    CAST("impactConsequenceCode" AS VARCHAR) AS "impactConsequenceCode",
    CAST("metadata_beginLifeSpanVersion" AS VARCHAR) AS "metadata_beginLifeSpanVersion",
    CAST("metadata_statusCode" AS VARCHAR) AS "metadata_statusCode",
    CAST("metadata_versionId" AS VARCHAR) AS "metadata_versionId",
    CAST("otherConsequenceDescription" AS VARCHAR) AS "otherConsequenceDescription",
    CAST("otherDamageDescription" AS VARCHAR) AS "otherDamageDescription",
    CAST("typeImpactConsequence" AS VARCHAR) AS "typeImpactConsequence"
FROM "european-environment-agency-wise-floods.preliminaryfloodriskassessment-impactconsequence-impactconsequencecode"
