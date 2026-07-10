SELECT
    CAST("confidentialityReason" AS VARCHAR) AS "confidentialityReason",
    CAST("controlFileId" AS VARCHAR) AS "controlFileId",
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("Id" AS VARCHAR) AS "Id",
    CAST("localId" AS VARCHAR) AS "localId",
    CAST("namespace" AS VARCHAR) AS "namespace",
    CAST("numberOfEmployees" AS VARCHAR) AS "numberOfEmployees",
    CAST("numberOfOperatingHours" AS VARCHAR) AS "numberOfOperatingHours",
    CAST("remarks" AS VARCHAR) AS "remarks",
    CAST("reportDataId" AS VARCHAR) AS "reportDataId",
    CAST("reportingYear" AS VARCHAR) AS "reportingYear",
    CAST("representativeStackHeightM" AS VARCHAR) AS "representativeStackHeightM",
    CAST("stackHeightClass" AS VARCHAR) AS "stackHeightClass"
FROM "european-environment-agency-ied.productionfacilityreport"
