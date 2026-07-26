-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "building_id",
    "bin",
    "street_address",
    "borocode",
    "block",
    "lot",
    "bqi",
    "discharged_aep",
    "discharged_7a",
    "hpd_vacate_order",
    "dob_vacate_order",
    "harassment_finding",
    "date_added",
    "borough",
    "postcode",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "bbl",
    "census_tract_2020",
    "neighborhood_tabulation_area_nta_2020"
FROM "nyc-open-data-bzxi-2tsw"
