SELECT
    CAST("controlFileId" AS VARCHAR) AS "controlFileId",
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("Datasource" AS VARCHAR) AS "Datasource",
    CAST("gmlId" AS VARCHAR) AS "gmlId",
    CAST("id" AS VARCHAR) AS "id",
    CAST("reportingYear" AS VARCHAR) AS "reportingYear"
FROM "european-environment-agency-ied.reportdata"
