-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    "AgeofEvaluation" AS ageofevaluation,
    "EvaluationPeriod" AS evaluationperiod,
    "HBT" AS hbt,
    "Vaccine" AS vaccine,
    CAST("NumberInCohort" AS BIGINT) AS numberincohort,
    "NumberVaccinated" AS numbervaccinated,
    "NumberVaccinatedQF" AS numbervaccinatedqf,
    "PercentUptake" AS percentuptake,
    "PercentUptakeQF" AS percentuptakeqf,
    "CA" AS ca,
    "NumberInCohortQF" AS numberincohortqf,
    "EthnicGroup" AS ethnicgroup,
    "Ethnicity" AS ethnicity,
    CAST("UrbanRuralCode" AS BIGINT) AS urbanruralcode,
    "UrbanRuralName" AS urbanruralname
FROM "public-health-scotland-childhood-immunisation-statistics"
