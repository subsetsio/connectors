SELECT
    CAST("CountryCode" AS VARCHAR) AS "CountryCode",
    CAST("euregReportingYear" AS VARCHAR) AS "euregReportingYear",
    CAST("facilityInspireId" AS VARCHAR) AS "facilityInspireId",
    CAST("FacilityNameInspireID" AS VARCHAR) AS "FacilityNameInspireID",
    CAST("heatReleaseHazardousWaste" AS VARCHAR) AS "heatReleaseHazardousWaste",
    CAST("installationInspireId" AS VARCHAR) AS "installationInspireId",
    CAST("installationPartName" AS VARCHAR) AS "installationPartName",
    CAST("lcpInspireId" AS VARCHAR) AS "lcpInspireId",
    CAST("plantType" AS VARCHAR) AS "plantType",
    CAST("siteInspireId" AS VARCHAR) AS "siteInspireId",
    CAST("siteName" AS VARCHAR) AS "siteName",
    CAST("specificConditions" AS VARCHAR) AS "specificConditions",
    CAST("totalNominalCapacityAnyWaste" AS VARCHAR) AS "totalNominalCapacityAnyWaste",
    CAST("totalRatedThermalInput" AS VARCHAR) AS "totalRatedThermalInput",
    CAST("untreatedMunicipalWaste" AS VARCHAR) AS "untreatedMunicipalWaste"
FROM "european-environment-agency-ied.browse10-header"
