-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    strptime("WeekEnding", '%Y%m%d')::DATE AS weekending,
    "HB" AS hb,
    "HBQF" AS hbqf,
    "AgeGroup" AS agegroup,
    "AgeGroupQF" AS agegroupqf,
    "Sex" AS sex,
    "SexQF" AS sexqf,
    CAST("CompletedContacts" AS BIGINT) AS completedcontacts,
    CAST("Average20182019" AS DOUBLE) AS average20182019,
    CAST("PercentVariation" AS DOUBLE) AS percentvariation,
    CAST("SIMDQuintile" AS BIGINT) AS simdquintile,
    "HSCP" AS hscp
FROM "public-health-scotland-covid-19-wider-impacts-contacts-with-nhs-24"
