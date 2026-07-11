-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Chronic absenteeism rows are subgroup accountability aggregates; do not add overlapping subgroups as independent populations.
SELECT
    "report_year",
    "entity_cd",
    "entity_name",
    "year",
    "subject",
    "subgroup_name",
    "state_baseline",
    "school_baseline",
    "attend_days",
    "absent_count",
    "absent_rate",
    "mip",
    "state_mip",
    "long_term_goal",
    "exceed_lt_goal",
    "end_goal",
    "level",
    "override",
    "enrollment",
    "met_sh_target",
    "met_ag_target",
    "institution_id",
    "data_rep_flag",
    "partial_data_flag",
    "count_zero_non_display_flag"
FROM "new-york-state-education-department-src-acc-em-chronic-absenteeism"
