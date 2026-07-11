-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    "SchoolYear" AS schoolyear,
    "CA" AS ca,
    "ClassYear" AS classyear,
    "Sex" AS sex,
    "Vaccine" AS vaccine,
    CAST("NumberInCohort" AS BIGINT) AS numberincohort,
    "NumberInCohortQF" AS numberincohortqf,
    "NumberVaccinated" AS numbervaccinated,
    "NumberVaccinatedQF" AS numbervaccinatedqf,
    "PercentCoverage" AS percentcoverage,
    "PercentCoverageQF" AS percentcoverageqf,
    "HB" AS hb
FROM "public-health-scotland-hpv-immunisation-statistics"
