SELECT
    CAST("amount" AS VARCHAR) AS "amount",
    CAST("eprtrReportingYear" AS VARCHAR) AS "eprtrReportingYear",
    CAST("euregReportingYear" AS VARCHAR) AS "euregReportingYear",
    CAST("Facility Inspire Id" AS VARCHAR) AS "Facility Inspire Id",
    CAST("facilityLocalCode" AS VARCHAR) AS "facilityLocalCode",
    CAST("identifier" AS VARCHAR) AS "identifier",
    CAST("indicator" AS VARCHAR) AS "indicator",
    CAST("LCPNameInspireID" AS VARCHAR) AS "LCPNameInspireID",
    CAST("Method used" AS VARCHAR) AS "Method used",
    CAST("Method" AS VARCHAR) AS "Method",
    CAST("pollutant" AS VARCHAR) AS "pollutant",
    CAST("releaseTarget" AS VARCHAR) AS "releaseTarget",
    CAST("Site Inspire ID" AS VARCHAR) AS "Site Inspire ID",
    CAST("siteId" AS VARCHAR) AS "siteId"
FROM "european-environment-agency-ied.tableau-browse7-pollutantreleases"
