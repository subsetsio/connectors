SELECT
    CAST("CountryCode" AS VARCHAR) AS "CountryCode",
    CAST("indBranch" AS VARCHAR) AS "indBranch",
    CAST("indCodePlant" AS VARCHAR) AS "indCodePlant",
    CAST("indConditions" AS VARCHAR) AS "indConditions",
    CAST("indDateCompliance" AS VARCHAR) AS "indDateCompliance",
    CAST("indDateCompliance_original" AS VARCHAR) AS "indDateCompliance_original",
    CAST("indIndustriesID" AS VARCHAR) AS "indIndustriesID",
    CAST("indNamePlant" AS VARCHAR) AS "indNamePlant",
    CAST("indOrganicLoad" AS VARCHAR) AS "indOrganicLoad",
    CAST("indState" AS VARCHAR) AS "indState",
    CAST("repCode" AS VARCHAR) AS "repCode"
FROM "european-environment-agency-wise-uwwtd.t-industries"
