-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "site_id",
    "planned_kiosk_type",
    "installation_status",
    "ppt_id",
    "legacy_id",
    "borough",
    "council_district",
    "community_board",
    "street_address",
    "cross_street_1",
    "cross_street_2",
    "ixn_corner",
    "postcode",
    "zoning",
    "latitude",
    "longitude",
    "installation_complete",
    "activation_complete",
    "neighborhood_tabulation_area_nta",
    "building_identification_number_bin",
    "boroughblocklot_bbl",
    "census_tract_ct",
    "_location" AS location
FROM "nyc-open-data-s4kf-3yrf"
