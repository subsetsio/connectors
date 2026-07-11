-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "resource_id",
    "resource_name",
    CAST("FinancialYear" AS BIGINT) AS financialyear,
    "Sex" AS sex,
    "AgeGroup" AS agegroup,
    CAST("Population" AS BIGINT) AS population,
    CAST("NumberBaselineCohort" AS BIGINT) AS numberbaselinecohort,
    CAST("NumberBaselineCohortOnOat" AS BIGINT) AS numberbaselinecohortonoat,
    CAST("PersonYearsAtRiskCohortOnOat" AS BIGINT) AS personyearsatriskcohortonoat,
    CAST("PersonYearsAtRiskCohortOffOat" AS BIGINT) AS personyearsatriskcohortoffoat,
    CAST("DeathsCohortOnOat" AS BIGINT) AS deathscohortonoat,
    CAST("HospitalisationsCohortOnOat" AS BIGINT) AS hospitalisationscohortonoat,
    CAST("DeathsCohortOffOat" AS BIGINT) AS deathscohortoffoat,
    CAST("HospitalisationsCohortOffOat" AS BIGINT) AS hospitalisationscohortoffoat,
    CAST("DeathsUnobserved" AS BIGINT) AS deathsunobserved,
    CAST("HospitalisationsUnobserved" AS BIGINT) AS hospitalisationsunobserved,
    CAST("OtherCauseMortality" AS BIGINT) AS othercausemortality,
    CAST("PersonYearsAtRiskDiedDrd" AS BIGINT) AS personyearsatriskdieddrd
FROM "public-health-scotland-estimated-prevalence-of-opioid-dependence-in-scotland"
