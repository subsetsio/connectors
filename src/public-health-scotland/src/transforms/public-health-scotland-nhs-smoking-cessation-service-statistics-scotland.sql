-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    "FinancialYear" AS financialyear,
    "Gender" AS gender,
    "GenderQF" AS genderqf,
    "AgeGroup" AS agegroup,
    "AgeGroupQF" AS agegroupqf,
    CAST("NumberQuitAttempts" AS BIGINT) AS numberquitattempts,
    CAST("NumberFourWeekQuits" AS BIGINT) AS numberfourweekquits,
    CAST("NumberTwelveWeekQuits" AS BIGINT) AS numbertwelveweekquits,
    CAST("FourWeekQuitRate" AS DOUBLE) AS fourweekquitrate,
    CAST("TwelveWeekQuitRate" AS DOUBLE) AS twelveweekquitrate,
    "HBT" AS hbt,
    "HBTQF" AS hbtqf,
    "CA" AS ca,
    "CAQF" AS caqf,
    CAST("SIMDQuintile" AS BIGINT) AS simdquintile
FROM "public-health-scotland-nhs-smoking-cessation-service-statistics-scotland"
