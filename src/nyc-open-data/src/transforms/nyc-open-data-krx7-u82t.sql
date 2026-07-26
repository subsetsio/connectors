-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "created",
    "bic_number",
    "account_name",
    "trade_name",
    "address",
    "city",
    "state",
    "postcode",
    "phone",
    "email",
    "application_type",
    "disposition_date",
    "effective_date",
    "expiration_date",
    "renewal",
    "export_date",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta",
    "boro"
FROM "nyc-open-data-krx7-u82t"
