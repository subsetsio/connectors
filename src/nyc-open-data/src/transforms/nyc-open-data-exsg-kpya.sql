-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "bic_number",
    "account_name",
    "trade_name",
    "application_type",
    "application_industry",
    "application_status",
    "application_status_date",
    "street",
    "city",
    "state",
    "postcode",
    "renewal_application",
    "export_date",
    "borough",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-exsg-kpya"
