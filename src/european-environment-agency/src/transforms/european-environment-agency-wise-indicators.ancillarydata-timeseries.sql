SELECT
    CAST("conversionFactor" AS VARCHAR) AS "conversionFactor",
    CAST("eeaIndicator" AS VARCHAR) AS "eeaIndicator",
    CAST("flag" AS VARCHAR) AS "flag",
    CAST("numberOfRecords" AS VARCHAR) AS "numberOfRecords",
    CAST("observedPropertyCode" AS VARCHAR) AS "observedPropertyCode",
    CAST("observedPropertyLabel" AS VARCHAR) AS "observedPropertyLabel",
    CAST("outputUom" AS VARCHAR) AS "outputUom",
    CAST("qualityElementCode" AS VARCHAR) AS "qualityElementCode",
    CAST("qualityElementLabel" AS VARCHAR) AS "qualityElementLabel",
    CAST("resultUom" AS VARCHAR) AS "resultUom",
    CAST("sortKey" AS VARCHAR) AS "sortKey",
    CAST("waterBodyCategory" AS VARCHAR) AS "waterBodyCategory"
FROM "european-environment-agency-wise-indicators.ancillarydata-timeseries"
