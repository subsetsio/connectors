SELECT
    CAST("controlFileId" AS VARCHAR) AS "controlFileId",
    CAST("dateOfGranting" AS VARCHAR) AS "dateOfGranting",
    CAST("dateOfLastUpdate" AS VARCHAR) AS "dateOfLastUpdate",
    CAST("enforcementAction" AS VARCHAR) AS "enforcementAction",
    CAST("Id" AS VARCHAR) AS "Id",
    CAST("installationId" AS VARCHAR) AS "installationId",
    CAST("permitGranted" AS VARCHAR) AS "permitGranted",
    CAST("permitReconsidered" AS VARCHAR) AS "permitReconsidered",
    CAST("permitUpdated" AS VARCHAR) AS "permitUpdated",
    CAST("permitURL" AS VARCHAR) AS "permitURL"
FROM "european-environment-agency-ied.productioninstallationpermitdetails"
