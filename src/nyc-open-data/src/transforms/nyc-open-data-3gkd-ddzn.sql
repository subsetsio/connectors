-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "community_board",
    "chair",
    "district_manager",
    "board_meetingcabinet_meeting",
    "address_1",
    "address_2",
    "phone_number",
    "postcode",
    "borough",
    "latitude",
    "longitude",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta",
    "location_1"
FROM "nyc-open-data-3gkd-ddzn"
