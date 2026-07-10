SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("crossBorderRelationship" AS VARCHAR) AS "crossBorderRelationship",
    CAST("dateOfCommencement" AS VARCHAR) AS "dateOfCommencement",
    CAST("durationOfFlood" AS VARCHAR) AS "durationOfFlood",
    CAST("euFloodsUnitOfManagementCode" AS VARCHAR) AS "euFloodsUnitOfManagementCode",
    CAST("eventTypePastFuture" AS VARCHAR) AS "eventTypePastFuture",
    CAST("floodEventCode" AS VARCHAR) AS "floodEventCode",
    CAST("floodEventName" AS VARCHAR) AS "floodEventName",
    CAST("floodEventReference" AS VARCHAR) AS "floodEventReference",
    CAST("metadata_beginLifeSpanVersion" AS VARCHAR) AS "metadata_beginLifeSpanVersion",
    CAST("metadata_statusCode" AS VARCHAR) AS "metadata_statusCode",
    CAST("metadata_versionId" AS VARCHAR) AS "metadata_versionId",
    CAST("returnPeriod" AS VARCHAR) AS "returnPeriod"
FROM "european-environment-agency-wise-floods.preliminaryfloodriskassessment-floodevent"
