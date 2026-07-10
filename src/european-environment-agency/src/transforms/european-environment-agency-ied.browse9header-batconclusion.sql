SELECT
    CAST("BATConclusionDate" AS VARCHAR) AS "BATConclusionDate",
    CAST("BATConclusionName" AS VARCHAR) AS "BATConclusionName",
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("EUregReportingYear" AS VARCHAR) AS "EUregReportingYear",
    CAST("facilityInspireId" AS VARCHAR) AS "facilityInspireId",
    CAST("installationInspireId" AS VARCHAR) AS "installationInspireId",
    CAST("siteInspireId" AS VARCHAR) AS "siteInspireId",
    CAST("siteName" AS VARCHAR) AS "siteName",
    CAST("Status" AS VARCHAR) AS "Status",
    CAST("StatusModifiedYear" AS VARCHAR) AS "StatusModifiedYear"
FROM "european-environment-agency-ied.browse9header-batconclusion"
