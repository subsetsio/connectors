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
    CAST("Deaths" AS BIGINT) AS deaths,
    CAST("Average20152019" AS DOUBLE) AS average20152019,
    CAST("PercentVariation" AS DOUBLE) AS percentvariation,
    "PercentVariationQF" AS percentvariationqf,
    "HSCP" AS hscp,
    "Country" AS country,
    CAST("SIMDQuintile" AS BIGINT) AS simdquintile
FROM "public-health-scotland-covid-19-wider-impacts-deaths"
