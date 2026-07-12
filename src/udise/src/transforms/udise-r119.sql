-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This report is a wide UDISE+ cross-tab with no verified row key in the raw profile; treat rows as report records and filter the relevant dimensions before aggregating values.
SELECT
    "_udise_report_code" AS udise_report_code,
    "_udise_report_id" AS udise_report_id,
    CAST("_udise_year_id" AS BIGINT) AS udise_year_id,
    "c11_g",
    "ly5_b",
    "c11",
    "ly10_b",
    "ly8_b",
    "ly5",
    "ly8",
    "c11_b",
    "caste_name",
    "location_name",
    "c6",
    "c9_g",
    "c9_b",
    "caste_id",
    "c6_g",
    "c9",
    "ly5_g",
    "ly8_g",
    "c6_b",
    "ly10",
    "ly10_g"
FROM "udise-r119"
