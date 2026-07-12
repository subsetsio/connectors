-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    "HB" AS hb,
    CAST("Month" AS BIGINT) AS month,
    CAST("TotalPatientsSeen" AS BIGINT) AS totalpatientsseen,
    "TotalPatientsSeenQF" AS totalpatientsseenqf,
    CAST("NumberOfPatientsSeen0To18Weeks" AS BIGINT) AS numberofpatientsseen0to18weeks,
    "NumberOfPatientsSeen0To18WeeksQF" AS numberofpatientsseen0to18weeksqf,
    CAST("NumberOfPatientsSeen19To35Weeks" AS BIGINT) AS numberofpatientsseen19to35weeks,
    "NumberOfPatientsSeen19To35WeeksQF" AS numberofpatientsseen19to35weeksqf,
    CAST("NumberOfPatientsSeen36To52Weeks" AS BIGINT) AS numberofpatientsseen36to52weeks,
    "NumberOfPatientsSeen36To52WeeksQF" AS numberofpatientsseen36to52weeksqf,
    CAST("NumberOfPatientsSeenOver52Weeks" AS BIGINT) AS numberofpatientsseenover52weeks,
    "NumberOfPatientsSeenOver52WeeksQF" AS numberofpatientsseenover52weeksqf,
    CAST("MedianWeeksPatientsSeen" AS BIGINT) AS medianweekspatientsseen,
    "MedianWeeksPatientsSeenQF" AS medianweekspatientsseenqf,
    CAST("90thPercentileWeeksPatientsSeen" AS BIGINT) AS "90thpercentileweekspatientsseen",
    "90thPercentileWeeksPatientsSeenQF" AS "90thpercentileweekspatientsseenqf",
    CAST("TotalPatientsWaiting" AS BIGINT) AS totalpatientswaiting,
    "TotalPatientsWaitingQF" AS totalpatientswaitingqf,
    CAST("NumberOfPatientsWaiting0To18Weeks" AS BIGINT) AS numberofpatientswaiting0to18weeks,
    "NumberOfPatientsWaiting0To18WeeksQF" AS numberofpatientswaiting0to18weeksqf,
    CAST("NumberOfPatientsWaiting19To35Weeks" AS BIGINT) AS numberofpatientswaiting19to35weeks,
    "NumberOfPatientsWaiting19To35WeeksQF" AS numberofpatientswaiting19to35weeksqf,
    CAST("NumberOfPatientsWaiting36To52Weeks" AS BIGINT) AS numberofpatientswaiting36to52weeks,
    "NumberOfPatientsWaiting36To52WeeksQF" AS numberofpatientswaiting36to52weeksqf,
    CAST("NumberOfPatientsWaitingOver52Weeks" AS BIGINT) AS numberofpatientswaitingover52weeks,
    "NumberOfPatientsWaitingOver52WeeksQF" AS numberofpatientswaitingover52weeksqf,
    CAST("ReferralsAccepted" AS BIGINT) AS referralsaccepted,
    "ReferralsAcceptedQF" AS referralsacceptedqf,
    CAST("ReferralsReceived" AS BIGINT) AS referralsreceived,
    "ReferralsReceivedQF" AS referralsreceivedqf
FROM "public-health-scotland-psychological-therapies-waiting-times"
