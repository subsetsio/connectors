SELECT
    CAST("bathingWaterIdentifier" AS VARCHAR) AS "bathingWaterIdentifier",
    CAST("geographicalConstraint" AS VARCHAR) AS "geographicalConstraint",
    CAST("groupIdentifier" AS VARCHAR) AS "groupIdentifier",
    CAST("link" AS VARCHAR) AS "link",
    CAST("metadata_beginLifeSpanVersion" AS VARCHAR) AS "metadata_beginLifeSpanVersion",
    CAST("metadata_endLifeSpanVersion" AS VARCHAR) AS "metadata_endLifeSpanVersion",
    CAST("metadata_observationStatus" AS VARCHAR) AS "metadata_observationStatus",
    CAST("metadata_replacedBy" AS VARCHAR) AS "metadata_replacedBy",
    CAST("metadata_replaces" AS VARCHAR) AS "metadata_replaces",
    CAST("metadata_statements" AS VARCHAR) AS "metadata_statements",
    CAST("metadata_statusCode" AS VARCHAR) AS "metadata_statusCode",
    CAST("metadata_statusDate" AS VARCHAR) AS "metadata_statusDate",
    CAST("metadata_versionId" AS VARCHAR) AS "metadata_versionId",
    CAST("qualityClass" AS VARCHAR) AS "qualityClass",
    CAST("remarks" AS VARCHAR) AS "remarks",
    CAST("season" AS VARCHAR) AS "season",
    CAST("UID" AS VARCHAR) AS "UID"
FROM "european-environment-agency-wise-bwd.timeseries-characterisation"
