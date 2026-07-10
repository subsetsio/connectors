SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("entityStatus" AS VARCHAR) AS "entityStatus",
    CAST("EUregReportingYear" AS VARCHAR) AS "EUregReportingYear",
    CAST("facilityInspireId" AS VARCHAR) AS "facilityInspireId",
    CAST("installationInspireId" AS VARCHAR) AS "installationInspireId",
    CAST("operatingSince_" AS VARCHAR) AS "operatingSince_",
    CAST("permitAvailable" AS VARCHAR) AS "permitAvailable",
    CAST("permitingAuthority" AS VARCHAR) AS "permitingAuthority",
    CAST("permitUpdated" AS VARCHAR) AS "permitUpdated",
    CAST("regulatedActivities" AS VARCHAR) AS "regulatedActivities",
    CAST("seveso" AS VARCHAR) AS "seveso",
    CAST("siteInspireId" AS VARCHAR) AS "siteInspireId",
    CAST("siteName" AS VARCHAR) AS "siteName"
FROM "european-environment-agency-ied.browse9header-permit"
