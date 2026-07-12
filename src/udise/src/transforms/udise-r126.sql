-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This report is a wide UDISE+ cross-tab with no verified row key in the raw profile; treat rows as report records and filter the relevant dimensions before aggregating values.
SELECT
    "_udise_report_code" AS udise_report_code,
    "_udise_report_id" AS udise_report_id,
    CAST("_udise_year_id" AS BIGINT) AS udise_year_id,
    "caste_orc_f",
    "caste_obc_m",
    "caste_general_f",
    "caste_others_m",
    "caste_sc_f",
    "caste_general_m",
    "caste_others_f",
    "caste_sc_m",
    "caste_st_m",
    "total",
    "sch_mgmt_id",
    "location_name",
    "caste_st_f",
    "caste_obc_f",
    "caste_orc_m",
    "sch_mgmt_name"
FROM "udise-r126"
