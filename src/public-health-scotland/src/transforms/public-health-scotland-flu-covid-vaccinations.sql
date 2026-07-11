-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    strptime("Date", '%Y%m%d')::DATE AS date,
    "Country" AS country,
    "Dose" AS dose,
    CAST("CumulativeNumberVaccinated" AS BIGINT) AS cumulativenumbervaccinated,
    "AgeBand" AS ageband,
    "JCVIPriorityGroup" AS jcviprioritygroup,
    CAST("Population" AS BIGINT) AS population,
    "PopulationQF" AS populationqf,
    CAST("CumulativePercentCoverage" AS DOUBLE) AS cumulativepercentcoverage,
    "CumulativePercentCoverageQF" AS cumulativepercentcoverageqf,
    CAST("NumberVaccinated" AS BIGINT) AS numbervaccinated,
    "PercentCoverage" AS percentcoverage,
    "HB" AS hb,
    "HBQF" AS hbqf,
    "HBName" AS hbname,
    "Ethnicity" AS ethnicity,
    CAST("Count" AS BIGINT) AS count,
    CAST("PercentageCoverage" AS DOUBLE) AS percentagecoverage,
    "JCVIPriorityGroupQF" AS jcviprioritygroupqf,
    "SIMD" AS simd,
    "UrbanRural" AS urbanrural
FROM "public-health-scotland-flu-covid-vaccinations"
