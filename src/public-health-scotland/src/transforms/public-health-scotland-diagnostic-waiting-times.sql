-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    strptime("MonthEnding", '%Y%m%d')::DATE AS monthending,
    "HBT" AS hbt,
    "DiagnosticTestType" AS diagnostictesttype,
    "DiagnosticTestDescription" AS diagnostictestdescription,
    "WaitingTime" AS waitingtime,
    CAST("NumberOnList" AS BIGINT) AS numberonlist,
    "NumberOnListQF" AS numberonlistqf,
    "Country" AS country,
    "Type" AS type,
    "Description" AS description,
    strptime("Month", '%Y%m%d')::DATE AS month,
    CAST("NumberWaitingOverFourWeeks" AS BIGINT) AS numberwaitingoverfourweeks,
    "NumberWaitingOverFourWeeksQF" AS numberwaitingoverfourweeksqf,
    CAST("NumberWaitingOverSixWeeks" AS BIGINT) AS numberwaitingoversixweeks,
    "NumberWaitingOverSixWeeksQF" AS numberwaitingoversixweeksqf,
    "HBT2014" AS hbt2014
FROM "public-health-scotland-diagnostic-waiting-times"
