-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_udise_report_code" AS udise_report_code,
    "_udise_report_id" AS udise_report_id,
    CAST("_udise_year_id" AS BIGINT) AS udise_year_id,
    "visuals_m",
    "other",
    "visuals",
    "loco_motor",
    "loco_motor_f",
    "hearing_impaired_f",
    "other_m",
    "hearing_impaired_m",
    "location_name",
    "not_applicable_m",
    "loco_motor_m",
    "other_f",
    "visuals_f",
    "hearing_impaired",
    "not_applicable",
    "not_applicable_f",
    "sch_category_name",
    "sch_mgmt_name"
FROM "udise-r127"
