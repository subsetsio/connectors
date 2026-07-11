-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    CAST("MonthOfDelay" AS BIGINT) AS monthofdelay,
    "HBT" AS hbt,
    "HBTQF" AS hbtqf,
    "AgeGroup" AS agegroup,
    "AgeGroupQF" AS agegroupqf,
    "ReasonForDelay" AS reasonfordelay,
    "ReasonForDelayQF" AS reasonfordelayqf,
    CAST("NumberOfDelayedBedDays" AS BIGINT) AS numberofdelayedbeddays,
    CAST("AverageDailyNumberOfDelayedBeds" AS BIGINT) AS averagedailynumberofdelayedbeds,
    "CA" AS ca,
    "CAQF" AS caqf,
    CAST("NumberOfCensusDelays" AS BIGINT) AS numberofcensusdelays
FROM "public-health-scotland-delayed-discharges-in-nhsscotland"
