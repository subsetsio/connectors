SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("metadata_statusCode" AS VARCHAR) AS "metadata_statusCode",
    CAST("metadata_versionId" AS VARCHAR) AS "metadata_versionId",
    CAST("monitoringSiteIdentifier" AS VARCHAR) AS "monitoringSiteIdentifier",
    CAST("ND_BeginDate" AS VARCHAR) AS "ND_BeginDate",
    CAST("ND_EndDate" AS VARCHAR) AS "ND_EndDate",
    CAST("ND_NatStatCode" AS VARCHAR) AS "ND_NatStatCode",
    CAST("ND_StationType" AS VARCHAR) AS "ND_StationType",
    CAST("ND_TrophicState" AS VARCHAR) AS "ND_TrophicState",
    CAST("parameterWaterBodyCategory" AS VARCHAR) AS "parameterWaterBodyCategory",
    CAST("phenomenonTimeReferenceYear" AS VARCHAR) AS "phenomenonTimeReferenceYear"
FROM "european-environment-agency-wise-nitrates.nid-eutrophicationstate"
