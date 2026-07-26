-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "hpd_building_id",
    "address",
    "bbl",
    "bin",
    "council_district",
    "community_district",
    "census_tract_2010",
    "neighborhood_tabulation_area",
    "postcode",
    "borough",
    "latitude",
    "longitude",
    "total_ih_floor_area",
    "transferred_ih_floor_area",
    "remaining_ih_floor_area",
    "property_type",
    "geocoding_method"
FROM "nyc-open-data-cm6g-t7ye"
