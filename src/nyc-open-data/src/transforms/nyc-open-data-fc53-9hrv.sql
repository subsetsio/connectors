-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "agency",
    "station_name",
    "type_of_charger",
    "no_of_plugs",
    "address",
    "city",
    "postcode",
    "borough",
    "public_charger",
    "fee_for_city_drivers",
    "latitude",
    "longitude",
    "community_district",
    "council_district",
    "census_tract_2020",
    "bin",
    "bbl",
    "neighborhood_tabulation_area_nta_2020"
FROM "nyc-open-data-fc53-9hrv"
