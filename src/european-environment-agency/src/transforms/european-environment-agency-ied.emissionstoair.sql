SELECT
    CAST("confidentialityReason" AS VARCHAR) AS "confidentialityReason",
    CAST("controlFileId" AS VARCHAR) AS "controlFileId",
    CAST("Id" AS VARCHAR) AS "Id",
    CAST("installationPartReportId" AS VARCHAR) AS "installationPartReportId",
    CAST("pollutant" AS VARCHAR) AS "pollutant",
    CAST("totalPollutantQuantityTNE" AS VARCHAR) AS "totalPollutantQuantityTNE"
FROM "european-environment-agency-ied.emissionstoair"
