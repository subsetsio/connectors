SELECT
    CAST("BATAEL" AS VARCHAR) AS "BATAEL",
    CAST("BATDerogationIndicator" AS VARCHAR) AS "BATDerogationIndicator",
    CAST("controlFileId" AS VARCHAR) AS "controlFileId",
    CAST("derogationDurationEndDate" AS VARCHAR) AS "derogationDurationEndDate",
    CAST("derogationDurationStartDate" AS VARCHAR) AS "derogationDurationStartDate",
    CAST("Id" AS VARCHAR) AS "Id",
    CAST("installationId" AS VARCHAR) AS "installationId",
    CAST("publicReasonURL" AS VARCHAR) AS "publicReasonURL"
FROM "european-environment-agency-ied.productioninstallationbatderogation"
