SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("CountryName" AS VARCHAR) AS "CountryName",
    CAST("LCP Class" AS VARCHAR) AS "LCP Class",
    CAST("LCPCounting" AS VARCHAR) AS "LCPCounting",
    CAST("reportingYear" AS VARCHAR) AS "reportingYear"
FROM "european-environment-agency-ied.tableau-analysis-lcp-class"
