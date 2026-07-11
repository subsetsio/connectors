-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    strptime("WeekEndingDate", '%Y%m%d')::DATE AS weekendingdate,
    "Country" AS country,
    "HBT" AS hbt,
    "TreatmentLocation" AS treatmentlocation,
    "DepartmentType" AS departmenttype,
    "AttendanceCategory" AS attendancecategory,
    CAST("NumberOfAttendancesEpisode" AS BIGINT) AS numberofattendancesepisode,
    CAST("NumberWithin4HoursEpisode" AS BIGINT) AS numberwithin4hoursepisode,
    CAST("NumberOver4HoursEpisode" AS BIGINT) AS numberover4hoursepisode,
    CAST("PercentageWithin4HoursEpisode" AS DOUBLE) AS percentagewithin4hoursepisode,
    CAST("NumberOver8HoursEpisode" AS BIGINT) AS numberover8hoursepisode,
    CAST("PercentageOver8HoursEpisode" AS DOUBLE) AS percentageover8hoursepisode,
    CAST("NumberOver12HoursEpisode" AS BIGINT) AS numberover12hoursepisode,
    CAST("PercentageOver12HoursEpisode" AS DOUBLE) AS percentageover12hoursepisode
FROM "public-health-scotland-weekly-accident-and-emergency-activity-and-waiting-times"
