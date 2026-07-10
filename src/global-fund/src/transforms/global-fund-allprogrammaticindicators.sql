-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows mix baseline, target, result, disaggregation, and source fields across programmatic datasets; filter to the intended dataset, indicator, and period before comparing or summing values.
SELECT
    "programmaticIndicatorId" AS programmaticindicatorid,
    "indicatorName" AS indicatorname,
    "recordId" AS recordid,
    "activityAreaId" AS activityareaid,
    "startDate" AS startdate,
    "geographicCoverage" AS geographiccoverage,
    "isReversed" AS isreversed,
    "aggregationType" AS aggregationtype,
    "endDate" AS enddate,
    "periodCovered" AS periodcovered,
    CAST("periodFrom" AS BIGINT) AS periodfrom,
    CAST("periodTo" AS BIGINT) AS periodto,
    "grouping_Level1" AS grouping_level1,
    "grouping_Level2" AS grouping_level2,
    "valueType" AS valuetype,
    "baselineValueYear" AS baselinevalueyear,
    "baselineValueNumerator" AS baselinevaluenumerator,
    "baselineValueDenominator" AS baselinevaluedenominator,
    "baselineValuePercentage" AS baselinevaluepercentage,
    "baselineValueText" AS baselinevaluetext,
    "targetValueYear" AS targetvalueyear,
    "targetValueNumerator" AS targetvaluenumerator,
    "targetValueDenominator" AS targetvaluedenominator,
    "targetValuePercentage" AS targetvaluepercentage,
    "targetValueText" AS targetvaluetext,
    "resultValueYear" AS resultvalueyear,
    "resultValueNumerator" AS resultvaluenumerator,
    "resultValueDenominator" AS resultvaluedenominator,
    "resultValuePercentage" AS resultvaluepercentage,
    "resultValueText" AS resultvaluetext,
    "isMilestoneTarget" AS ismilestonetarget,
    "performance",
    "performanceCode" AS performancecode,
    "valueSource" AS valuesource,
    "dateTimeCreated" AS datetimecreated,
    "dateTimeUpdated" AS datetimeupdated,
    "programmaticDataSet" AS programmaticdataset
FROM "global-fund-allprogrammaticindicators"
