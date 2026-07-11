-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are aggregate assessment results by entity, subject or grade, and subgroup; do not sum across overlapping subgroups.
SELECT
    "report_year",
    strptime("school_year", '%m/%d/%Y')::DATE AS school_year,
    CAST("nrc_code" AS BIGINT) AS nrc_code,
    "nrc_desc",
    "county_code",
    "county_desc",
    "bedscode",
    "name",
    "item_subject_area",
    "item_desc",
    "subgroup_code",
    "subgroup_name",
    "total_tested",
    "l1_count",
    "l1_pct",
    "l2_count",
    "l2_pct",
    "l3_count",
    "l3_pct",
    "l4_count",
    "l4_pct",
    "l2_l4_pct",
    "l3_l4_pct",
    "mean_scale_score",
    "sum_of_scale_score",
    "sy_end_date",
    "total_enrolled",
    "total_not_tested"
FROM "new-york-state-education-department-assessment-3-8-ela-math"
