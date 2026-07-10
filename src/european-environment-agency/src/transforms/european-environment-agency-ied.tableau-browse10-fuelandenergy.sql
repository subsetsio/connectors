SELECT
    CAST("energyInput" AS VARCHAR) AS "energyInput",
    CAST("eprtrReportingYear" AS VARCHAR) AS "eprtrReportingYear",
    CAST("euregReportingYear" AS VARCHAR) AS "euregReportingYear",
    CAST("fuelInput" AS VARCHAR) AS "fuelInput",
    CAST("furtherDetails" AS VARCHAR) AS "furtherDetails",
    CAST("Installation Inspire ID" AS VARCHAR) AS "Installation Inspire ID",
    CAST("installationId" AS VARCHAR) AS "installationId",
    CAST("LCP Inspire ID" AS VARCHAR) AS "LCP Inspire ID",
    CAST("lcpId" AS VARCHAR) AS "lcpId",
    CAST("LCPNameInspireID" AS VARCHAR) AS "LCPNameInspireID",
    CAST("Other gaseous fuel" AS VARCHAR) AS "Other gaseous fuel",
    CAST("Other soil fuel" AS VARCHAR) AS "Other soil fuel",
    CAST("Site Inspire ID" AS VARCHAR) AS "Site Inspire ID",
    CAST("siteId" AS VARCHAR) AS "siteId"
FROM "european-environment-agency-ied.tableau-browse10-fuelandenergy"
