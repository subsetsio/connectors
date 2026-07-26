-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "court_index_number",
    "docket_number",
    "eviction_address",
    "eviction_apartment_number",
    "executed_date",
    "marshal_first_name",
    "marshal_last_name",
    "residentialcommercial",
    "borough",
    "eviction_postcode",
    "ejectment",
    "evictionlegal_possession",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-6z8x-wfk4"
