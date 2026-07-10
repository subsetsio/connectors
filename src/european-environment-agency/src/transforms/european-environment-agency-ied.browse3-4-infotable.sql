SELECT
    CAST("Activities" AS VARCHAR) AS "Activities",
    CAST("eprtrReportingYear" AS VARCHAR) AS "eprtrReportingYear",
    CAST("euregReportingYear" AS VARCHAR) AS "euregReportingYear",
    CAST("InspireSiteId" AS VARCHAR) AS "InspireSiteId",
    CAST("Installation regulatory information" AS VARCHAR) AS "Installation regulatory information",
    CAST("pollu" AS VARCHAR) AS "pollu",
    CAST("Site Country" AS VARCHAR) AS "Site Country",
    CAST("site" AS VARCHAR) AS "site",
    CAST("site_details" AS VARCHAR) AS "site_details",
    CAST("x_3857" AS VARCHAR) AS "x_3857",
    CAST("y_3857" AS VARCHAR) AS "y_3857"
FROM "european-environment-agency-ied.browse3-4-infotable"
