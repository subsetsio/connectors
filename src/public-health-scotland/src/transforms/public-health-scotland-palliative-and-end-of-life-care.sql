-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    "FinancialYear" AS financialyear,
    "FinancialYearQF" AS financialyearqf,
    "HBR" AS hbr,
    "HBRQF" AS hbrqf,
    CAST("PercentageSpentInHomeCommunity" AS DOUBLE) AS percentagespentinhomecommunity,
    CAST("PercentageSpentInHospital" AS DOUBLE) AS percentagespentinhospital,
    CAST("NumberOfDeaths" AS BIGINT) AS numberofdeaths,
    CAST("TotalLengthOfStay" AS DOUBLE) AS totallengthofstay,
    CAST("AverageDaysInCommunity" AS BIGINT) AS averagedaysincommunity,
    CAST("AverageDaysInHospital" AS BIGINT) AS averagedaysinhospital,
    "HSCP" AS hscp,
    "CA" AS ca,
    "Country" AS country,
    "AgeGroup" AS agegroup,
    "Sex" AS sex,
    CAST("SIMD" AS BIGINT) AS simd,
    "UrbanRural6Fold" AS urbanrural6fold
FROM "public-health-scotland-palliative-and-end-of-life-care"
