-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "community_district",
    "community_district_name",
    "tobacco_retail_dealer_cap",
    "active_tobacco_retail_dealer_licenses",
    "trd_available_under_cap",
    "electronic_cigarette_retail_dealer_cap",
    "active_electronic_cigarette_retail_dealer_licenses",
    "ecd_available_under_cap",
    "data_as_of"
FROM "nyc-open-data-p2wf-m8zt"
