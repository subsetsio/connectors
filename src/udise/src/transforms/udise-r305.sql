-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This report is a wide UDISE+ cross-tab with no verified row key in the raw profile; treat rows as report records and filter the relevant dimensions before aggregating values.
SELECT
    "_udise_report_code" AS udise_report_code,
    "_udise_report_id" AS udise_report_id,
    CAST("_udise_year_id" AS BIGINT) AS udise_year_id,
    "lgd_blockname",
    "category_name",
    "having_no_pre_primary",
    "total_anganwadi_boys",
    "primary_teacher_only_female",
    "total_anganwadi",
    "primary_teacher_only",
    "sch_mgmt_center_id",
    "pre_primary_teacher_only_male",
    "district_name",
    "state_name",
    "having_pre_primary",
    "total_anganwadi_girls",
    "loc_name",
    "state_id",
    "state_cd",
    "cpp_b",
    "cpp",
    "co_locate_angwnadi",
    "district_cd",
    "sch_loc_r_u",
    "all_result2",
    CAST("all_result1" AS BIGINT) AS all_result1,
    "cpp_g",
    "sch_category_id",
    "pre_primary_teacher_only",
    "district_id",
    "primary_teacher_only_male",
    "pre_primary_teacher_only_female",
    "sch_mgmt_name"
FROM "udise-r305"
