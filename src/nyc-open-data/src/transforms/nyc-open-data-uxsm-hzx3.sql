-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "report_date",
    "agency_code",
    "agency_description",
    "title_code",
    "title_description",
    "pure_prov_09_mos",
    "pure_prov_1024_mos",
    "pure_prov_25_mos",
    "pure_subtotal",
    "step_prov_09_mos",
    "step_prov_1024_mos",
    "step_prov_25_mos",
    "step_subtotal",
    "total_count"
FROM "nyc-open-data-uxsm-hzx3"
