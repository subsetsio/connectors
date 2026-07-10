SELECT
    CAST("class1" AS VARCHAR) AS "class1",
    CAST("class2" AS VARCHAR) AS "class2",
    CAST("class3" AS VARCHAR) AS "class3",
    CAST("class4" AS VARCHAR) AS "class4",
    CAST("class5" AS VARCHAR) AS "class5",
    CAST("eeaIndicator" AS VARCHAR) AS "eeaIndicator",
    CAST("maxValue" AS VARCHAR) AS "maxValue",
    CAST("meanValue" AS VARCHAR) AS "meanValue",
    CAST("minValue" AS VARCHAR) AS "minValue",
    CAST("numberOfCountries" AS VARCHAR) AS "numberOfCountries",
    CAST("numberOfReportedCountries" AS VARCHAR) AS "numberOfReportedCountries",
    CAST("numberOfReportedSites" AS VARCHAR) AS "numberOfReportedSites",
    CAST("numberOfSites" AS VARCHAR) AS "numberOfSites",
    CAST("phenomenonTimeReferenceYear" AS VARCHAR) AS "phenomenonTimeReferenceYear",
    CAST("resultUom" AS VARCHAR) AS "resultUom",
    CAST("stdevValue" AS VARCHAR) AS "stdevValue",
    CAST("waterBodyCategory" AS VARCHAR) AS "waterBodyCategory"
FROM "european-environment-agency-wise-indicators.aggregateddata-europe"
