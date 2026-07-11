-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    CAST("Year" AS BIGINT) AS year,
    strptime("DateBeginning", '%Y%m%d')::DATE AS datebeginning,
    strptime("DateEnding", '%Y%m%d')::DATE AS dateending,
    "HB" AS hb,
    "HBQF" AS hbqf,
    "Source" AS source,
    CAST("TotalTested" AS BIGINT) AS totaltested,
    CAST("Positive" AS BIGINT) AS positive,
    CAST("Seroprevalence" AS DOUBLE) AS seroprevalence,
    CAST("LowerConfidenceInterval" AS DOUBLE) AS lowerconfidenceinterval,
    CAST("UpperConfidenceInterval" AS DOUBLE) AS upperconfidenceinterval,
    "Response" AS response,
    "Country" AS country,
    "AgeGroup" AS agegroup,
    "AgeGroupQF" AS agegroupqf,
    "Sex" AS sex,
    "SexQF" AS sexqf
FROM "public-health-scotland-enhanced-surveillance-of-covid-19-in-scotland"
