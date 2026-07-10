SELECT
    CAST("confidentialityReason" AS VARCHAR) AS "confidentialityReason",
    CAST("controlFileId" AS VARCHAR) AS "controlFileId",
    CAST("facilityReportId" AS VARCHAR) AS "facilityReportId",
    CAST("furtherDetails" AS VARCHAR) AS "furtherDetails",
    CAST("Id" AS VARCHAR) AS "Id",
    CAST("methodCode" AS VARCHAR) AS "methodCode",
    CAST("pollutant" AS VARCHAR) AS "pollutant",
    CAST("rawId" AS VARCHAR) AS "rawId",
    CAST("totalPollutantQuantityKg" AS VARCHAR) AS "totalPollutantQuantityKg"
FROM "european-environment-agency-ied.offsitepollutanttransfer"
