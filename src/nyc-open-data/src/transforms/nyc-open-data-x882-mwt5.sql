-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "provider_id",
    "provider_name",
    "hq_address_1",
    "hq_address_2",
    "hq_borough",
    "hq_city",
    "hq_state",
    "hq_postcode",
    "provider_ein",
    "provider_website",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-x882-mwt5"
