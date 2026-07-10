SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("euFloodsUnitOfManagementCode" AS VARCHAR) AS "euFloodsUnitOfManagementCode",
    CAST("levelOfResponsibility" AS VARCHAR) AS "levelOfResponsibility",
    CAST("measureCode" AS VARCHAR) AS "measureCode",
    CAST("metadata_beginLifeSpanVersion" AS VARCHAR) AS "metadata_beginLifeSpanVersion",
    CAST("metadata_endLifeSpanVersion" AS VARCHAR) AS "metadata_endLifeSpanVersion",
    CAST("metadata_observationStatus" AS VARCHAR) AS "metadata_observationStatus",
    CAST("metadata_replacedBy" AS VARCHAR) AS "metadata_replacedBy",
    CAST("metadata_replaces" AS VARCHAR) AS "metadata_replaces",
    CAST("metadata_statements" AS VARCHAR) AS "metadata_statements",
    CAST("metadata_statusCode" AS VARCHAR) AS "metadata_statusCode",
    CAST("metadata_statusDate" AS VARCHAR) AS "metadata_statusDate",
    CAST("metadata_versionId" AS VARCHAR) AS "metadata_versionId",
    CAST("nameResponsibleAuthority" AS VARCHAR) AS "nameResponsibleAuthority",
    CAST("UID" AS VARCHAR) AS "UID"
FROM "european-environment-agency-wise-floods.floodriskmanagementplans-responsibleauthority"
