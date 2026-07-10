SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("creator" AS VARCHAR) AS "creator",
    CAST("description" AS VARCHAR) AS "description",
    CAST("envUrl" AS VARCHAR) AS "envUrl",
    CAST("hasUnknownQC" AS VARCHAR) AS "hasUnknownQC",
    CAST("isBlockedByQCError" AS VARCHAR) AS "isBlockedByQCError",
    CAST("isReleased" AS VARCHAR) AS "isReleased",
    CAST("modifiedDate" AS VARCHAR) AS "modifiedDate",
    CAST("periodDescription" AS VARCHAR) AS "periodDescription",
    CAST("periodEndYear" AS VARCHAR) AS "periodEndYear",
    CAST("periodStartYear" AS VARCHAR) AS "periodStartYear",
    CAST("reportingDate" AS VARCHAR) AS "reportingDate",
    CAST("status" AS VARCHAR) AS "status",
    CAST("statusDate" AS VARCHAR) AS "statusDate",
    CAST("title" AS VARCHAR) AS "title",
    CAST("ts_modified" AS VARCHAR) AS "ts_modified"
FROM "european-environment-agency-ied.euregenvelope"
