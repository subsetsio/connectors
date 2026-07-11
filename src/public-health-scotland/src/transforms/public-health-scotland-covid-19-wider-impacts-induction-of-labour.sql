-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    "HB" AS hb,
    "HBQF" AS hbqf,
    CAST("Month" AS BIGINT) AS month,
    CAST("SingletonLiveBirths37to42Wks" AS BIGINT) AS singletonlivebirths37to42wks,
    CAST("NumberInduced" AS BIGINT) AS numberinduced,
    CAST("NumberNotInduced" AS BIGINT) AS numbernotinduced,
    CAST("NumberInductionUnknown" AS BIGINT) AS numberinductionunknown,
    CAST("PercentInduced" AS DOUBLE) AS percentinduced,
    CAST("PercentNotInduced" AS DOUBLE) AS percentnotinduced,
    CAST("PercentUnknown" AS DOUBLE) AS percentunknown,
    "Country" AS country,
    "AgeGroup" AS agegroup,
    CAST("SIMDQuintile" AS BIGINT) AS simdquintile
FROM "public-health-scotland-covid-19-wider-impacts-induction-of-labour"
