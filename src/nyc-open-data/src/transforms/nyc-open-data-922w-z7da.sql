-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "physical_address_id",
    "location_id",
    "address_1",
    "address_2",
    "city",
    "borough",
    "state_province",
    "postcode",
    "site_catchment",
    "site_intersection_street_1",
    "site_intersection_street_2",
    "number",
    "street",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-922w-z7da"
