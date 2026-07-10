SELECT
    CAST("controlFileId" AS VARCHAR) AS "controlFileId",
    CAST("desulphurisationRate" AS VARCHAR) AS "desulphurisationRate",
    CAST("Id" AS VARCHAR) AS "Id",
    CAST("installationPartReportId" AS VARCHAR) AS "installationPartReportId",
    CAST("month" AS VARCHAR) AS "month",
    CAST("sulphurContent" AS VARCHAR) AS "sulphurContent",
    CAST("technicalJustification" AS VARCHAR) AS "technicalJustification"
FROM "european-environment-agency-ied.desulphurisationinformation"
