SELECT
    CAST("amount" AS VARCHAR) AS "amount",
    CAST("eprtrReportingYear" AS VARCHAR) AS "eprtrReportingYear",
    CAST("euregReportingYear" AS VARCHAR) AS "euregReportingYear",
    CAST("Installation Inspire ID" AS VARCHAR) AS "Installation Inspire ID",
    CAST("installationId" AS VARCHAR) AS "installationId",
    CAST("LCP Inspire ID" AS VARCHAR) AS "LCP Inspire ID",
    CAST("lcpId" AS VARCHAR) AS "lcpId",
    CAST("LCPNameInspireID" AS VARCHAR) AS "LCPNameInspireID",
    CAST("pollutant" AS VARCHAR) AS "pollutant",
    CAST("Site Inspire ID" AS VARCHAR) AS "Site Inspire ID",
    CAST("siteId" AS VARCHAR) AS "siteId"
FROM "european-environment-agency-ied.tableau-browse10-lcppollutant"
