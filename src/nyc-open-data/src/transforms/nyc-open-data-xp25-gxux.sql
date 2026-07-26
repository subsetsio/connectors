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
    "final_submission_a",
    "gf_permit_application_id",
    "gf_doitt_submitted_to_cb_a",
    "gf_cb_comment_period_ends_a",
    "street_address",
    "cross_street_1",
    "cross_street_2",
    "ixn_corner",
    "postcode",
    "zoning",
    "longitude",
    "latitude",
    "site_in_business_improvement_district_bid",
    "bid",
    "link_in_historic_district",
    "historic_district_name",
    "neighborhood_tabulation_area_nta",
    "building_identification_number_bin",
    "boroughblocklot_bbl",
    "census_tract",
    "location2"
FROM "nyc-open-data-xp25-gxux"
