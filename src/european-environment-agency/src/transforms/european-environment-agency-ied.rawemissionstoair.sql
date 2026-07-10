SELECT
    CAST("confidentialityReason" AS VARCHAR) AS "confidentialityReason",
    CAST("controlFileId" AS VARCHAR) AS "controlFileId",
    CAST("pollutant" AS VARCHAR) AS "pollutant",
    CAST("ProductionInstallationPartReport_localId" AS VARCHAR) AS "ProductionInstallationPartReport_localId",
    CAST("ProductionInstallationPartReport_namespace" AS VARCHAR) AS "ProductionInstallationPartReport_namespace",
    CAST("totalPollutantQuantityTNE" AS VARCHAR) AS "totalPollutantQuantityTNE"
FROM "european-environment-agency-ied.rawemissionstoair"
