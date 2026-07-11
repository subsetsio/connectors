-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are accountability-scoped graduation-rate measures by cohort and subgroup, distinct from the standalone graduation outcomes table.
SELECT
    "report_year",
    "entity_cd",
    "entity_name",
    "year",
    "subgroup_name",
    "cohort",
    "state_baseline",
    "school_baseline",
    "cohort_count",
    "grad_rate",
    "mip",
    "state_mip",
    "long_term_goal",
    "exceed_lt_goal",
    "end_goal",
    "cohort_level",
    "override",
    "met_sh_target",
    "met_ag_target",
    "change_cohort",
    "change_grad_rate",
    "change_sh_target",
    "change_ag_target",
    "change_cohort_level",
    "display_cohort_count",
    "institution_id",
    "grad_count",
    "wt_perf_flag",
    "count_zero_non_display_flag"
FROM "new-york-state-education-department-src-acc-hs-graduation-rate"
