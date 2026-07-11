-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    "FinancialYear" AS financialyear,
    "HBR" AS hbr,
    "HBRQF" AS hbrqf,
    "CA" AS ca,
    "CAQF" AS caqf,
    "AgeGroup" AS agegroup,
    "AgeGroupQF" AS agegroupqf,
    "Sex" AS sex,
    "SexQF" AS sexqf,
    "InjuryLocation" AS injurylocation,
    "InjuryLocationQF" AS injurylocationqf,
    "InjuryType" AS injurytype,
    "InjuryTypeQF" AS injurytypeqf,
    CAST("NumberOfAdmissions" AS BIGINT) AS numberofadmissions,
    CAST("Year" AS BIGINT) AS year,
    CAST("NumberofDeaths" AS BIGINT) AS numberofdeaths
FROM "public-health-scotland-unintentional-injuries"
