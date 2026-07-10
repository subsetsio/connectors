SELECT
    CAST("Class" AS VARCHAR) AS "Class",
    CAST("CountryCode" AS VARCHAR) AS "CountryCode",
    CAST("CountryName" AS VARCHAR) AS "CountryName",
    CAST("LCPCounting" AS VARCHAR) AS "LCPCounting",
    CAST("ReportingYear" AS VARCHAR) AS "ReportingYear"
FROM "european-environment-agency-ied.lcp-classcounting-2004-2015"
