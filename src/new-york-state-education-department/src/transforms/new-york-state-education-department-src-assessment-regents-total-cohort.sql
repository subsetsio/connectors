-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Total Cohort Regents rows measure cohort-based Regents outcomes, not annual exam administrations.
SELECT
    "report_year",
    "entity_cd",
    "entity_name",
    "subgroup_name",
    "subject",
    "cohort",
    "cohort_count",
    "ntest_count",
    "ntest_cohort",
    "test_count",
    "test_cohort",
    "level1_count",
    "level1_cohort",
    "level2_count",
    "level2_cohort",
    "level3_count",
    "level3_cohort",
    "level4_count",
    "level4_cohort",
    "prof_count",
    "prof_cohort",
    "institution_id",
    "total_exempt",
    "num_exempt_ntest",
    "pct_exempt_ntest",
    "num_exempt_test",
    "pct_exempt_test"
FROM "new-york-state-education-department-src-assessment-regents-total-cohort"
