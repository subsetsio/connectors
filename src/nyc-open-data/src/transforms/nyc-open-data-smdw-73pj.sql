-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "development_name",
    "borough",
    "account_name",
    "_location" AS location,
    "meter_amr",
    "meter_scope",
    "tds",
    "edp",
    "rc_code",
    "funding_source",
    "amp",
    "vendor_name",
    "umis_bill_id",
    strptime("revenue_month", '%Y-%m')::DATE AS revenue_month,
    "service_start_date",
    "service_end_date",
    "_days" AS days,
    "meter_number",
    "estimated",
    "current_charges",
    "rate_class",
    "bill_analyzed",
    "consumption_mlbs"
FROM "nyc-open-data-smdw-73pj"
