-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "community_board",
    "neighborhoods",
    "cb_office_address",
    "cb_address_line_2",
    "cb_office_phone",
    "cb_office_fax",
    "cb_office_email",
    "cb_website",
    "cb_chair",
    "cb_district_manager",
    "cb_board_meeting",
    "cb_cabinet_meeting",
    "cb_precincts",
    "cb_precinct_phones",
    "latitude",
    "longitude",
    "community_board_1",
    "council_district",
    "bin",
    "bbl",
    "census_tract",
    "nta",
    "postcode",
    "location_point"
FROM "nyc-open-data-ruf7-3wgc"
