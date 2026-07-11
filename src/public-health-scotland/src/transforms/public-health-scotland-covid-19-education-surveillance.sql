-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    strptime("WeekEnding", '%Y%m%d')::DATE AS weekending,
    "AgeGroup" AS agegroup,
    CAST("PatientsPositive" AS BIGINT) AS patientspositive,
    CAST("Rate" AS DOUBLE) AS rate,
    CAST("TotalTests" AS BIGINT) AS totaltests,
    CAST("PositiveTests" AS BIGINT) AS positivetests,
    CAST("NegativeTests" AS BIGINT) AS negativetests,
    CAST("PercentPositive" AS DOUBLE) AS percentpositive,
    CAST("AvgNumberAdmissions" AS DOUBLE) AS avgnumberadmissions,
    "AvgNumberAdmissionsQF" AS avgnumberadmissionsqf,
    CAST("TotalCases" AS BIGINT) AS totalcases,
    CAST("NumberCasesInEducationalSetting" AS BIGINT) AS numbercasesineducationalsetting,
    CAST("PercentCasesInEducationalSetting" AS DOUBLE) AS percentcasesineducationalsetting,
    CAST("NumberCasesInEducation" AS BIGINT) AS numbercasesineducation,
    CAST("PercentCasesInEducation" AS DOUBLE) AS percentcasesineducation,
    CAST("NumberCasesEmployedInEducation" AS BIGINT) AS numbercasesemployedineducation,
    CAST("PercentCasesEmployedInEducation" AS DOUBLE) AS percentcasesemployedineducation,
    CAST("IncompleteCases" AS BIGINT) AS incompletecases,
    CAST("PercentCompletedCases" AS DOUBLE) AS percentcompletedcases,
    strptime("TestWeekEnding", '%Y%m%d')::DATE AS testweekending,
    "Positive" AS positive,
    CAST("Number" AS BIGINT) AS number,
    "SchoolType" AS schooltype,
    CAST("Total" AS BIGINT) AS total,
    CAST("Percent" AS DOUBLE) AS percent
FROM "public-health-scotland-covid-19-education-surveillance"
