SELECT
    CAST("combustionPlantCategory" AS VARCHAR) AS "combustionPlantCategory",
    CAST("confidentialityReason" AS VARCHAR) AS "confidentialityReason",
    CAST("controlFileId" AS VARCHAR) AS "controlFileId",
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("furtherDetails" AS VARCHAR) AS "furtherDetails",
    CAST("Id" AS VARCHAR) AS "Id",
    CAST("localId" AS VARCHAR) AS "localId",
    CAST("namespace" AS VARCHAR) AS "namespace",
    CAST("numberOfOperatingHours" AS VARCHAR) AS "numberOfOperatingHours",
    CAST("proportionOfUsefulHeatProductionForDistrictHeating" AS VARCHAR) AS "proportionOfUsefulHeatProductionForDistrictHeating",
    CAST("remarks" AS VARCHAR) AS "remarks",
    CAST("reportDataId" AS VARCHAR) AS "reportDataId",
    CAST("reportingYear" AS VARCHAR) AS "reportingYear",
    CAST("withinRefinery" AS VARCHAR) AS "withinRefinery"
FROM "european-environment-agency-ied.productioninstallationpartreport"
