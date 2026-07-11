-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows mix aggregation levels and overlapping student subgroups; filter aggregation_type and subgroup before comparing pathway counts.
SELECT
    "report_year",
    "report_school_year",
    CAST("aggregation_index" AS BIGINT) AS aggregation_index,
    "aggregation_type",
    "institution_id",
    "aggregation_code",
    "aggregation_name",
    "lea_beds",
    "lea_name",
    CAST("nrc_code" AS BIGINT) AS nrc_code,
    "nrc_desc",
    "county_code",
    "county_name",
    CAST("nyc_ind" AS BIGINT) AS nyc_ind,
    "boces_code",
    "boces_name",
    CAST("membership_code" AS BIGINT) AS membership_code,
    "membership_desc",
    "subgroup_code",
    "subgroup_name",
    "course_of_study_code",
    "course_of_study",
    "student_count"
FROM "new-york-state-education-department-graduation-pathways"
