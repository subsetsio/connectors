-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    "Quarter" AS quarter,
    "QuarterQF" AS quarterqf,
    "HB" AS hb,
    "HBQF" AS hbqf,
    "Location" AS location,
    "LocationQF" AS locationqf,
    "AppointmentType" AS appointmenttype,
    "AppointmentTypeQF" AS appointmenttypeqf,
    CAST("Attendances" AS BIGINT) AS attendances,
    "AttendancesQF" AS attendancesqf,
    CAST("DNAAppointments" AS BIGINT) AS dnaappointments,
    "DNAAppointmentsQF" AS dnaappointmentsqf,
    CAST("DNARate" AS DOUBLE) AS dnarate,
    "DNARateQF" AS dnarateqf,
    "Sex" AS sex,
    "Age" AS age,
    CAST("SIMD" AS BIGINT) AS simd,
    "SIMDQF" AS simdqf,
    "Specialty" AS specialty,
    "SpecialtyName" AS specialtyname,
    "HBT" AS hbt,
    "HBR" AS hbr,
    CAST("CrossBoundaryFlag" AS BIGINT) AS crossboundaryflag,
    "loc_name",
    "dqNotesIP" AS dqnotesip,
    "dqNotesOP" AS dqnotesop,
    "dqNotesBeds" AS dqnotesbeds
FROM "public-health-scotland-outpatient-activity"
