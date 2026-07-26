-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "prequalified_vendor_master_trade_code",
    "prequalified_vendor_trade_description",
    "prequalified_vendor_name",
    "prequalified_vendor_address",
    "prequalified_vendor_city_name",
    "prequalified_vendor_state_code",
    "prequalified_vendor_zip_code",
    "prequalified_vendor_phone_number",
    "prequalified_vendor_fax_number",
    "prequalified_vendor_contact_person",
    "prequalified_vendor_minority_business_indicator",
    "prequalified_vendor_women_business_indicator",
    "prequalified_vendor_local_business_indicator",
    "prequalified_vendor_over_million_dollar_revenue_indicator",
    strptime("prequalified_vendor_date", '%m/%d/%Y')::DATE AS prequalified_vendor_date
FROM "nyc-open-data-szkz-syh6"
