-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "borough_description",
    "block",
    "lot",
    "_location" AS location,
    "commonly_known_name",
    "community_board_district",
    "council_district",
    "property_disposed_to_entity",
    "property_disposed_to_last_name",
    "property_disposed_to_first_name",
    "additional_purchasers",
    "property_disposed_to_house_number",
    "property_disposed_to_street_name",
    "property_disposed_to_address_line_2",
    "property_disposed_to_city",
    "property_disposed_to_state",
    "property_disposed_to_zip",
    "description_of_restriction",
    "description_of_restriction_continued",
    "link_to_deedleaseeasement",
    "removalmodification_request_status",
    "link_to_posted_information",
    "latitude",
    "longitude"
FROM "nyc-open-data-rfu7-paqe"
