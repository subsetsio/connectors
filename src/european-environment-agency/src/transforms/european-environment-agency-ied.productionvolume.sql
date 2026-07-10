SELECT
    CAST("Comments" AS VARCHAR) AS "Comments",
    CAST("controlFileId" AS VARCHAR) AS "controlFileId",
    CAST("facilityReportId" AS VARCHAR) AS "facilityReportId",
    CAST("Id" AS VARCHAR) AS "Id",
    CAST("productionVolume" AS VARCHAR) AS "productionVolume",
    CAST("productionVolumeUnits" AS VARCHAR) AS "productionVolumeUnits"
FROM "european-environment-agency-ied.productionvolume"
