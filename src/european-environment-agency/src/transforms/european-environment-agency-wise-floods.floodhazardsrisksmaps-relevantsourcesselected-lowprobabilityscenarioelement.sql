SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("euFloodsUnitOfManagementCode" AS VARCHAR) AS "euFloodsUnitOfManagementCode",
    CAST("highProbabilityScenarioElementOther" AS VARCHAR) AS "highProbabilityScenarioElementOther",
    CAST("lowProbabilityScenarioElement" AS VARCHAR) AS "lowProbabilityScenarioElement",
    CAST("lowProbabilityScenarioElementOther" AS VARCHAR) AS "lowProbabilityScenarioElementOther",
    CAST("mediumProbabilityScenarioElementOther" AS VARCHAR) AS "mediumProbabilityScenarioElementOther",
    CAST("metadata_beginLifeSpanVersion" AS VARCHAR) AS "metadata_beginLifeSpanVersion",
    CAST("metadata_statusCode" AS VARCHAR) AS "metadata_statusCode",
    CAST("metadata_versionId" AS VARCHAR) AS "metadata_versionId",
    CAST("modellingNotUsedDescription" AS VARCHAR) AS "modellingNotUsedDescription",
    CAST("modellingUsed" AS VARCHAR) AS "modellingUsed",
    CAST("relevantSource" AS VARCHAR) AS "relevantSource",
    CAST("relevantSourceOtherDescription" AS VARCHAR) AS "relevantSourceOtherDescription"
FROM "european-environment-agency-wise-floods.floodhazardsrisksmaps-relevantsourcesselected-lowprobabilityscenarioelement"
