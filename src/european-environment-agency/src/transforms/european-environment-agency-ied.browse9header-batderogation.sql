SELECT
    CAST("BATAELName" AS VARCHAR) AS "BATAELName",
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("EndDate" AS VARCHAR) AS "EndDate",
    CAST("EUregReportingYear" AS VARCHAR) AS "EUregReportingYear",
    CAST("facilityInspireId" AS VARCHAR) AS "facilityInspireId",
    CAST("installationInspireId" AS VARCHAR) AS "installationInspireId",
    CAST("PublicReason" AS VARCHAR) AS "PublicReason",
    CAST("siteInspireId" AS VARCHAR) AS "siteInspireId",
    CAST("siteName" AS VARCHAR) AS "siteName",
    CAST("StartDate" AS VARCHAR) AS "StartDate",
    CAST("Status" AS VARCHAR) AS "Status"
FROM "european-environment-agency-ied.browse9header-batderogation"
