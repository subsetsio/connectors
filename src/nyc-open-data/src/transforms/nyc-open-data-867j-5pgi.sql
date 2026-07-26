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
    "authorized_recycling_collection_type",
    "organic_waste_services_provided",
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
FROM "nyc-open-data-867j-5pgi"
