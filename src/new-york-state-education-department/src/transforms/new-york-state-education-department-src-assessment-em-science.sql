-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are assessment aggregates by grade or assessment name and subgroup; overlapping subgroups should not be summed.
SELECT
    "report_year",
    "entity_cd",
    "entity_name",
    "year",
    "assessment_name",
    "subgroup_name",
    "num_tested",
    "not_tested",
    "level1_count",
    "level1_tested",
    "level2_count",
    "level2_tested",
    "level3_count",
    "level3_tested",
    "level4_count",
    "level4_tested",
    "level5_count",
    "level5_tested",
    "num_prof",
    "per_prof",
    "total_scale_scores",
    "mean_score",
    "institution_id",
    "total_count",
    "pct_not_tested",
    "pct_tested",
    "total_exempt",
    "num_exempt_ntest",
    "pct_exempt_ntest",
    "num_exempt_test",
    "pct_exempt_test"
FROM "new-york-state-education-department-src-assessment-em-science"
