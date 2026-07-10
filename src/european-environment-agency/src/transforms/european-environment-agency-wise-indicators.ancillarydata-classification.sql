SELECT
    CAST("classificationType" AS VARCHAR) AS "classificationType",
    CAST("eeaIndicator" AS VARCHAR) AS "eeaIndicator",
    CAST("fixedClassBoundary12" AS VARCHAR) AS "fixedClassBoundary12",
    CAST("fixedClassBoundary23" AS VARCHAR) AS "fixedClassBoundary23",
    CAST("fixedClassBoundary34" AS VARCHAR) AS "fixedClassBoundary34",
    CAST("fixedClassBoundary45" AS VARCHAR) AS "fixedClassBoundary45",
    CAST("qualityElementCode" AS VARCHAR) AS "qualityElementCode",
    CAST("qualityElementLabel" AS VARCHAR) AS "qualityElementLabel",
    CAST("remarks" AS VARCHAR) AS "remarks",
    CAST("resultUom" AS VARCHAR) AS "resultUom",
    CAST("sortKey" AS VARCHAR) AS "sortKey",
    CAST("waterBodyCategory" AS VARCHAR) AS "waterBodyCategory"
FROM "european-environment-agency-wise-indicators.ancillarydata-classification"
