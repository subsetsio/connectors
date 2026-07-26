-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "data_published_in_district_resource_statement",
    "data_as_of",
    "borough",
    "community_district",
    "drs_medicaid_ma_only_enrollees",
    "drs_total_medicaid_ma_enrollees",
    "drs_cash_assistance_ca_recipients",
    "drs_cash_assistance_ca_cases",
    "drs_total_supplemental_nutrition_assistance_program_snap_recipients",
    "drs_total_supplemental_nutrition_assistance_program_snap_households"
FROM "nyc-open-data-au2c-rs69"
