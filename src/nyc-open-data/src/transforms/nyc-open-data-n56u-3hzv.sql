-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "fiscal_year",
    "media_placement_vendor_name",
    "city_agency",
    "ad_campaign_name",
    "campaign_purpose",
    "media_outlet_name_city_agency_submission",
    "media_outlet_name_standardized",
    "media_type_agency_submission",
    "media_type_standardized",
    "_language" AS language,
    "run_start_date",
    "run_end_date",
    "_quarter" AS quarter,
    "net_spend_amount"
FROM "nyc-open-data-n56u-3hzv"
