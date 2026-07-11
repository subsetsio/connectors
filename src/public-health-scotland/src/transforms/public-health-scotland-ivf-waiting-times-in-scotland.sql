-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    "Quarter" AS quarter,
    "IVFCentre" AS ivfcentre,
    CAST("PatientsScreened" AS BIGINT) AS patientsscreened,
    "PatientsScreenedQF" AS patientsscreenedqf,
    CAST("NumberScreenedZeroTo13Weeks" AS BIGINT) AS numberscreenedzeroto13weeks,
    "NumberScreenedZeroTo13WeeksQF" AS numberscreenedzeroto13weeksqf,
    CAST("NumberScreened14To26Weeks" AS BIGINT) AS numberscreened14to26weeks,
    "NumberScreened14To26WeeksQF" AS numberscreened14to26weeksqf,
    CAST("NumberScreened27To39Weeks" AS BIGINT) AS numberscreened27to39weeks,
    "NumberScreened27To39WeeksQF" AS numberscreened27to39weeksqf,
    CAST("NumberScreened40To52Weeks" AS BIGINT) AS numberscreened40to52weeks,
    "NumberScreened40To52WeeksQF" AS numberscreened40to52weeksqf,
    CAST("NumberScreenedOver52Weeks" AS BIGINT) AS numberscreenedover52weeks,
    "NumberScreenedOver52WeeksQF" AS numberscreenedover52weeksqf,
    "HBR" AS hbr,
    "HBRQF" AS hbrqf,
    CAST("NumberOfReferrals" AS BIGINT) AS numberofreferrals,
    "NumberOfReferralsQF" AS numberofreferralsqf,
    CAST("Month" AS BIGINT) AS month,
    CAST("PatientsWaiting" AS BIGINT) AS patientswaiting,
    "PatientsWaitingQF" AS patientswaitingqf,
    CAST("NumberWaitingZeroTo13Weeks" AS BIGINT) AS numberwaitingzeroto13weeks,
    "NumberWaitingZeroTo13WeeksQF" AS numberwaitingzeroto13weeksqf,
    CAST("NumberWaiting14To26Weeks" AS BIGINT) AS numberwaiting14to26weeks,
    "NumberWaiting14To26WeeksQF" AS numberwaiting14to26weeksqf,
    CAST("NumberWaiting27To39Weeks" AS BIGINT) AS numberwaiting27to39weeks,
    "NumberWaiting27To39WeeksQF" AS numberwaiting27to39weeksqf,
    CAST("NumberWaiting40To52Weeks" AS BIGINT) AS numberwaiting40to52weeks,
    "NumberWaiting40To52WeeksQF" AS numberwaiting40to52weeksqf,
    CAST("NumberWaitingOver52Weeks" AS BIGINT) AS numberwaitingover52weeks,
    "NumberWaitingOver52WeeksQF" AS numberwaitingover52weeksqf
FROM "public-health-scotland-ivf-waiting-times-in-scotland"
