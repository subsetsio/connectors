SELECT
    CAST("archivedFiles" AS VARCHAR) AS "archivedFiles",
    CAST("contentType" AS VARCHAR) AS "contentType",
    CAST("envUrl" AS VARCHAR) AS "envUrl",
    CAST("fileName" AS VARCHAR) AS "fileName",
    CAST("fileSize" AS VARCHAR) AS "fileSize",
    CAST("fileSizeHR" AS VARCHAR) AS "fileSizeHR",
    CAST("isRestricted" AS VARCHAR) AS "isRestricted",
    CAST("pk" AS VARCHAR) AS "pk",
    CAST("schemaURL" AS VARCHAR) AS "schemaURL",
    CAST("title" AS VARCHAR) AS "title",
    CAST("ts_modified" AS VARCHAR) AS "ts_modified",
    CAST("uploadDate" AS VARCHAR) AS "uploadDate",
    CAST("url" AS VARCHAR) AS "url"
FROM "european-environment-agency-ied.eprtrenvelopefile"
