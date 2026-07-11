-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    "Year" AS year,
    "Month" AS month,
    "Country" AS country,
    "HBT" AS hbt,
    "Type" AS type,
    "TypeQF" AS typeqf,
    "ConsultationType" AS consultationtype,
    "ConsultationTypeQF" AS consultationtypeqf,
    CAST("NumberOfConsultations" AS BIGINT) AS numberofconsultations,
    CAST("YearMonth" AS TIMESTAMP) AS yearmonth,
    CAST("Day" AS BIGINT) AS day,
    CAST("AEAttendancesUnplannedPlusNewPlanned" AS BIGINT) AS aeattendancesunplannedplusnewplanned,
    "AEAttendancesUnplannedPlusNewPlannedQF" AS aeattendancesunplannedplusnewplannedqf,
    "NumberOfConsultationsQF" AS numberofconsultationsqf,
    CAST("NumberOfCases" AS BIGINT) AS numberofcases,
    "NumberOfCasesQF" AS numberofcasesqf
FROM "public-health-scotland-primary-care-out-of-hours"
