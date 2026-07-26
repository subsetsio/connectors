-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "board",
    "district_manager_first_name",
    "district_manager_last_name",
    "address",
    "city",
    "postcode",
    "phone_number",
    "email",
    "monthly_meeting",
    "borough",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta",
    "cb_chair_first_name",
    "cb_chair_last_name"
FROM "nyc-open-data-8z5h-tzdr"
