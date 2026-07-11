-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "resource_id",
    "resource_name",
    "Quarter" AS quarter,
    "HB" AS hb,
    "HBT" AS hbt,
    "HBTQF" AS hbtqf,
    "CancerType" AS cancertype,
    "CancerTypeQF" AS cancertypeqf,
    CAST("NumberOfEligibleReferrals31DayStandard" AS BIGINT) AS numberofeligiblereferrals31daystandard,
    "NumberOfEligibleReferrals31DayStandardQF" AS numberofeligiblereferrals31daystandardqf,
    CAST("NumberOfEligibleReferralsTreatedWithin31Days" AS BIGINT) AS numberofeligiblereferralstreatedwithin31days,
    "NumberOfEligibleReferralsTreatedWithin31DaysQF" AS numberofeligiblereferralstreatedwithin31daysqf,
    "HBQF" AS hbqf,
    CAST("NumberOfEligibleReferrals62DayStandard" AS BIGINT) AS numberofeligiblereferrals62daystandard,
    "NumberOfEligibleReferrals62DayStandardQF" AS numberofeligiblereferrals62daystandardqf,
    CAST("NumberOfEligibleReferralsTreatedWithin62Days" AS BIGINT) AS numberofeligiblereferralstreatedwithin62days,
    "NumberOfEligibleReferralsTreatedWithin62DaysQF" AS numberofeligiblereferralstreatedwithin62daysqf
FROM "public-health-scotland-cancer-waiting-times"
