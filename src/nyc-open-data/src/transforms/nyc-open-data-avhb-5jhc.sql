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
    CAST("edp" AS BIGINT) AS edp,
    "rc_code",
    "funding_source",
    "amp",
    "vendor_name",
    CAST("umis_bill_id" AS BIGINT) AS umis_bill_id,
    "revenue_month",
    strptime("service_start_date", '%m/%d/%Y')::DATE AS service_start_date,
    strptime("service_end_date", '%m/%d/%Y')::DATE AS service_end_date,
    CAST("_days" AS BIGINT) AS days,
    CAST("meter_number" AS BIGINT) AS meter_number,
    "estimated",
    CAST("current_charges" AS DOUBLE) AS current_charges,
    "rate_class",
    "bill_analyzed",
    CAST("consumption_therms" AS DOUBLE) AS consumption_therms,
    "es_commodity",
    "underlying_utility"
FROM "nyc-open-data-avhb-5jhc"
