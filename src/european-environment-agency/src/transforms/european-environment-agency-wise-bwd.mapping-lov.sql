SELECT
    CAST("altLabel" AS VARCHAR) AS "altLabel",
    CAST("broader" AS VARCHAR) AS "broader",
    CAST("broadMatch" AS VARCHAR) AS "broadMatch",
    CAST("definition" AS VARCHAR) AS "definition",
    CAST("id" AS VARCHAR) AS "id",
    CAST("label" AS VARCHAR) AS "label",
    CAST("notation" AS VARCHAR) AS "notation",
    CAST("sameAs" AS VARCHAR) AS "sameAs",
    CAST("statusCode" AS VARCHAR) AS "statusCode",
    CAST("statusDate" AS VARCHAR) AS "statusDate",
    CAST("statusRemarks" AS VARCHAR) AS "statusRemarks",
    CAST("tableName" AS VARCHAR) AS "tableName",
    CAST("URI" AS VARCHAR) AS "URI"
FROM "european-environment-agency-wise-bwd.mapping-lov"
