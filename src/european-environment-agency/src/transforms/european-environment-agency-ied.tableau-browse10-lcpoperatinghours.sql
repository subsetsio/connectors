SELECT
    CAST("combustionPlantCategory" AS VARCHAR) AS "combustionPlantCategory",
    CAST("eprtrReportingYear" AS VARCHAR) AS "eprtrReportingYear",
    CAST("euregReportingYear" AS VARCHAR) AS "euregReportingYear",
    CAST("Facility Inspire Id" AS VARCHAR) AS "Facility Inspire Id",
    CAST("facilityId" AS VARCHAR) AS "facilityId",
    CAST("Installation Inspire ID" AS VARCHAR) AS "Installation Inspire ID",
    CAST("LCP Inspire ID" AS VARCHAR) AS "LCP Inspire ID",
    CAST("lcpId" AS VARCHAR) AS "lcpId",
    CAST("LCPNameInspireID" AS VARCHAR) AS "LCPNameInspireID",
    CAST("numberOfOperatingHours" AS VARCHAR) AS "numberOfOperatingHours",
    CAST("proportionOfUsefulHeatProductionForDistrictHeating" AS VARCHAR) AS "proportionOfUsefulHeatProductionForDistrictHeating",
    CAST("Site Inspire ID" AS VARCHAR) AS "Site Inspire ID",
    CAST("siteId" AS VARCHAR) AS "siteId",
    CAST("withinRefinery" AS VARCHAR) AS "withinRefinery"
FROM "european-environment-agency-ied.tableau-browse10-lcpoperatinghours"
