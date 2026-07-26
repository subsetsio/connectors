-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "business_address",
    "business_name",
    "what_indicates_the_storefront_is_availablevacant",
    "is_the_storefront_boarded_up_with_plywood",
    "east_or_west_side_of_the_street",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta",
    "borough",
    "postcode"
FROM "nyc-open-data-w49t-5gha"
