SELECT
    CAST("excludeRecords" AS VARCHAR) AS "excludeRecords",
    CAST("n" AS VARCHAR) AS "n",
    CAST("recordQualityState" AS VARCHAR) AS "recordQualityState",
    CAST("recordTable" AS VARCHAR) AS "recordTable",
    CAST("statementLabel" AS VARCHAR) AS "statementLabel"
FROM "european-environment-agency-wise-indicators.ancillarytable-qualitycontrol"
